"""Record every numeric check of one part in one JSON file.

Each check compares a value that one method computes with a value that another method computes.
The registry raises an error when a check fails, so a failure stops the script.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

DEFAULT_RELATIVE_TOLERANCE = 1.0e-9


class CheckRegistry:
    """Collect the numeric checks of one part and write them to a JSON file."""

    def __init__(self, part_name: str) -> None:
        """Create an empty registry for the part that the name selects."""
        self.part_name = part_name
        self.records: list[dict[str, Any]] = []

    def compare(
        self,
        name: str,
        computed: float,
        expected: float,
        tolerance: float = DEFAULT_RELATIVE_TOLERANCE,
        note: str = "",
    ) -> None:
        """Compare two numbers, record the pair, and raise an error on a failure.

        Args:
            name: Short label of the check.
            computed: Value that the first method computes.
            expected: Value that the second method computes.
            tolerance: Largest accepted relative difference of the two values.
            note: One sentence on the two methods that produce the two values.
        """
        difference = abs(float(computed) - float(expected))
        scale = max(abs(float(computed)), abs(float(expected)), 1.0e-12)
        relative_difference = difference / scale
        passed = bool(math.isfinite(difference)) and relative_difference <= tolerance
        self.records.append(
            {
                "part": self.part_name,
                "name": name,
                "computed": float(computed),
                "expected": float(expected),
                "difference": difference,
                "relative_difference": relative_difference,
                "tolerance": tolerance,
                "passed": passed,
                "note": note,
            }
        )
        print(
            f"[{'PASS' if passed else 'FAIL'}] {name}: computed={computed!r} "
            f"expected={expected!r} difference={difference:.3e} tolerance={tolerance:.1e}"
        )
        if not passed:
            raise AssertionError(f"check {name} failed: {computed!r} against {expected!r}")

    def compare_absolute(
        self, name: str, computed: float, expected: float, tolerance: float, note: str = ""
    ) -> None:
        """Compare two numbers with an absolute tolerance and record the pair.

        Args:
            name: Short label of the check.
            computed: Value that the first method computes.
            expected: Value that the second method computes.
            tolerance: Largest accepted absolute difference of the two values.
            note: One sentence on the two methods that produce the two values.
        """
        difference = abs(float(computed) - float(expected))
        passed = bool(math.isfinite(difference)) and difference <= tolerance
        self.records.append(
            {
                "part": self.part_name,
                "name": name,
                "computed": float(computed),
                "expected": float(expected),
                "difference": difference,
                "relative_difference": difference,
                "tolerance": tolerance,
                "passed": passed,
                "note": note,
            }
        )
        print(
            f"[{'PASS' if passed else 'FAIL'}] {name}: computed={computed!r} "
            f"expected={expected!r} difference={difference:.3e} absolute tolerance={tolerance:.1e}"
        )
        if not passed:
            raise AssertionError(f"check {name} failed: {computed!r} against {expected!r}")

    def compare_exact(self, name: str, computed: Any, expected: Any, note: str = "") -> None:
        """Compare two exact numbers and record the pair.

        Args:
            name: Short label of the check.
            computed: Exact value that the first method computes.
            expected: Exact value that the second method computes.
            note: One sentence on the two methods that produce the two values.
        """
        passed = computed == expected
        self.records.append(
            {
                "part": self.part_name,
                "name": name,
                "computed": str(computed),
                "expected": str(expected),
                "difference": 0.0 if passed else 1.0,
                "relative_difference": 0.0 if passed else 1.0,
                "tolerance": 0.0,
                "passed": bool(passed),
                "note": note,
            }
        )
        print(f"[{'PASS' if passed else 'FAIL'}] {name}: computed={computed} expected={expected}")
        if not passed:
            raise AssertionError(f"exact check {name} failed: {computed} against {expected}")

    def passed_count(self) -> int:
        """Return the number of recorded checks that pass."""
        return sum(1 for record in self.records if record["passed"])

    def write(self, path: Path) -> None:
        """Write the records and the count to one JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "part": self.part_name,
            "check_count": len(self.records),
            "passed_count": self.passed_count(),
            "records": self.records,
        }
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {len(self.records)} checks to {path}")


def write_values(path: Path, values: dict[str, Any]) -> None:
    """Write the named values of one part to one JSON file.

    Args:
        path: Target file of the values.
        values: Mapping from a name to a computed value or a formatted string.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(values, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(values)} values to {path}")


def latex_fraction(numerator: int, denominator: int) -> str:
    """Return the LaTeX source of one exact fraction.

    Args:
        numerator: Numerator of the fraction.
        denominator: Denominator of the fraction, not zero.
    """
    if denominator == 1:
        return str(numerator)
    return f"\\dfrac{{{numerator}}}{{{denominator}}}"
