# spinnaker-pipeline

A Spinnaker pipeline definition for Orders (`pipeline.json`) and a script that checks its stage graph.

## Goal

Show a promotion flow of staging deploy, smoke tests, human approval and production rollout, expressed as stage dependencies.

## Run it

```
python3 validate.py
```

Expected output: `spinnaker ok: Deploy staging -> Smoke tests -> Approve prod -> Deploy prod canary -> Deploy prod full`

Not run end to end: no Spinnaker instance was available, so the pipeline was never saved or executed. The stages carry only accounts and types, not full manifests or job specs, so it would need those before it could run.

## What it proves

- The five stages form a linear graph through `requisiteStageRefIds`, with no duplicate ids, unknown references or cycles.
- Both production deploys (accounts `prod`) come after the `manualJudgment` stage `Approve prod`.
- A `docker` trigger on `ghcr.io/example/orders` starts the pipeline.

## Trade-offs

- The pipeline is JSON in git, so changes are reviewable, but Spinnaker has to be fed it (for example with `spin pipeline save`).
- `Deploy prod canary` is just a named deploy stage here; there is no automated canary analysis.
- Spinnaker is a heavy system to run for a small team.

## When not to use it

- When a Git-driven tool such as Argo CD or a CI workflow already covers promotion.
- For a single service with one environment.
