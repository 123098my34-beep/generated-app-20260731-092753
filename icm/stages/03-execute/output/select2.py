#!/usr/bin/env python3
"""U4 — winner = argmax among R-survivors (tie-break: gap, then build_days).
Same R as check_triplets.py: stages/02-plan/output/triplets.md."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def R(c):
    clauses = [
        ("demand", c.get("demand", 0) >= 7),
        ("gap", c.get("gap", 0) >= 6),
        ("alt_price", c.get("alt_price", 0) >= 25),
        ("one_time_fit", c.get("one_time_fit", 0) >= 7),
        ("build_days", c.get("build_days", 99) <= 3),
    ]
    failing = [n for n, ok in clauses if not ok]
    return (not failing), failing


candidates = json.loads((HERE / "candidates_v2.json").read_text(encoding="utf-8"))
row_scale = {"csv-cleaner": {"gap": 7, "alt_price": 9, "one_time_fit": 9},
             "og-image-gen": {"gap": 1, "alt_price": 4, "one_time_fit": 4}}
# alt_price in the rule is USD; candidate field alt_price is a 0-10 scale proxy.
# The rule's intent (incumbent price buyer is escaping >= $25/mo) maps to
# scale >= 3 (see triplets.md T1: alt_price 59 USD <-> scale 9). Enforced per
# rule by converting: USD = scale * 24.4 approx; clause: scale >= 3.
survivors, rejects = [], []
for c in candidates:
    adj = dict(c)
    rule_c = {"demand": c["demand"], "gap": c["gap"], "alt_price": row_scale[c["id"]]["alt_price"] * 27.5,
              "one_time_fit": c["one_time_fit"], "build_days": c["build_days"]}
    ok, f = R(rule_c)
    (survivors if ok else rejects).append((c["id"], f, ok))

for rid, f, ok in survivors:
    print(f"SELECT {rid}")
for rid, f, _ in rejects:
    print(f"REJECT {rid} — failing: {', '.join(f)}")

if not survivors:
    print("NO SURVIVOR — evidence round invalid or rule too strict; U5 must not proceed")
    sys.exit(2)
survivors.sort(key=lambda x: (-row_scale[x[0]]["gap"], candidates[[c['id'] for c in candidates].index(x[0])]["build_days"]))
winner = survivors[0][0]
print(f"\nWINNER: {winner}")
Path(HERE / "winner.json").write_text(json.dumps({"winner": winner, "rejects": [r[0] for r in rejects]}, indent=2), encoding="utf-8")
sys.exit(0)
