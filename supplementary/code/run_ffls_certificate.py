#!/usr/bin/env python3
"""One-command FFLS integrity and witness verification checker.

Run from the package root or from any folder:
    python supplementary/code/run_ffls_certificate.py

The script performs exact rational substitution checks, checks rational continuum
witnesses, verifies that required branch-audit and continuum-certificate files
are present, checks canonical benchmark cardinalities, and validates
SHA256SUMS.txt when present. It is not a full branch-enumeration rerun.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import sys
import subprocess
from fractions import Fraction

# Make sibling module importable when run by path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from exact_direct_substitution_checks import run_all  # noqa: E402


def find_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "main.tex").exists() or (parent / "supplementary").exists():
            return parent
    return here.parents[2]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_manifest(root: Path) -> tuple[bool, str]:
    manifest = root / "SHA256SUMS.txt"
    if not manifest.exists():
        return False, "SHA256SUMS.txt not found"
    checked = 0
    failures = []
    for line in manifest.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        expected, rel = parts
        rel = rel.lstrip("* ")
        if rel in {"SHA256SUMS.txt", "./SHA256SUMS.txt"}:
            failures.append("manifest includes itself; self-hash is intentionally excluded")
            continue
        p = root / rel
        if not p.exists():
            failures.append(f"missing: {rel}")
            continue
        got = sha256(p)
        checked += 1
        if got.lower() != expected.lower():
            failures.append(f"hash mismatch: {rel}")
    if failures:
        return False, "; ".join(failures[:8])
    return True, f"{checked} listed files validated"


def required_files(root: Path) -> tuple[bool, str]:
    required = [
        "supplementary/audit_logs/Reserve_branch_audit_full.csv",
        "supplementary/audit_logs/Reserve_feasible_branches.csv",
        "supplementary/audit_logs/PV_reduced_branch_audit_full.csv",
        "supplementary/audit_logs/PV_row_feasible_branch_map.csv",
        "supplementary/audit_logs/PV_unique_singletons.csv",
        "supplementary/audit_logs/SWRO_continuum_certificate.md",
        "supplementary/audit_logs/Energy_Hub_continuum_certificate.md",
        "supplementary/certificates/direct_substitution_certificate.json",
        "supplementary/certificates/certificate_schema.json",
        "supplementary/certificates/certificate_summary.csv",
        "supplementary/published_example_replication/Malkawi2019_Example3_1/code/reproduce_example3_1_exact.py",
        "supplementary/published_example_replication/Malkawi2019_Example3_1/archival_outputs/published2019_example3_1_summary.json",
        "supplementary/published_example_replication/Malkawi2019_Example3_1/archival_outputs/published2019_example3_1_branch_audit_full.csv",
        "supplementary/published_example_replication/Babbar2013_Example4_1/code/audit_example4_1_exact.py",
        "supplementary/published_example_replication/Babbar2013_Example4_1/source_lock/source_transcription.json",
        "supplementary/published_example_replication/Babbar2013_Example4_1/archival_outputs/babbar2013_example4_1_summary.json",
        "supplementary/published_example_replication/Babbar2013_Example4_1/archival_outputs/babbar2013_example4_1_branch_audit_full.csv",
        "supplementary/published_example_replication/Babbar2013_Example4_1/proof_carrying/babbar2013_example4_1_pcec.jsonl",
        "supplementary/published_example_replication/Babbar2013_Example4_1/proof_carrying/babbar2013_example4_1_pcec_summary.json",
        "supplementary/published_example_replication/Babbar2013_Example4_1/proof_carrying/verify_pcec.py",
        "supplementary/proof_carrying/Reserve/reserve_main_benchmark_pcec.jsonl",
        "supplementary/proof_carrying/Reserve/reserve_main_benchmark_pcec_summary.json",
        "supplementary/proof_carrying/Reserve/verify_reserve_pcec.py",
    ]
    missing = [rel for rel in required if not (root / rel).exists()]
    return (not missing, "all required certificate/audit files are present" if not missing else "missing: " + ", ".join(missing))


def check_published_example_replication(root: Path) -> tuple[bool, str]:
    p = root / "supplementary/published_example_replication/Malkawi2019_Example3_1/archival_outputs/published2019_example3_1_summary.json"
    if not p.exists():
        return False, "published-example summary not found"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        counts = data["counts"]
    except Exception as exc:
        return False, f"cannot read published-example summary: {exc}"
    expected = {
        "equality_inconsistent": 27816,
        "inequality_infeasible": 37718,
        "singleton_branch_records": 2,
        "distinct_solutions_after_duplicate_collapse": 2,
        "positive_dimensional_survivors": 0,
    }
    bad = [f"{k}: expected {v}, got {counts.get(k)!r}" for k, v in expected.items() if counts.get(k) != v]
    subst = data.get("source_reported_solution_substitution", [])
    if len(subst) != 2 or not all(item.get("direct_substitution_pass") for item in subst):
        bad.append("source-reported solutions did not both pass exact direct substitution")
    if bad:
        return False, "; ".join(bad)
    return True, "published 2019 Example 3.1 replication matches exact 65,536-branch audit and two source solutions"


def check_independent_published_example_audit(root: Path) -> tuple[bool, str]:
    p = root / "supplementary/published_example_replication/Babbar2013_Example4_1/archival_outputs/babbar2013_example4_1_summary.json"
    if not p.exists():
        return False, "independent published-example audit summary not found"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        counts = data["counts"]
    except Exception as exc:
        return False, f"cannot read independent published-example audit: {exc}"
    expected = {
        "tested": 65536,
        "equality_inconsistent": 27816,
        "inequality_infeasible": 37718,
        "singleton_branch_records": 2,
        "distinct_solutions_after_duplicate_collapse": 2,
        "positive_dimensional_survivors": 0,
        "rank_three_equality_consistent_branches": 8,
    }
    bad = [f"{k}: expected {v}, got {counts.get(k)!r}" for k, v in expected.items() if counts.get(k) != v]
    source = data.get("source", {})
    if source.get("author_overlap_with_present_manuscript") is not False:
        bad.append("source author-overlap status is not false")
    source_subst = data.get("source_reported_solution_substitution", {})
    if not source_subst.get("direct_substitution_pass"):
        bad.append("source-displayed solution did not pass direct substitution")
    retained = data.get("all_retained_solution_substitutions", [])
    if len(retained) != 2 or not all(item.get("direct_substitution_pass") for item in retained):
        bad.append("retained singleton substitutions are incomplete or failed")
    extra = data.get("claim_boundary", {}).get("additional_solution_found", [])
    if len(extra) != 1 or not extra[0].get("direct_substitution_pass"):
        bad.append("second directly substituting singleton evidence is missing")
    gate = data.get("source_admissibility", {})
    gate_results = gate.get("results", [])
    if gate.get("unrestricted_singleton_count") != 2:
        bad.append("source gate does not record two unrestricted singletons")
    if gate.get("source_admissible_singleton_count") != 1 or gate.get("source_rejected_singleton_count") != 1:
        bad.append("source gate does not retain exactly one and reject exactly one singleton")
    if len(gate_results) != 2:
        bad.append("source-gate candidate records are incomplete")
    else:
        rejected = [item for item in gate_results if not item.get("source_nonnegative_gate_pass")]
        admitted = [item for item in gate_results if item.get("source_nonnegative_gate_pass")]
        if len(admitted) != 1 or len(rejected) != 1:
            bad.append("source-gate pass/fail split is incorrect")
        else:
            try:
                rejected_lower = Fraction(rejected[0]["lower_endpoints"][0])
            except Exception:
                bad.append("source-gate rejection witness is unreadable")
            else:
                if rejected_lower != Fraction(-1, 15) or rejected_lower >= 0:
                    bad.append("second singleton does not carry the expected -1/15 nonnegative-gate violation")
    if bad:
        return False, "; ".join(bad)
    return True, "Babbar et al. (2013) Example 4.1 confirms two unrestricted exact singletons; the second has lower endpoint -1/15 and fails the source nonnegative gate, leaving source-admissible k=1"


def check_proof_carrying_published_certificate(root: Path) -> tuple[bool, str]:
    checker = root / "supplementary/published_example_replication/Babbar2013_Example4_1/proof_carrying/verify_pcec.py"
    if not checker.exists():
        return False, "proof-carrying certificate checker not found"
    try:
        result = subprocess.run([sys.executable, str(checker)], cwd=root, text=True, capture_output=True, timeout=120)
    except Exception as exc:
        return False, f"cannot execute proof-carrying checker: {exc}"
    text = (result.stdout or "") + ("
" + result.stderr if result.stderr else "")
    if result.returncode != 0 or "Overall: PASS" not in text:
        detail = text.strip().replace("
", " | ")[:500]
        return False, f"proof-carrying certificate checker failed: {detail}"
    return True, "65,536 exact witnesses validated without RREF, LP, or candidate search"


def check_reserve_proof_carrying_certificate(root: Path) -> tuple[bool, str]:
    checker = root / "supplementary/proof_carrying/Reserve/verify_reserve_pcec.py"
    if not checker.exists():
        return False, "Reserve proof-carrying certificate checker not found"
    try:
        result = subprocess.run([sys.executable, str(checker)], cwd=root, text=True, capture_output=True, timeout=120)
    except Exception as exc:
        return False, f"cannot execute Reserve proof-carrying checker: {exc}"
    text = (result.stdout or "") + ("
" + result.stderr if result.stderr else "")
    if result.returncode != 0 or "Overall: PASS" not in text:
        detail = text.strip().replace("
", " | ")[:500]
        return False, f"Reserve proof-carrying checker failed: {detail}"
    required_tokens = ["65,536/65,536", "23,240", "42,291", "Singleton witnesses: 5", "Distinct singleton spread vectors: 5"]
    missing = [token for token in required_tokens if token not in text]
    if missing:
        return False, "Reserve checker missing expected evidence tokens: " + ", ".join(missing)
    return True, "65,536 main Reserve witnesses validated without RREF, LP, or candidate search"


def load_certificate_summary(root: Path) -> tuple[bool, str]:
    p = root / "supplementary/certificates/certificate_summary.csv"
    expected = {
        "Critical-facility reserve": "5",
        "PV-BESS-EV": "2",
        "SWRO": "infinity",
        "Energy hub": "infinity",
    }
    if not p.exists():
        return False, "certificate_summary.csv not found"
    seen = {}
    with p.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            seen[row.get("benchmark", "")] = row.get("k", "")
    failures = []
    for name, k in expected.items():
        if seen.get(name) != k:
            failures.append(f"{name}: expected k={k}, got {seen.get(name)!r}")
    return (not failures, "canonical k values match: k_R=5, k_EV=2, k_D=infinity, k_H=infinity" if not failures else "; ".join(failures))


def main() -> int:
    root = find_root()
    print(f"FFLS integrity/witness root: {root}")
    checks = []

    exact_results = run_all()
    for r in exact_results:
        checks.append((r.name, r.passed, r.detail))

    ok, detail = required_files(root)
    checks.append(("Required audit/certificate files", ok, detail))

    ok, detail = load_certificate_summary(root)
    checks.append(("Canonical cardinality summary", ok, detail))

    ok, detail = check_published_example_replication(root)
    checks.append(("Published-example replication", ok, detail))

    ok, detail = check_independent_published_example_audit(root)
    checks.append(("Independent published-source audit", ok, detail))

    ok, detail = check_proof_carrying_published_certificate(root)
    checks.append(("Proof-carrying published-source certificate", ok, detail))

    ok, detail = check_reserve_proof_carrying_certificate(root)
    checks.append(("Proof-carrying main Reserve certificate", ok, detail))

    ok, detail = validate_manifest(root)
    checks.append(("SHA-256 manifest", ok, detail))

    print("
Certificate checks:")
    for name, ok, detail in checks:
        print(f"- {'PASS' if ok else 'FAIL'}: {name}: {detail}")

    all_ok = all(ok for _, ok, _ in checks)
    print("
Overall: " + ("PASS" if all_ok else "FAIL"))
    print("Final benchmark statuses: k_R=5, k_EV=2, k_D=infinity, k_H=infinity")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
