"""Support module for the verification scripts of Problem 25.

The module holds one description of the solid E, two independent integration routes, one Monte Carlo
route, and a check recorder. Each part script compares a value from one route with a value from a
different route, so that no comparison has the same expression on both sides.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Sequence

import numpy as np
from scipy import integrate, special

Density = Callable[[float, float, float], float]

QUADRATURE_ABSOLUTE_TOLERANCE = 1.0e-11
QUADRATURE_RELATIVE_TOLERANCE = 1.0e-12
MONTE_CARLO_STANDARD_ERROR_FACTOR = 4.0
GEOMETRY_TOLERANCE = 1.0e-9
RELATIVE_DIFFERENCE_LIMIT = 1.0e-6
BOX_X_UPPER = 1.0
BOX_Y_UPPER = 3.0
BOX_Z_UPPER = 3.0
BOX_VOLUME = BOX_X_UPPER * BOX_Y_UPPER * BOX_Z_UPPER


def cylinder_height(y: float) -> float:
    """Return the upper bound of z at a fixed y, taken from the cylinder y^2 + z^2 = 9."""
    return math.sqrt(max(0.0, 9.0 - y * y))


def x_upper(y: float) -> float:
    """Return the upper bound of x at a fixed y, taken from the plane y = 3x."""
    return y / 3.0


def section_corners(y: float) -> list[tuple[float, float, float]]:
    """Return the four corners of the section of E at a fixed y, before any duplicate is removed."""
    width = x_upper(y)
    height = cylinder_height(y)
    return [(0.0, y, 0.0), (width, y, 0.0), (0.0, y, height), (width, y, height)]


def distinct_corners(y: float) -> list[tuple[float, float, float]]:
    """Return the section corners at a fixed y after duplicate points are removed."""
    kept: list[tuple[float, float, float]] = []
    for corner in section_corners(y):
        if not any(math.dist(corner, other) <= GEOMETRY_TOLERANCE for other in kept):
            kept.append(corner)
    return kept


def section_shape_from_distinct_corners(y: float) -> str:
    """Name the shape of the section at a fixed y by its count of distinct corners."""
    count = len(distinct_corners(y))
    return {4: "rectangle", 2: "segment", 1: "point"}.get(count, f"{count} points")


def section_shape_from_edge_lengths(y: float) -> str:
    """Name the shape of the section at a fixed y by its two edge lengths."""
    width = x_upper(y)
    height = cylinder_height(y)
    width_positive = width > GEOMETRY_TOLERANCE
    height_positive = height > GEOMETRY_TOLERANCE
    if width_positive and height_positive:
        return "rectangle"
    if width_positive or height_positive:
        return "segment"
    return "point"


def inside_solid(x: float, y: float, z: float) -> bool:
    """Return True when the point (x, y, z) satisfies the four surfaces and the first octant."""
    return (
        x >= 0.0
        and y >= 0.0
        and z >= 0.0
        and y * y + z * z <= 9.0 + 1.0e-12
        and 3.0 * x <= y + 1.0e-12
    )


def integrate_dx_dz_dy(density: Density) -> float:
    """Integrate over E in the order dx, then dz, then dy, with the bounds of the inequalities."""
    inner = lambda y, z: integrate.quad(  # noqa: E731
        lambda x: density(x, y, z), 0.0, x_upper(y),
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)[0]
    middle = lambda y: integrate.quad(  # noqa: E731
        lambda z: inner(y, z), 0.0, cylinder_height(y),
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)[0]
    return integrate.quad(
        middle, 0.0, BOX_Y_UPPER,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)[0]


def integrate_dz_dy_dx(density: Density) -> float:
    """Integrate over E in the order dz, then dy, then dx, with a different outer variable."""
    inner = lambda x, y: integrate.quad(  # noqa: E731
        lambda z: density(x, y, z), 0.0, cylinder_height(y),
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)[0]
    middle = lambda x: integrate.quad(  # noqa: E731
        lambda y: inner(x, y), 3.0 * x, BOX_Y_UPPER,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)[0]
    return integrate.quad(
        middle, 0.0, BOX_X_UPPER,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)[0]


def monte_carlo(density: Density, sample_count: int, seed: int) -> tuple[float, float]:
    """Estimate the integral over E by rejection sampling, and return the estimate and its error."""
    generator = np.random.default_rng(seed)
    x = generator.uniform(0.0, BOX_X_UPPER, sample_count)
    y = generator.uniform(0.0, BOX_Y_UPPER, sample_count)
    z = generator.uniform(0.0, BOX_Z_UPPER, sample_count)
    accepted = (y * y + z * z <= 9.0) & (3.0 * x <= y)
    weight = np.where(accepted, density(x, y, z), 0.0)
    estimate = BOX_VOLUME * float(np.mean(weight))
    standard_error = BOX_VOLUME * float(np.std(weight, ddof=1)) / math.sqrt(sample_count)
    return estimate, standard_error


@dataclass
class CheckRecord:
    """One comparison of a computed value with an expected value from a different method."""

    name: str
    computed: float
    expected: float
    tolerance: float
    unit: str = ""


@dataclass
class CheckLedger:
    """The collection of checks of one part script."""

    part: str
    records: list[CheckRecord] = field(default_factory=list)

    def add(self, name: str, computed: float, expected: float, tolerance: float,
            unit: str = "") -> None:
        """Record one check and print the two compared values and the verdict."""
        passed = abs(computed - expected) <= tolerance
        self.records.append(CheckRecord(name, computed, expected, tolerance, unit))
        print(f"CHECK {name}")
        print(f"  computed = {computed!r}")
        print(f"  expected = {expected!r}")
        print(f"  difference = {abs(computed - expected):.6e}  tolerance = {tolerance:.6e}"
              f"  {'PASS' if passed else 'FAIL'}")
        if not passed:
            raise AssertionError(f"check failed: {name}")

    def add_text(self, name: str, computed: str, expected: str) -> None:
        """Record one check of a text value, and print the two compared values."""
        passed = computed == expected
        print(f"CHECK {name}")
        print(f"  computed = {computed}")
        print(f"  expected = {expected}")
        print(f"  {'PASS' if passed else 'FAIL'}")
        if not passed:
            raise AssertionError(f"check failed: {name}")

    def summary(self) -> dict[str, object]:
        """Return the pass count and the rows of the ledger for the product page."""
        rows = [
            {
                "name": record.name,
                "computed": record.computed,
                "expected": record.expected,
                "difference": abs(record.computed - record.expected),
                "tolerance": record.tolerance,
            }
            for record in self.records
        ]
        return {"part": self.part, "count": len(rows), "rows": rows}


def write_results(path: Path, payload: dict[str, object]) -> None:
    """Write one JSON result file, so that the composed page reads every number from a print."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def scientific_latex(value: float) -> str:
    """Return one small number as a LaTeX product of a mantissa and a power of ten."""
    if value == 0.0:
        return "0"
    exponent = int(math.floor(math.log10(abs(value))))
    mantissa = value / (10.0 ** exponent)
    return f"{mantissa:.2f} \\times 10^{{{exponent}}}"


def rounded_three_decimals(value: float) -> str:
    """Return the value rounded to three decimal places with the round-half-up rule."""
    from decimal import ROUND_HALF_UP, Decimal

    return str(Decimal(repr(float(value))).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def exact_three_decimals(numerator: int, denominator: int) -> str:
    """Return the exact fraction rounded to three decimal places with the round-half-up rule."""
    from decimal import ROUND_HALF_UP, Decimal

    value = Decimal(numerator) / Decimal(denominator)
    return str(value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def add_difference(ledger: "CheckLedger", name: str, wrong: float, correct: float,
                   minimum_gap: float) -> None:
    """Record one check that a wrong candidate differs from the correct value by a stated gap."""
    gap = abs(wrong - correct)
    print(f"CHECK {name}")
    print(f"  wrong candidate = {wrong!r}")
    print(f"  correct value = {correct!r}")
    print(f"  gap = {gap:.6f}  required gap = {minimum_gap:.6f}"
          f"  {'PASS' if gap >= minimum_gap else 'FAIL'}")
    if gap < minimum_gap:
        raise AssertionError(f"check failed: {name}")
    ledger.records.append(CheckRecord(name, wrong, correct, minimum_gap))
