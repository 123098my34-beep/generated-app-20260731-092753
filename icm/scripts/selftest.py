#!/usr/bin/env python3
"""ICM selftest — the one runnable check. Run: python scripts/selftest.py"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        failures.append(name)


required = [
    "CLAUDE.md",
    "CONTEXT.md",
    "stages/01-intake/CONTEXT.md",
    "stages/02-plan/CONTEXT.md",
    "stages/03-execute/CONTEXT.md",
    "stages/04-validate/CONTEXT.md",
    "references/forms.md",
    "references/plan-rules.md",
    "references/verify-rules.md",
    "references/anti-patterns.md",
    "skills/azr/SKILL.md",
    "skills/nomistake/SKILL.md",
    "source/job.md",
    "buffer/BUFFER.md",
]
missing = [p for p in required if not (ROOT / p).exists()]
check("required files", not missing, ", ".join(missing))

for stage in ["01-intake", "02-plan", "03-execute", "04-validate"]:
    text = (ROOT / "stages" / stage / "CONTEXT.md").read_text(encoding="utf-8")
    fm = re.search(r"^---\n(.*?)\n---", text, re.S)
    has_sections = all(
        re.search(rf"^## {s}", text, re.M) for s in ["Inputs", "Process", "Outputs"]
    )
    check(
        f"{stage} contract",
        fm is not None
        and has_sections
        and "inputs:" in fm.group(1)
        and "outputs:" in fm.group(1),
    )

l1 = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
forms = ["product", "service", "automation", "agent", "content", "analysis"]
check("routing forms", all(re.search(rf"\|\s*{f}\s*\|", l1) for f in forms))
check("routing target", "stages/01-intake" in l1)

buf = (ROOT / "buffer" / "BUFFER.md").read_text(encoding="utf-8")
check("buffer table", "| # | what | ran | result |" in buf)
azr = (ROOT / "skills" / "azr" / "SKILL.md").read_text(encoding="utf-8")
check("azr propose-before-solve", "Propose before solving" in azr)

print()
if failures:
    print(f"SELFTEST FAIL ({len(failures)}): {', '.join(failures)}")
    sys.exit(1)
print("SELFTEST ALL PASS")
