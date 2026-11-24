"""Shared geometry of the wedge and the record of the checks of one part.

The wedge is the set of points that satisfy four conditions: the point is in the first
octant, the point is inside the cylinder y^2 + z^2 = 1, the point is on the side y >= x of
the plane y = x, and the point is on the side x <= 1 of the plane x = 1.

The module holds two independent descriptions of that set, the height of the cylinder, the
area of one slice, and a recorder that prints each check and writes the record of a part.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Callable

from scipy.integrate import quad

CODE_DIRECTORY = Path(__file__).resolve().parent
"""Directory of the product code."""

OUTPUT_DIRECTORY = CODE_DIRECTORY / "outputs"
"""Directory of the JSON records of the parts."""

FIGURE_DIRECTORY = CODE_DIRECTORY / "figures"
"""Directory of the rendered figures."""

TOLERANCE = 1.0e-9
"""Absolute tolerance of a comparison of two computed values."""


def cylinder_height(y: float) -> float:
    """Return the largest height z of the cylinder y^2 + z^2 = 1 at the coordinate y."""
    return math.sqrt(max(0.0, 1.0 - y * y))


def inside_by_limits(x: float, y: float, z: float) -> bool:
    """Return True when the point satisfies the wedges as three stacked intervals.

    The intervals are 0 <= y <= 1, 0 <= x <= y, and 0 <= z <= sqrt(1 - y^2).  The bound of z
    comes from the cylinder, and the bound of x comes from the plane y = x.
    """
    if not (0.0 <= y <= 1.0):
        return False
    if not (0.0 <= x <= y):
        return False
    return 0.0 <= z <= cylinder_height(y)


def inside_by_surfaces(x: float, y: float, z: float) -> bool:
    """Return True when the point is inside each of the four bounding surfaces.

    The test uses the four surface expressions directly: the first octant, the quadratic form
    y^2 + z^2 <= 1, the difference y - x >= 0, and 1 - x >= 0.  It shares no square root and no
    chained comparison with :func:`inside_by_limits`.
    """
    if min(x, y, z) < 0.0:
        return False
    if y * y + z * z > 1.0:
        return False
    return (y - x) >= 0.0 and (1.0 - x) >= 0.0


def slice_area_exact(z: float) -> float:
    """Return the area of the horizontal slice at height z as the closed form (1 - z^2) / 2.

    At height z the slice holds 0 <= y <= sqrt(1 - z^2) and 0 <= x <= y, so its area is the
    integral of y over that interval.
    """
    height = cylinder_height(z)
    return height * height / 2.0


def slice_area_quadrature(z: float) -> float:
    """Return the area of the horizontal slice at height z by adaptive quadrature of y."""
    value, _ = quad(lambda y: y, 0.0, cylinder_height(z), limit=200,
                    epsabs=1.0e-14, epsrel=1.0e-13)
    return value


def slice_length_at_height(z: float) -> float:
    """Return the length sqrt(1 - z^2) of the slice at height z along the y direction."""
    return cylinder_height(z)


def integrate(function: Callable[[float], float], low: float, high: float) -> float:
    """Return the adaptive quadrature of one function on one interval."""
    value, _ = quad(function, low, high, limit=400, epsabs=1.0e-14, epsrel=1.0e-13)
    return value


class Recorder:
    """Print each check, keep its record, and write the JSON record of one part."""

    def __init__(self, part: int) -> None:
        """Start the record of one part.

        Args:
            part: Number of the part.
        """
        self.part = part
        self.checks: list[dict[str, object]] = []
        self.values: dict[str, str] = {}
        self.passed = 0

    def record(self, name: str, computed: float, expected: float,
               tolerance: float = TOLERANCE) -> float:
        """Compare a value of one method with a value of a different method."""
        if computed is expected:
            raise AssertionError(f"{name}: the two sides are the same object")
        difference = abs(computed - expected)
        passed = math.isfinite(difference) and difference <= tolerance
        self.checks.append({"name": name, "computed": computed, "expected": expected,
                            "difference": difference, "tolerance": tolerance,
                            "passed": passed})
        self.passed += int(passed)
        print(f"{name}: computed {computed:.12f} expected {expected:.12f} "
              f"difference {difference:.3e} tolerance {tolerance:.1e} "
              f"{'PASS' if passed else 'FAIL'}")
        if not passed:
            raise AssertionError(f"{name} failed with difference {difference:.3e}")
        return computed

    def record_text(self, name: str, computed: str, expected: str) -> str:
        """Compare two strings that two different methods produced."""
        passed = computed == expected
        self.checks.append({"name": name, "computed": computed, "expected": expected,
                            "difference": 0.0 if passed else 1.0,
                            "tolerance": 0.0, "passed": passed})
        self.passed += int(passed)
        print(f"{name}: computed {computed} expected {expected} "
              f"{'PASS' if passed else 'FAIL'}")
        if not passed:
            raise AssertionError(f"{name} failed: {computed} against {expected}")
        return computed

    def publish(self, key: str, value: str) -> None:
        """Store one string that the page interpolates."""
        self.values[key] = value

    def write(self) -> None:
        """Write the values and the checks of the part to the output directory."""
        OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
        values_path = OUTPUT_DIRECTORY / f"part{self.part}_values.json"
        checks_path = OUTPUT_DIRECTORY / f"part{self.part}_checks.json"
        values_path.write_text(json.dumps(self.values, indent=2) + "\n",
                               encoding="utf-8", newline="\n")
        checks_path.write_text(
            json.dumps({"check_count": len(self.checks), "passed_count": self.passed,
                        "checks": self.checks}, indent=2) + "\n",
            encoding="utf-8", newline="\n")
        print(f"part {self.part}: {self.passed} of {len(self.checks)} checks pass")
