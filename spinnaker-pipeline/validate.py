import json
p = json.load(open("pipeline.json"))
st = {s["refId"]: s for s in p["stages"]}
assert len(st) == len(p["stages"]), "duplicate refId"
for s in st.values():
    for r in s["requisiteStageRefIds"]:
        assert r in st, f"{s['name']}: unknown requisite {r}"
seen, order = set(), []


def visit(r, path=()):
    assert r not in path, "cycle"
    if r in seen:
        return
    for q in st[r]["requisiteStageRefIds"]:
        visit(q, path + (r,))
    seen.add(r)
    order.append(r)


for r in st:
    visit(r)
names = [st[r]["name"] for r in order]
prod = [i for i, r in enumerate(order) if st[r].get("account") == "prod"]
judge = next(i for i, r in enumerate(order) if st[r]["type"] == "manualJudgment")
assert all(judge < i for i in prod), "prod deploy before manual judgment"
assert p["triggers"], "pipeline needs a trigger"
print("spinnaker ok:", " -> ".join(names))
