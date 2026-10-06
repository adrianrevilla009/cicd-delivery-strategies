import yaml
kind = yaml.safe_load(open("kind-config.yaml"))
assert kind["nodes"][0]["image"].split(":")[1].startswith("v1."), "pin the node image"
spec = yaml.safe_load(open("applicationset.yaml"))["spec"]
assert "pullRequest" in spec["generators"][0]
t = spec["template"]
assert "{{number}}" in t["metadata"]["name"] and "{{number}}" in t["spec"]["destination"]["namespace"], "per-PR names"
assert t["spec"]["source"]["targetRevision"] == "{{head_sha}}", "pin to the PR commit"
assert t["spec"]["syncPolicy"]["automated"]["prune"] is True, "prune so closed PRs are cleaned up"
print("preview environments ok")
