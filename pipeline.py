import json
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://stfc.pro/servers"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("📥 Requesting page from stfc.pro...")
try:
    response = requests.get(URL, headers=HEADERS, timeout=15)
    if response.status_code != 200:
        print(f"❌ Failed to download page. Status code: {response.status_code}")
        exit()
except Exception as e:
    print(f"❌ Network connection failed: {e}")
    exit()

print("🧼 Parsing server-side rendered data string...")
soup = BeautifulSoup(response.text, "lxml")

target_data = None
# Look for scripts containing the key signature
for script in soup.find_all("script"):
    if script.string and "Tomalak" in script.string:
        target_data = script.string
        break

if not target_data:
    print("❌ Could not isolate the raw data block from the webpage HTML template.")
    exit()

try:
    # Find all serverid entries (quotes are escaped in the Next.js hydration format)
    serverid_matches = list(re.finditer(r'\\?"serverid\\?":\d+', target_data))

    if not serverid_matches:
        print("❌ Could not find server data in script")
        exit()

    # Find array boundaries
    first_match = serverid_matches[0]
    last_match = serverid_matches[-1]

    # Search backwards from first serverid for opening bracket
    search_back = target_data[max(0, first_match.start()-100):first_match.start()]
    opening_bracket_pos = search_back.rfind('[')

    if opening_bracket_pos == -1:
        print("❌ Could not find array start")
        exit()

    actual_start = first_match.start() - len(search_back) + opening_bracket_pos

    # Search forward from last serverid for closing bracket
    search_forward = target_data[last_match.end():last_match.end()+1000]
    closing_bracket_pos = search_forward.find(']')

    if closing_bracket_pos == -1:
        print("❌ Could not find array end")
        exit()

    actual_end = last_match.end() + closing_bracket_pos + 1

    # Extract and clean the JSON
    json_raw = target_data[actual_start:actual_end]
    json_cleaned = json_raw.replace('\\"', '"').replace('\\\\', '\\')
    json_cleaned = re.sub(r'"\$D([^"]+)"', r'"\1"', json_cleaned)

    raw_servers = json.loads(json_cleaned)
except Exception as e:
    print(f"❌ JSON formatting cleanup failed: {e}")
    exit()

print("📊 Structuring data array and engineering metrics...")
full_df = pd.DataFrame(raw_servers)

# Standardize column naming convention just in case keys are minified
if "serverid" not in full_df.columns and "id" in full_df.columns:
    full_df.rename(columns={"id": "serverid"}, inplace=True)

# Clean out non-US region strings
us_df = full_df[full_df["region"] == "US"].copy()

# Cast strings to explicit numeric datatypes
numeric_cols = ["players", "avglevel", "totalpower", "incwins", "incloss"]
for col in numeric_cols:
    if col in us_df.columns:
        us_df[col] = pd.to_numeric(us_df[col], errors='coerce').fillna(0)

# Handle creation date formats
if "created" in us_df.columns:
    us_df["created_dt"] = pd.to_datetime(us_df["created"], errors='coerce')
    us_df["creation_year"] = us_df["created_dt"].dt.year.fillna(2018).astype(int)
    us_df["server_age_years"] = 2026 - us_df["creation_year"]

# Calculate core derived aggregates cleanly without dividing by zero
us_df["total_incursions"] = us_df["incwins"] + us_df["incloss"]
us_df["incursion_win_rate"] = (us_df["incwins"] / us_df["total_incursions"].replace(0, 1)) * 100
us_df["power_per_player"] = us_df["totalpower"] / us_df["players"].replace(0, 1)

output_file = "stfc_us_servers_clean.csv"
us_df.to_csv(output_file, index=False)

# Export JSON for web dashboard
json_output = "data.json"
us_df.to_json(json_output, orient="records", indent=4)

print(f"🎉 Pipeline successfully compiled!")
print(f"Total US Servers Detected and Evaluated: {len(us_df)}")
print(f"Cleaned spreadsheet dataset saved to: {output_file}")
print(f"Web-ready JSON payload saved to: {json_output}")
