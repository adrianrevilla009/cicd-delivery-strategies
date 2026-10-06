# feature-flag-rollout

A small percentage-rollout flag evaluator in Python with its flag file `flags.json`.

## Goal

Show how a feature can be released to a stable share of users, with an allow list and a kill switch, without redeploying.

## Run it

```
python3 rollout.py
```

Expected output, with the percentage computed over 10,000 synthetic users: `feature flag ok: 24.7% on`

## What it proves

- `flags.json` sets `new-checkout` to 25% rollout; `rollout.py` hashes `flag:user` with SHA-256 into a bucket 0-99, and 24.7% of the 10,000 users land inside it.
- The same user always gets the same answer, checked for the first 100 users.
- `user-vip` in the `allow` list is on regardless of bucket.
- Setting `kill_switch` to true turns the flag off even for `user-vip`.

## Trade-offs

- The flag file is read once at import; a real system needs a store and a refresh path.
- Hashing by flag and user gives independent buckets per flag, but raising 25% to 50% keeps earlier users on, which is wanted, and there is no audit trail.
- No targeting beyond the allow list and no metrics on exposure.

## When not to use it

- When a hosted flag service or OpenFeature provider is already in place.
- For flags that need per-segment rules, scheduling or experiments.
