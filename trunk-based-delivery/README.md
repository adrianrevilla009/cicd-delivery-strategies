# trunk-based-delivery

A GitHub Actions workflow (`.github/workflows/ci.yml`) for trunk-based development, plus a script that checks it.

## Goal

Show a pipeline where everything merges to `main`, CI runs on every pull request, and only `main` can deploy.

## Run it

```
python3 validate.py
```

Expected output: `trunk-based ok`

Not run end to end: the workflow never ran on GitHub. The `build` job calls a reusable workflow from `adrianrevilla009/lab-workflows`, which was not available here, and the `deploy` job only echoes a message instead of deploying.

## What it proves

- The workflow triggers only on pushes and pull requests to `main`, and no `release/` branch appears.
- `build` reuses `validate-config.yml` from `lab-workflows`.
- `deploy` needs `build` and has the condition `github.ref == 'refs/heads/main'`, so pull requests never deploy.

## Trade-offs

- Incomplete work has to be hidden behind feature flags (see `feature-flag-rollout`), which adds flag cleanup work.
- The deploy step is a stub; a real one needs credentials and an environment.
- Depends on fast CI and a team used to small, frequent merges.

## When not to use it

- For software shipped in versioned releases that need long-lived maintenance branches.
- When there is no reliable automated test suite to protect `main`.
