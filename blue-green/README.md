# blue-green

An Argo Rollouts blue/green `Rollout` for Orders with separate active and preview Services, plus a script that checks the wiring.

## Goal

Show how a new version is deployed next to the live one, reachable through a preview Service, and only switched over when someone promotes it.

## Run it

```
python3 validate.py
```

Expected output: `blue-green ok`

Not run end to end: the manifest was never applied to a cluster, so no Argo Rollouts controller has acted on it. `validate.py` only parses `rollout.yaml` and asserts its structure.

## What it proves

- `rollout.yaml` defines `orders-active` and `orders-preview` as two distinct Services, both referenced by the `blueGreen` strategy.
- `autoPromotionEnabled: false` means the new ReplicaSet gets no production traffic until a manual promote.
- The image is `ghcr.io/example/orders:1.1.0`, pinned and not `latest`; `validate.py` fails otherwise.
- The old ReplicaSet is kept for `scaleDownDelaySeconds: 300`, so a rollback in that window is instant.

## Trade-offs

- Two full copies (3 replicas each) run during a release, doubling resource use.
- Both Services select `app: orders`; the Argo Rollouts controller adds the revision hash to each at runtime, which the offline check cannot see.
- The check validates structure, not behaviour of the controller.

## When not to use it

- When the database schema change is not backward compatible; both versions must work against the same data.
- On small clusters where doubling capacity is not affordable; a rolling update or canary is cheaper.
