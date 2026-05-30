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
