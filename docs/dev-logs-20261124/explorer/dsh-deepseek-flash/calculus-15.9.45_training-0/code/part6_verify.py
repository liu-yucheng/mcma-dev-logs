"""Verify the closed form and the ratio that Part 6 states.

The script compares the value that the term by term expansion produces with the value that the
closed form produces, and it compares the ratio to the unit ball with the ratio of the two exact
fractions.  It also prints the decimal string of the exact value, so that the page can quote the
same digits that the script writes.
"""

from __future__ import annotations

import math
from fractions import Fraction

import bumpy_sphere
from verification_report import CheckLog

DECIMAL_DIGITS = 12
"""Number of digits after the decimal point that the page quotes."""

RELATIVE_TOLERANCE = 1.0e-13
"""Relative tolerance that the exact arithmetic route must meet."""


def decimal_string(value: float, digits: int = DECIMAL_DIGITS) -> str:
    """Return the fixed point string of one value.

    Args:
        value: Value to write.
        digits: Number of digits after the decimal point.
    """
    return f"{value:.{digits}f}"


def main() -> None:
    """Run the checks of Part 6 and write the summary of the part."""
    log = CheckLog("part6")

    expansion_value = bumpy_sphere.exact_volume().as_float()
    closed_value = float(bumpy_sphere.closed_form_volume_over_pi()) * math.pi
    relative = abs(expansion_value - closed_value) / abs(closed_value)
    log.record(
        "closed form against the term by term expansion: relative difference",
        relative, 0.0, relative, relative < RELATIVE_TOLERANCE,
    )

    exact_quotient = bumpy_sphere.exact_volume_over_pi()
    closed_quotient = bumpy_sphere.closed_form_volume_over_pi()
    log.record(
        "quotient over pi: term by term against the closed form",
        str(exact_quotient), str(closed_quotient),
        abs(float(exact_quotient) - float(closed_quotient)),
        exact_quotient == closed_quotient,
    )

    unit_ball = 4.0 * math.pi / 3.0
    measured_ratio = expansion_value / unit_ball
    exact_ratio = float(Fraction(34, 33))
    log.record(
        "ratio to the unit ball: measured against 34/33",
        measured_ratio, exact_ratio, abs(measured_ratio - exact_ratio),
        abs(measured_ratio - exact_ratio) < 1.0e-12,
    )

    excess = expansion_value - unit_ball
    excess_reference = float(Fraction(4, 99)) * math.pi
    log.record(
        "excess over the unit ball: measured against 4 pi / 99",
        excess, excess_reference, abs(excess - excess_reference),
        abs(excess - excess_reference) < 1.0e-12,
    )

    residue = abs(bumpy_sphere.exact_volume_of_term(1, 1).as_float()) + abs(
        bumpy_sphere.exact_volume_of_term(3, 3).as_float())
    log.record(
        "vanishing terms of the expansion: sum of the two residues against 0",
        residue, 0.0, residue, residue < 1.0e-15,
    )

    log.require_all_passed()
    log.write()
    print(f"decimal value of the volume: {decimal_string(expansion_value)}", flush=True)
    print(f"exact value: {exact_quotient} times pi, ratio to the unit ball {exact_ratio:.10f}",
          flush=True)


if __name__ == "__main__":
    main()
