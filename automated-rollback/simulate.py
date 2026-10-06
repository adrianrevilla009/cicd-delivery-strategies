import yaml

spec = yaml.safe_load(open("analysis.yaml"))["spec"]["metrics"][0]
THRESHOLD = float(spec["successCondition"].split("<")[1])


def decide(samples):
    """Mimic Argo Rollouts: abort once failures exceed failureLimit."""
    failures = 0
    for i, v in enumerate(samples, 1):
        if not v < THRESHOLD:
            failures += 1
        if failures > spec["failureLimit"]:
            return "rollback", i
    return "promote", len(samples)


good = [0.001, 0.004, 0.002, 0.003, 0.001]
flaky = [0.001, 0.05, 0.002, 0.003, 0.001]  # one blip is tolerated
bad = [0.001, 0.05, 0.08, 0.09, 0.2]
assert decide(good) == ("promote", 5)
assert decide(flaky) == ("promote", 5)
assert decide(bad) == ("rollback", 4), decide(bad)
print("automated rollback ok: bad release aborted at sample 4")
