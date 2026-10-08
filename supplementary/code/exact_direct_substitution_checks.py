#!/usr/bin/env python3
"""Exact rational direct-substitution checks for the FFLS certified benchmarks.

This script verifies the displayed finite benchmark envelopes and rational
continuum spot checks under the declared lower-modal-upper endpoint/min-max
triangular product. It is intentionally dependency-free and uses Python's
fractions.Fraction for exact arithmetic.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from typing import Iterable, List, Sequence, Tuple

Tri = Tuple[F, F, F]
Matrix = List[List[Tri]]
Vector = List[Tri]


def tri(a: int | str | F, b: int | str | F, c: int | str | F) -> Tri:
    return (F(a), F(b), F(c))


def tri_mul(a: Tri, x: Tri) -> Tri:
    al, am, au = a
    xl, xm, xu = x
    endpoints = (al * xl, al * xu, au * xl, au * xu)
    return (min(endpoints), am * xm, max(endpoints))


def tri_add(values: Iterable[Tri]) -> Tri:
    vals = list(values)
    return tuple(sum(v[i] for v in vals) for i in range(3))  # type: ignore[return-value]


def matvec(A: Matrix, X: Vector) -> Vector:
    return [tri_add(tri_mul(a, x) for a, x in zip(row, X)) for row in A]


def format_tri(t: Tri) -> str:
    def f(x: F) -> str:
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return "(" + ", ".join(f(x) for x in t) + ")"


def format_vec(v: Vector) -> str:
    return "[" + ", ".join(format_tri(t) for t in v) + "]"


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


def reserve_checks() -> CheckResult:
    A: Matrix = [
        [tri(-3, 1, 8), tri(-1, 5, 6)],
        [tri(3, 3, 5), tri(-1, 3, 4)],
    ]
    B: Vector = [tri(-50, 4, 74), tri(-32, 0, 48)]
    Xs: List[Vector] = [
        [tri(F(-4, 3), -1, 4), tri(F(-19, 3), 1, 7)],
        [tri(-4, -1, F(4, 3)), tri(-3, 1, F(31, 3))],
        [tri(-4, -1, 4), tri(-3, 1, 7)],
        [tri(F(-118, 27), -1, F(40, 27)), tri(F(-203, 81), 1, F(274, 27))],
        [tri(-5, -1, 4), tri(F(-5, 3), 1, 7)],
    ]
    failures = []
    for idx, X in enumerate(Xs, 1):
        lhs = matvec(A, X)
        if lhs != B:
            failures.append(f"R{idx}: got {format_vec(lhs)}, expected {format_vec(B)}")
    return CheckResult(
        "Critical-facility reserve exact substitution",
        not failures,
        "5/5 displayed envelopes match exactly" if not failures else "; ".join(failures),
    )


def pv_checks() -> CheckResult:
    A: Matrix = [
        [tri(-2, 3, 4), tri(-2, 2, 3), tri(1, 2, 3)],
        [tri(1, 2, 2), tri(4, 4, 5), tri(1, 2, 3)],
        [tri(-1, 2, 3), tri(-4, 2, 3), tri(0, 0, 0)],
    ]
    B: Vector = [tri(-12, 12, 23), tri(-13, 12, 23), tri(-11, 6, 18)]
    Xs: List[Vector] = [
        [tri(1, 2, 2), tri(-3, 1, 2), tri(1, 2, 3)],
        [tri(F(3, 10), 2, F(11, 5)), tri(F(-57, 20), 1, F(11, 5)), tri(F(19, 20), 2, F(38, 15))],
    ]
    failures = []
    for idx, X in enumerate(Xs, 1):
        lhs = matvec(A, X)
        if lhs != B:
            failures.append(f"PV{idx}: got {format_vec(lhs)}, expected {format_vec(B)}")
    return CheckResult(
        "PV-BESS-EV exact substitution",
        not failures,
        "2/2 displayed envelopes match exactly" if not failures else "; ".join(failures),
    )


def swro_spot_checks() -> CheckResult:
    A: Matrix = [
        [tri(-4, -4, -3), tri(0, 2, 3)],
        [tri(2, 2, 3), tri(-1, 0, 3)],
    ]
    B: Vector = [tri(-27, -14, 12), tri(-12, 6, 19)]
    samples = [F(0), F(1, 2), F(1)]
    failures = []
    for t in samples:
        X = [tri(-3, 3, 6), tri(-1, -1, -1 + t)]
        lhs = matvec(A, X)
        if lhs != B:
            failures.append(f"t={t}: got {format_vec(lhs)}, expected {format_vec(B)}")
    return CheckResult(
        "SWRO continuum rational spot checks",
        not failures,
        "t = 0, 1/2, 1 match exactly; continuum inclusion is documented in the supplied certificate" if not failures else "; ".join(failures),
    )


def energy_hub_spot_checks() -> CheckResult:
    A: Matrix = [
        [tri(1, 2, 3), tri(2, 3, 4), tri(3, 4, 5)],
        [tri(2, 4, 6), tri(4, 6, 8), tri(6, 8, 10)],
        [tri(2, 5, 7), tri(3, 6, 8), tri(4, 7, 9)],
    ]
    B: Vector = [tri(8, 34, 82), tri(16, 68, 164), tri(12, 70, 166)]
    samples = [F(0), F(1, 2), F(1)]
    failures = []
    for lam in samples:
        X = [tri(1 + lam, 5, 8), tri(2 - 2 * lam, 4, 7), tri(1 + lam, 3, 6)]
        lhs = matvec(A, X)
        if lhs != B:
            failures.append(f"lambda={lam}: got {format_vec(lhs)}, expected {format_vec(B)}")
    return CheckResult(
        "Energy-hub continuum rational spot checks",
        not failures,
        "lambda = 0, 1/2, 1 match exactly; continuum inclusion is documented in the supplied certificate" if not failures else "; ".join(failures),
    )


def run_all() -> List[CheckResult]:
    return [reserve_checks(), pv_checks(), swro_spot_checks(), energy_hub_spot_checks()]


if __name__ == "__main__":
    results = run_all()
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status}: {result.name} - {result.detail}")
    raise SystemExit(0 if all(r.passed for r in results) else 1)
