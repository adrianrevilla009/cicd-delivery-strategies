# canary-argo-rollouts

An Argo Rollouts canary for Orders with weights 10, 50 and 100 percent and a Prometheus-backed `AnalysisTemplate`, plus a structural check.

## Goal

Show how a release is shifted gradually and how a success-rate metric gates the larger jump.

## Run it

```
python3 validate.py
```

Expected output: `canary ok: [10, 50, 100]`

Not run end to end: there is no cluster or Prometheus here, so the analysis query was never executed. `validate.py` only checks `rollout.yaml` offline.

## What it proves

- The steps in `rollout.yaml` are `setWeight` 10, pause 2m, analysis, `setWeight` 50, pause 5m, `setWeight` 100; weights only go up and end at 100.
- The `analysis` step references the `success-rate` template defined in the same file, and it sits before the 50% step.
- The template runs every 1m, 3 times, tolerates 1 failure (`failureLimit: 1`) and requires `result[0] >= 0.99`.
- The Prometheus query divides non-5xx request rate by total request rate for `app="orders"`.

## Trade-offs

- The Prometheus address `http://prometheus.monitoring:9090` and the `http_requests_total` metric are assumptions about the cluster.
- With 5 replicas, 10% rounds to one pod unless a traffic router is configured; none is, so weights are approximated by replica counts.
- Three one-minute samples is a short window and can miss slow regressions.

## When not to use it

- For services with too little traffic for a 99% success rate to be statistically meaningful.
- When there is no metrics backend; an unanswerable query fails the analysis.
