# shadow-traffic

An Istio `VirtualService` and `DestinationRule` that send all Orders traffic to v1 and mirror a share of it to v2, plus a check script.

## Goal

Show how a new version can see real production requests without its responses reaching users.

## Run it

```
python3 validate.py
```

Expected output: `shadow ok`

Not run end to end: Istio is not installed here, so no request was actually mirrored. `validate.py` only checks `virtualservice.yaml` offline.

## What it proves

- `virtualservice.yaml` routes 100% of traffic to subset `v1`, and `mirror` targets subset `v2`.
- `mirrorPercentage` is 20.0, so only a fifth of requests are copied.
- Both subsets are defined in the `DestinationRule` through `version` labels; the check fails if the mirror subset is undefined or equals the primary one.

## Trade-offs

- Mirrored requests are fire-and-forget, so v2 responses are never compared automatically; you need logs or metrics for that.
- Mirrored writes hit v2's dependencies; side effects such as payments or emails must be stubbed.
- Requires a service mesh, which adds operational weight.

## When not to use it

- For endpoints with non-idempotent side effects that cannot be isolated in the shadow version.
- When there is no mesh and the cost of installing one outweighs the benefit; a canary is simpler.
