import yaml
wf = yaml.safe_load(open(".github/workflows/ci.yml"))
on = wf.get(True) or wf["on"]  # PyYAML parses the key `on` as True
assert on["push"]["branches"] == ["main"], "only trunk is pushed to"
assert on["pull_request"]["branches"] == ["main"], "PRs target trunk"
jobs = wf["jobs"]
assert jobs["build"]["uses"].startswith("adrianrevilla009/lab-workflows/"), "reuse lab-workflows"
assert jobs["deploy"]["needs"] == "build", "deploy only after CI"
assert "refs/heads/main" in jobs["deploy"]["if"], "deploy only from trunk"
assert not any("release/" in str(v) for v in on.values()), "no long-lived release branches"
print("trunk-based ok")
