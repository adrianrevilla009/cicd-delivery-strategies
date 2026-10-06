import yaml
docs = list(yaml.safe_load_all(open("rollout.yaml")))
ro = next(d for d in docs if d["kind"] == "Rollout")
at = {d["metadata"]["name"]: d for d in docs if d["kind"] == "AnalysisTemplate"}
steps = ro["spec"]["strategy"]["canary"]["steps"]
weights = [s["setWeight"] for s in steps if "setWeight" in s]
assert weights == sorted(weights) and weights[-1] == 100, "weights must rise to 100"
used = [t["templateName"] for s in steps if "analysis" in s for t in s["analysis"]["templates"]]
assert used and all(u in at for u in used), "analysis step must reference an existing template"
first_analysis = next(i for i, s in enumerate(steps) if "analysis" in s)
first_50 = next(i for i, s in enumerate(steps) if s.get("setWeight", 0) >= 50)
assert first_analysis < first_50, "analysis must gate the big weight jump"
m = at[used[0]]["spec"]["metrics"][0]
assert m["failureLimit"] >= 0 and "successCondition" in m
print("canary ok:", weights)
