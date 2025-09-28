# CodeRabbit Toy Review Repository

This repository is intentionally small and noisy so you can push it to GitHub, wire it up to CodeRabbit, and experiment with automated code reviews.

## What Step 2 Actually Means

In the CodeRabbit quickstart, step 2 says: "Observe CodeRabbit perform a code review of a pull request that you initiate." All you have to do is:

1. Create a branch locally.
2. Make some changes (the provided scenarios help with that).
3. Push the branch and open a pull request against `main` on GitHub.
4. Wait a few seconds—CodeRabbit should automatically leave review comments on that PR.

The rest of this README gives you ready-made changes you can apply so you get rich feedback without thinking about what to break.

## Repository Layout

- `src/coderabbit_toy/` – sample production code with simple business logic.
- `tests/` – pytest-based regression tests.
- `scenarios/` – patch files you can apply to generate realistic pull requests with intentional issues.
- `scripts/` – helper scripts for preparing scenarios (currently a stub you can extend).

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

Everything should pass on the `main` branch. If your tests fail before opening a PR, fix them or reset before moving on.

## How to Use with CodeRabbit

1. Create a new GitHub repository (public or private).
2. Copy or push the contents of this folder to that repository.
3. Install the CodeRabbit GitHub App and enable it for your new repository.
4. Pick a scenario below, apply it on a new branch, and push that branch.
5. Open a pull request and refresh the page—CodeRabbit will start reviewing automatically.

### Scenario 1 – Sanitizer Regression (`scenarios/01_sanitizer_regression.patch`)

- Applies a "performance tweak" that accidentally reintroduces HTML/script injection risk.
- Adds a regression test that now fails to highlight the problem.
- Expect CodeRabbit to flag security concerns, missing tests, and behaviour regressions.

Usage:

```bash
git checkout -b scenario/sanitizer-regression
git apply scenarios/01_sanitizer_regression.patch
pytest  # expect failures
git status  # review the staged changes
```

Commit the changes, push the branch, and open a PR.

### Scenario 2 – Metrics Drift (`scenarios/02_metrics_drift.patch`)

- Introduces a new growth calculation that divides by the wrong baseline.
- Adds dead code and forgets to update tests.
- Expect feedback on logic bugs, unused code, and documentation gaps.

Usage:

```bash
git checkout -b scenario/metrics-drift
git apply scenarios/02_metrics_drift.patch
pytest  # fails because of the regression
```

### Scenario 3 – Documentation Noise (`scenarios/03_docs_noise.patch`)

- Adds customer-facing documentation with TODOs and inconsistent tone.
- Edits code comments and types without following the style guide.
- Expect copy-edit suggestions, todo reminders, and style hints.

Usage:

```bash
git checkout -b scenario/docs-noise
git apply scenarios/03_docs_noise.patch
```

These scenarios are independent—reset to `main` between each (`git checkout main && git reset --hard origin/main`). Feel free to tweak them or craft your own diffs once you are comfortable.

## Scripts (Optional)

The `scripts` folder is empty on purpose. Add helpers like `scripts/prepare_pr.py` if you want to automate scenario application or generate fresh diffs.

## Tips for Deeper Testing

- Push multiple commits to the same branch so you can see how CodeRabbit handles incremental reviews.
- Reply to its comments and request re-reviews.
- Combine patches or introduce lint-only changes to test low/no-code diffs.
- Try a tiny change (single line) versus a large one to understand comment density.

Happy breaking!

