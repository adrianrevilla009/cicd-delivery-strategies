# cicd-delivery-strategies

Eight small examples of release strategies (blue/green, canary, shadow traffic, pipelines, feature flags, rollback, trunk-based delivery, preview environments) as Kubernetes, Argo, Istio and Spinnaker config plus offline checks. They all use the same tiny Orders service as the subject.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`blue-green`](./blue-green) | Argo Rollouts blue/green with active and preview Services and manual promotion | `python3 validate.py` |
| [`canary-argo-rollouts`](./canary-argo-rollouts) | Canary steps 10, 50, 100 with a Prometheus analysis gate | `python3 validate.py` |
| [`shadow-traffic`](./shadow-traffic) | Istio mirroring of 20% of requests to a new version | `python3 validate.py` |
| [`spinnaker-pipeline`](./spinnaker-pipeline) | Spinnaker pipeline JSON: staging, smoke tests, approval, prod | `python3 validate.py` |
| [`feature-flag-rollout`](./feature-flag-rollout) | Percentage flag with allow list and kill switch | `python3 rollout.py` |
| [`automated-rollback`](./automated-rollback) | Failure-limit rollback logic simulated against an analysis template | `python3 simulate.py` |
| [`trunk-based-delivery`](./trunk-based-delivery) | GitHub Actions workflow that builds on PRs and deploys only from `main` | `python3 validate.py` |
| [`preview-environments`](./preview-environments) | Argo CD ApplicationSet creating one namespace per pull request | `python3 validate.py` |

## Prerequisites

- Python 3.10+ with PyYAML (`pip install pyyaml`).
- To apply the manifests for real (not needed for the checks): a Kubernetes cluster such as kind, Argo Rollouts, Istio, Argo CD or Spinnaker as relevant.

## How to read it

Start with `blue-green`, then `canary-argo-rollouts` and `automated-rollback`, which build on each other. Every folder is standalone and its check runs offline in under a second. None of the manifests were applied to a cluster.
