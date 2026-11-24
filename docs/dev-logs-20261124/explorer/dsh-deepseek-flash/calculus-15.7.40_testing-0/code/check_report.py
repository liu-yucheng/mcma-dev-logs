"""Record, print, and store the checks of one part of the tutorial.

Every check compares a value that one method computes with a value that a different method computes. The module
refuses a check whose two methods carry the same name, because such a check cannot fail.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

OUTPUT_DIRECTORY: Path = Path(__file__).resolve().parent / "outputs"
"""The directory that holds the machine-readable record of each part."""

RANDOM_SEED: int = 20261123
"""The seed of every random sample of the tutorial."""


@dataclass
class Check:
    """One comparison of a computed value against an independently computed value.

    Attributes:
        name: The short name of the check.
        computed: The value of the first method, as printed text.
        expected: The value of the second method, as printed text.
        tolerance: The tolerance of the comparison, as printed text.
        first_method: The name of the method that produced the computed value.
        second_method: The name of the method that produced the expected value.
        passed: True when the two values agree inside the tolerance.
    """

    name: str
    computed: str
    expected: str
    tolerance: str
    first_method: str
    second_method: str
    passed: bool


@dataclass
class PartRecord:
    """The record of one part: its checks, its printed values, and its summary.

    Attributes:
        part_number: The number of the part.
        part_title: The title of the part.
        checks: The list of checks of the part.
        values: The printed values that the composed page interpolates.
        pass_count: The number of checks that passed.
        fail_count: The number of checks that failed.
    """

    part_number: int
    part_title: str
    checks: list[Check] = field(default_factory=list)
    values: dict[str, str] = field(default_factory=dict)
    pass_count: int = 0
    fail_count: int = 0


class CheckRecorder:
    """Collect the checks of one part, print each one, and write the record to a JSON file."""

    def __init__(self, part_number: int, part_title: str) -> None:
        """Start the record of one part.

        Args:
            part_number: The number of the part.
            part_title: The title of the part.
        """
        self.record = PartRecord(part_number=part_number, part_title=part_title)

    def set_value(self, key: str, text: str) -> None:
        """Store one printed value for the composed page.

        Args:
            key: The name of the value.
            text: The text of the value, already in page form.
        """
        if key in self.record.values:
            raise KeyError(f"the value '{key}' is already set")
        self.record.values[key] = text

    def note(self, text: str) -> None:
        """Print one informational line that is not a check.

        Args:
            text: The line to print.
        """
        print(f"NOTE  {text}")

    def _store(self, check: Check) -> bool:
        self.record.checks.append(check)
        if check.passed:
            self.record.pass_count += 1
        else:
            self.record.fail_count += 1
        status = "PASS" if check.passed else "FAIL"
        print(
            f"CHECK {check.name}: computed {check.computed} ({check.first_method}) "
            f"expected {check.expected} ({check.second_method}) "
            f"tolerance {check.tolerance} {status}"
        )
        return check.passed

    def compare_float(
        self,
        name: str,
        computed: float,
        expected: float,
        tolerance: float,
        first_method: str,
        second_method: str,
    ) -> bool:
        """Compare two floating-point values inside a tolerance.

        Args:
            name: The short name of the check.
            computed: The value of the first method.
            expected: The value of the second method.
            tolerance: The largest difference that the check accepts.
            first_method: The name of the first method.
            second_method: The name of the second method.

        Returns:
            True when the difference is inside the tolerance.
        """
        if first_method == second_method:
            raise ValueError(f"the check '{name}' compares one method with itself")
        difference = abs(float(computed) - float(expected))
        check = Check(
            name=name,
            computed=f"{computed:.12g}",
            expected=f"{expected:.12g}",
            tolerance=f"{tolerance:.1e}",
            first_method=first_method,
            second_method=second_method,
            passed=bool(difference <= tolerance),
        )
        return self._store(check)

    def compare_exact(
        self,
        name: str,
        computed: Fraction,
        expected: Fraction,
        first_method: str,
        second_method: str,
    ) -> bool:
        """Compare two exact rational values.

        Args:
            name: The short name of the check.
            computed: The value of the first method.
            expected: The value of the second method.
            first_method: The name of the first method.
            second_method: The name of the second method.

        Returns:
            True when the two fractions are equal.
        """
        if first_method == second_method:
            raise ValueError(f"the check '{name}' compares one method with itself")
        check = Check(
            name=name,
            computed=str(computed),
            expected=str(expected),
            tolerance="0",
            first_method=first_method,
            second_method=second_method,
            passed=bool(computed == expected),
        )
        return self._store(check)

    def compare_text(
        self,
        name: str,
        computed: str,
        expected: str,
        first_method: str,
        second_method: str,
    ) -> bool:
        """Compare two text values that a script prints from different sources.

        Args:
            name: The short name of the check.
            computed: The text of the first method.
            expected: The text of the second method.
            first_method: The name of the first method.
            second_method: The name of the second method.

        Returns:
            True when the two texts are equal.
        """
        if first_method == second_method:
            raise ValueError(f"the check '{name}' compares one method with itself")
        check = Check(
            name=name,
            computed=computed,
            expected=expected,
            tolerance="0",
            first_method=first_method,
            second_method=second_method,
            passed=bool(computed == expected),
        )
        return self._store(check)

    def finish(self) -> None:
        """Print the summary, write the JSON record, and stop the script on a failure."""
        self.record.pass_count = sum(1 for check in self.record.checks if check.passed)
        self.record.fail_count = len(self.record.checks) - self.record.pass_count
        total = len(self.record.checks)
        print(
            f"SUMMARY part {self.record.part_number}: {self.record.pass_count} of {total} checks passed, "
            f"{self.record.fail_count} failed"
        )
        OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
        destination = OUTPUT_DIRECTORY / f"part{self.record.part_number}_summary.json"
        payload: dict[str, Any] = asdict(self.record)
        destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"RECORD part {self.record.part_number}: {destination}")
        if self.record.fail_count:
            sys.exit(1)
