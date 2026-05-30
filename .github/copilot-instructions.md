# STFC Dashboard - Repository Engineering Instructions

These instructions apply to all AI-assisted development work on the STFC Dashboard project.

## Engineering Workflow Rules

### Change Planning
Before making significant changes:

- If a task will modify more than 3 files OR more than 200 lines of code, first provide an implementation plan.
- Identify all files expected to change.
- Explain the intended approach before editing files.

### Incremental Development
For major features:

1. Analyze
2. Plan
3. Implement a minimal working version
4. Verify functionality
5. Expand incrementally

Avoid implementing large multi-component changes in a single pass.

### Terminal Execution Rules

**CRITICAL: These rules prevent Exit Code 130 failures and execution race conditions.**

#### Command Chaining Prohibition
**NEVER chain commands using `&&`, `||`, or `;` in terminal executions.**

Forbidden patterns:
```bash
# FORBIDDEN - Do NOT do this
git add . && git commit -m "message"
npm install && npm run build
command1 && command2 || fallback
```

Required pattern:
```bash
# CORRECT - Execute separately and sequentially
# Step 1:
git add .

# Wait for successful completion (exit code 0)

# Step 2 (separate execution):
git commit -m "message"
```

#### Atomic Operations
High-risk operations must be executed as separate, independent commands:

- **Git operations:** Never combine `git add` and `git commit`
- **Build chains:** Never combine `npm install` and `npm run build`
- **File operations:** Never combine `mkdir` and file creation commands
- **Multi-step deployments:** Break into individual verification steps

Each command must:
1. Execute independently
2. Complete successfully (exit code 0)
3. Be verified before proceeding to the next command

#### Execution Sequencing
When multiple commands are required:

1. Execute the first command
2. Wait for completion
3. Verify exit code is 0
4. Only then execute the next command

If any command fails:
- Stop the sequence immediately
- Report the failure
- Diagnose the issue
- Do not attempt subsequent commands

#### Git Workflow Pattern
For Git operations, always use this strict sequence:

```bash
# Step 1: Stage files
git add <files>

# Verify staging succeeded before proceeding

# Step 2: Commit (separate execution)
git commit -m "commit message"

# Verify commit succeeded before proceeding

# Step 3: Push (separate execution, only if requested)
git push
```

Never combine these operations.

#### GitHub CLI (`gh`) Execution
**WARNING: `gh` CLI commands can cause VS Code window crashes (Exit Code 5).**

Prefer web-based GitHub configuration over `gh` CLI when possible.

**Safer Alternative Pattern:**
```bash
# Instead of: gh api ...
# Do this:
# 1. Create config files locally
# 2. Commit and push
# 3. Configure via GitHub web UI
```

If `gh` commands are required:

- Execute `gh` commands individually, never chained with other operations
- Verify authentication status before API operations
- Use non-interactive mode where possible to avoid hanging prompts
- Add explicit timeouts for long-running API calls
- Wait for complete output before proceeding
- **Close unused terminal panes** before running `gh` commands

Known stable operations:
- File creation and Git operations
- Reading files
- Standard shell commands

Known crash-prone operations:
- `gh` API calls
- `gh` authentication flows
- Multiple simultaneous `gh` commands

#### VS Code Stability Precautions
To prevent window crashes and interruptions:

**Commit Frequently:**
- Commit working changes after each major step
- Create Git checkpoints before risky operations
- Never lose more than 5-10 minutes of work

**Conservative Operation Batching:**
- Limit parallel file operations to 3-5 files maximum
- Avoid reading multiple large files simultaneously
- Prefer sequential operations when stability is critical

**Terminal Output Management:**
- Avoid commands that produce excessive output (>1000 lines)
- Use `head`, `tail`, or `grep` to limit output
- Add `--quiet` or `--silent` flags when available
- Test with `--dry-run` flags before actual execution

**Checkpoint Pattern for Complex Tasks:**
```bash
# Step 1: Make changes to files
# Step 2: Test/verify
# Step 3: Commit immediately
git add <changed-files>
git commit -m "Checkpoint: [specific change]"
# Step 4: Continue to next change
```

**Long-Running Operations:**
- Break into smaller incremental steps
- Provide progress updates between steps
- Commit after each successful substep

### Refactoring Rules

- Prefer modifying existing working code over rewriting working code.
- Avoid large-scale search-and-replace operations without explicit approval.
- Avoid dashboard-wide refactors unless explicitly requested.
- Preserve existing functionality whenever possible.

### Error Handling
If a change introduces:

- build failures
- syntax errors
- runtime errors

then:

- stop making additional changes
- diagnose the root cause
- explain the issue
- propose a fix

Do not continue making unrelated modifications while errors remain unresolved.

### Risk Assessment
Before any architectural change, explain:

- why the change is necessary
- expected benefits
- risks
- rollback strategy

### Verification
After significant changes:

- verify build success
- verify desktop layout
- verify tablet layout
- verify mobile layout
- verify no console errors

---

## Dashboard-Specific Rules

### Mobile First
Mobile responsiveness is a primary requirement.

All chart and UI changes must consider:

- desktop
- tablet
- mobile

### Readability Priority
Prioritize:

- readability
- usability
- responsive behavior

over visual effects and decorative enhancements.

### Scatter Plot Rules
For scatter plots:

- prioritize data visibility
- avoid oversized highlight markers
- avoid permanent labels that obscure data
- use tooltips instead of persistent annotations whenever possible

### Feature Scope Control
When a request is primarily:

- bug fixing
- polish
- responsiveness
- usability

do not introduce unrelated new features unless explicitly requested.

### Stability First
When approaching a release-ready state:

- prioritize stabilization
- prioritize visual QA
- prioritize bug fixes

over introducing new capabilities.

---

## Working-State Protection
Before major modifications:

Recommend creating a Git checkpoint.

Examples:

```bash
git add .
git commit -m "Stable checkpoint before major change"
```

For large or risky tasks:

Recommend working in a feature branch.

Examples:

```bash
git checkout -b feature/new-capability
```

The objective is to ensure that working functionality is preserved and recoverable throughout development.
