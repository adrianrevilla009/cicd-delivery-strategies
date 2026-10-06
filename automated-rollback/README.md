# automated-rollback

An Argo Rollouts `AnalysisTemplate` on error rate (`analysis.yaml`) and a Python simulation of its failure-limit decision.

## Goal

Show when a release is aborted automatically: a single bad sample is tolerated, repeated ones trigger a rollback.

## Run it

```
python3 simulate.py
```

Expected output: `automated rollback ok: bad release aborted at sample 4`

Only the decision logic is simulated, by `simulate.py`, which reads the threshold and limit from `analysis.yaml`. It is not Argo Rollouts itself, and the Prometheus query was never run against a live system.

## What it proves

- `analysis.yaml` samples every 30s, 5 times, succeeds while error rate is below 0.02 and allows `failureLimit: 2`.
- A good series is promoted after 5 samples.
- A series with one 5% spike is still promoted, because one failure is within the limit.
- The series `[0.001, 0.05, 0.08, 0.09, 0.2]` is aborted at sample 4, when the third failure exceeds the limit.

## Trade-offs

- The simulation mirrors the documented semantics but could drift from the real controller.
- The 2% threshold and 30s interval are example values, not tuned to any service.
- A rollback only reverts the release; data changes made by the bad version are not undone.

## When not to use it

- When metrics are too sparse or delayed to judge a release within a few minutes.
- For changes that cannot be rolled back safely, such as destructive migrations.
