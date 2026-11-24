"""Recording of the numeric checks of one tutorial part.

One CheckRecorder compares a value that one method computes with a value that a
different method computes, keeps every comparison, and writes one JSON record
and one text table under code/outputs/.
"""

from __future__ import annotations

import json
from pathlib import Path


def format_number(value: float, digits: int = 9) -> str:
    """Return a decimal text of one number with a fixed count of digits.

    Args:
        value: The number to format.
        digits: Count of digits after the decimal point.

    Returns:
        The text of the number.
    """
    return f"{value:.{digits}f}"


class CheckRecorder:
    """Compare computed values with expected values and store the record."""

    def __init__(self, part_name: str, output_directory: Path) -> None:
        """Store the name of the part and the directory of its record.

        Args:
            part_name: Name of the part, such as "part1".
            output_directory: Directory that receives the JSON record and the table.
        """
        self.part_name = part_name
        self.output_directory = output_directory
        self.checks: list[dict] = []
        self.display: dict[str, str] = {}

    def compare(self, name: str, computed: float, expected: float, tolerance: float, reason: str) -> None:
        """Compare two values with an absolute tolerance and record the comparison.

        Args:
            name: Name of the check.
            computed: Value that the first method computes.
            expected: Value that the second method computes.
            tolerance: Largest accepted absolute difference.
            reason: One sentence that names the two methods.

        Raises:
            AssertionError: The difference is larger than the tolerance.
        """
        difference = abs(float(computed) - float(expected))
        passed = difference <= tolerance
        self.checks.append(
            {
                "name": name,
                "computed": float(computed),
                "expected": float(expected),
                "difference": difference,
                "tolerance": float(tolerance),
                "reason": reason,
                "passed": bool(passed),
            }
        )
        print(
            f"CHECK {name}: computed={computed:.12g} expected={expected:.12g} "
            f"difference={difference:.3g} tolerance={tolerance:.3g} {'PASS' if passed else 'FAIL'}"
        )
        if not passed:
            raise AssertionError(f"{name}: difference {difference!r} exceeds tolerance {tolerance!r}")

    def compare_ratio(self, name: str, numerator: float, denominator: float, limit: float, reason: str) -> None:
        """Compare two positive values with a relative tolerance and record the comparison.

        Args:
            name: Name of the check.
            numerator: Value that the first method computes.
            denominator: Value that the second method computes.
            limit: Largest accepted relative difference.
            reason: One sentence that names the two methods.

        Raises:
            AssertionError: The relative difference is larger than the limit.
        """
        relative = abs(float(numerator) - float(denominator)) / abs(float(denominator))
        passed = relative <= limit
        self.checks.append(
            {
                "name": name,
                "computed": float(numerator),
                "expected": float(denominator),
                "relative_difference": relative,
                "tolerance": float(limit),
                "reason": reason,
                "passed": bool(passed),
            }
        )
        print(
            f"CHECK {name}: computed={numerator:.12g} expected={denominator:.12g} "
            f"relative={relative:.3g} limit={limit:.3g} {'PASS' if passed else 'FAIL'}"
        )
        if not passed:
            raise AssertionError(f"{name}: relative difference {relative!r} exceeds limit {limit!r}")

    def compare_bound(self, name: str, value: float, bound: float, reason: str) -> None:
        """Check that one value does not exceed one bound and record the comparison.

        Args:
            name: Name of the check.
            value: Value that a method computes.
            bound: Largest accepted value.
            reason: One sentence that names the method and the source of the bound.

        Raises:
            AssertionError: The value exceeds the bound.
        """
        passed = float(value) <= float(bound)
        self.checks.append(
            {
                "name": name,
                "computed": float(value),
                "bound": float(bound),
                "reason": reason,
                "passed": bool(passed),
            }
        )
        print(f"CHECK {name}: computed={value:.12g} bound={bound:.12g} {'PASS' if passed else 'FAIL'}")
        if not passed:
            raise AssertionError(f"{name}: value {value!r} exceeds bound {bound!r}")

    def set_display(self, key: str, text: str) -> None:
        """Store one text that the composed page reads.

        Args:
            key: Placeholder key without the braces.
            text: Text of the value, already formatted.
        """
        self.display[key] = text

    def save(self) -> None:
        """Write the JSON record and the text table of the part.

        Raises:
            AssertionError: One stored check did not pass.
        """
        failed = [check for check in self.checks if not check["passed"]]
        if failed:
            raise AssertionError(f"{self.part_name}: {len(failed)} checks did not pass")
        self.output_directory.mkdir(parents=True, exist_ok=True)
        record = {
            "part": self.part_name,
            "check_count": len(self.checks),
            "passed_count": len(self.checks) - len(failed),
            "checks": self.checks,
            "display": self.display,
        }
        json_path = self.output_directory / f"{self.part_name}_summary.json"
        json_path.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
        lines = [f"{self.part_name} checks"]
        lines.append(f"{'check':44s} {'computed':>16s} {'expected':>16s} {'tolerance':>12s} result")
        for check in self.checks:
            expected = check.get("expected", check.get("bound"))
            tolerance = check.get("tolerance", 0.0)
            lines.append(
                f"{check['name']:44s} {check['computed']:16.9f} {float(expected):16.9f} "
                f"{float(tolerance):12.2e} {'pass' if check['passed'] else 'fail'}"
            )
        lines.append(f"{len(self.checks)} checks, {len(self.checks) - len(failed)} pass")
        (self.output_directory / f"{self.part_name}_table.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{self.part_name}: {len(self.checks)} checks, {len(self.checks) - len(failed)} pass")
