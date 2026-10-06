# preview-environments

An Argo CD `ApplicationSet` that creates one environment per open pull request, a pinned kind cluster config and a check script.

## Goal

Show how every pull request gets its own namespace, deployed from its own commit and removed when the PR closes.

## Run it

```
python3 validate.py
```

Expected output: `preview environments ok`

Not run end to end: no kind cluster or Argo CD was started. `kind-config.yaml` (node image `kindest/node:v1.31.0`) was not used to create a cluster, and the ApplicationSet points at `adrianrevilla009/orders`, which was not contacted.

## What it proves

- The `pullRequest` generator in `applicationset.yaml` polls GitHub every 120s.
- Each PR becomes an application `orders-pr-{{number}}` in namespace `preview-{{number}}`, created with `CreateNamespace=true`.
- `targetRevision: '{{head_sha}}'` pins the preview to the PR commit.
- `automated` sync with `prune: true` and `selfHeal: true`; once the PR closes the application is removed.

## Trade-offs

- Each preview uses cluster resources; many open PRs need quotas.
- Polling at 120s means a delay before a new PR appears; webhooks would be faster.
- The source path `deploy/overlay` must exist in the application repo, and GitHub access needs a token not configured here.

## When not to use it

- For services whose dependencies (databases, third parties) cannot be created per PR.
- When PR volume is low and a shared staging environment is enough.
