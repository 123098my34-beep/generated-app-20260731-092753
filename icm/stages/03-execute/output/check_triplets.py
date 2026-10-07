#!/usr/bin/env python3
"""AZR proposal check — runs BEFORE any marketplace search (stage 03, U2).
Checks T0/T1/T2 (synthetic deductions) and T4 (induction on prior exemplars).
The rule R is the one stated in stages/02-plan/output/triplets.md."""

import json
import subprocess
import sys
from pathlib import Path

FAILURES = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        FAILURES.append(name)


def R(c):
    """Selection rule. Returns (bool, failing_clauses)."""
    clauses = [
        ("demand", c.get("demand", 0) >= 7),
        ("gap", c.get("gap", 0) >= 6),
        ("alt_price", c.get("alt_price", 0) >= 25),
        ("one_time_fit", c.get("one_time_fit", 0) >= 7),
        ("build_days", c.get("build_days", 99) <= 3),
    ]
    failing = [n for n, ok in clauses if not ok]
    return (not failing), failing


# --- T0: saturated trap must REJECT (gap among failing clauses) ---
ok0, f0 = R({"demand": 9, "complaints": 8, "gap": 2, "alt_price": 15, "one_time_fit": 8, "build_days": 2})
check("T0 saturated trap REJECTED", (not ok0) and "gap" in f0, f"failing clauses: {f0}")

# --- T1: true only-option shape must SELECT ---
ok1, f1 = R({"demand": 8, "complaints": 8, "gap": 7, "alt_price": 59, "one_time_fit": 9, "build_days": 2})
check("T1 only-option shape SELECTED", ok1 and not f1)

# --- T2: popular-but-free trap must REJECT ---
ok2, f2 = R({"demand": 10, "complaints": 5, "gap": 3, "alt_price": 0, "one_time_fit": 5, "build_days": 1})
check("T2 free-alternative trap REJECTED", (not ok2) and set(f2) == {"gap", "alt_price", "one_time_fit"})

# --- T4: induction against prior run's verified exemplars (azr/i1_check.py) ---
EXEMPLARS = [
    {"id": "p134-checkout", "demand": 8, "gap": 7, "alt_price": 30, "one_time_fit": 10, "build_days": 1, "expect": "SELECT"},
    {"id": "photoshop-script", "demand": 9, "gap": 8, "alt_price": 25, "one_time_fit": 8, "build_days": 5, "expect": "REJECT"},
    {"id": "prompt-pack-flop", "demand": 6, "gap": 1, "alt_price": 0, "one_time_fit": 5, "build_days": 1, "expect": "REJECT"},
]
for e in EXEMPLARS:
    ok, f = R(e)
    got = "SELECT" if ok else "REJECT"
    check(f"T4 exemplar {e['id']}", got == e["expect"], f"got {got}, clauses {f}, expected {e['expect']}")

print()
if FAILURES:
    print(f"PROPOSAL CHECK FAIL ({len(FAILURES)}): {', '.join(FAILURES)}")
    sys.exit(1)
print("PROPOSAL CHECK ALL PASS — rule R is fit to search with")
sys.exit(0)
