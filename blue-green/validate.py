import yaml
docs = list(yaml.safe_load_all(open("rollout.yaml")))
ro = next(d for d in docs if d["kind"] == "Rollout")
bg = ro["spec"]["strategy"]["blueGreen"]
svcs = {d["metadata"]["name"] for d in docs if d["kind"] == "Service"}
assert bg["activeService"] in svcs and bg["previewService"] in svcs, "services missing"
assert bg["activeService"] != bg["previewService"], "active and preview must differ"
assert bg["autoPromotionEnabled"] is False, "promotion must be manual"
image = ro["spec"]["template"]["spec"]["containers"][0]["image"]
assert ":" in image.split("/")[-1] and not image.endswith(":latest"), "image must be pinned"
print("blue-green ok")
