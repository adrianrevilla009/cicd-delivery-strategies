import hashlib
import json

FLAGS = json.load(open("flags.json"))


def bucket(flag, user):
    return int(hashlib.sha256(f"{flag}:{user}".encode()).hexdigest(), 16) % 100


def is_on(flag, user):
    f = FLAGS[flag]
    if f["kill_switch"] or not f["enabled"]:
        return False
    return user in f["allow"] or bucket(flag, user) < f["rollout_percent"]


if __name__ == "__main__":
    users = [f"user-{i}" for i in range(10000)]
    pct = sum(is_on("new-checkout", u) for u in users) / len(users) * 100
    assert abs(pct - 25) < 2, pct
    assert all(is_on("new-checkout", u) == is_on("new-checkout", u) for u in users[:100]), "unstable"
    assert is_on("new-checkout", "user-vip")
    FLAGS["new-checkout"]["kill_switch"] = True
    assert not is_on("new-checkout", "user-vip"), "kill switch must win"
    print(f"feature flag ok: {pct:.1f}% on")
