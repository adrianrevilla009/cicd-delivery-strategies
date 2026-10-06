import yaml
docs = list(yaml.safe_load_all(open("virtualservice.yaml")))
vs = next(d for d in docs if d["kind"] == "VirtualService")
dr = next(d for d in docs if d["kind"] == "DestinationRule")
subsets = {s["name"] for s in dr["spec"]["subsets"]}
http = vs["spec"]["http"][0]
assert sum(r["weight"] for r in http["route"]) == 100
assert http["route"][0]["destination"]["subset"] in subsets
assert http["mirror"]["subset"] in subsets, "mirror subset undefined"
assert http["mirror"]["subset"] != http["route"][0]["destination"]["subset"], "mirror must target the new version"
assert 0 < http["mirrorPercentage"]["value"] <= 100
print("shadow ok")
