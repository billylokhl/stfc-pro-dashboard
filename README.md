# STFC US Servers Dashboard

[![Deploy to GitHub Pages](https://github.com/billylokhl/stfc-pro-dashboard/actions/workflows/deploy.yml/badge.svg)](https://github.com/billylokhl/stfc-pro-dashboard/actions/workflows/deploy.yml)

Interactive analytics dashboard for Star Trek Fleet Command US servers.

## 🚀 Live Dashboard

**[View Live Dashboard →](https://billylokhl.github.io/stfc-pro-dashboard/)**

## 📊 Features

- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **Interactive Charts** - Powered by Chart.js with responsive tooltips
- **Population Rankings** - Track server activity and player counts
- **Power Rankings** - Analyze top players and power distribution
- **Incursion Analytics** - Monitor incursion performance metrics
- **Server Age Analysis** - Compare servers by age and maturity
- **Mobile-Friendly Interface** - Optimized touch interactions and tap tooltips

## 🛠️ Technology Stack

- Plain HTML/CSS/JavaScript
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Chart.js](https://www.chartjs.org/) - Interactive charting library
- [Chart.js Annotation Plugin](https://www.chartjs.org/chartjs-plugin-annotation/) - Enhanced chart annotations
- Python pipeline for data processing

## 📦 Data Pipeline

The dashboard is powered by a Python data pipeline:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the data pipeline
python pipeline.py
```

This generates `data.json` from the CSV source data.

## 🚀 Deployment

The dashboard is automatically deployed to GitHub Pages via GitHub Actions on every push to `main`.

### Manual Deployment

To deploy manually:

1. Ensure `data.json` is up to date
2. Push changes to `main` branch
3. GitHub Actions will automatically build and deploy

## 📱 Mobile Responsiveness

The dashboard prioritizes mobile-first design:

- Responsive chart sizing
- Touch-optimized tooltips
- Adaptive layout for all screen sizes
- Optimized for phones, tablets, and desktops

## 🤝 Contributing

This is a community analytics project. Data updates and feature suggestions are welcome.

## 📄 License

MIT License - Feel free to use and modify for your alliance or community.
