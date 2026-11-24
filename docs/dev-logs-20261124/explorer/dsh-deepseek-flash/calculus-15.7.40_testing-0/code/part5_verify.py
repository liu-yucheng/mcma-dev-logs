"""Assemble the answer and check it against the records of the earlier parts.

The script derives the mass and the center of mass once more from three single integrals, compares the result with
the value that each earlier part recorded, and checks the interpretation of the answer with computed bounds.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import integrate

import check_report
import problem_model

PART_NUMBER = 5
PART_TITLE = "State the answer and check its meaning"

EXACT_MASS = Fraction(16, 5)
"""The mass that the tutorial reports."""

EXACT_CENTER = (Fraction(5, 14), Fraction(0), Fraction(2, 7))
"""The center of mass that the tutorial reports."""

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"
"""The directory that holds the record of each part."""


def read_record(part_number: int) -> dict:
    """Return the record of one part.

    Args:
        part_number: The number of the part.

    Returns:
        The parsed record.
    """
    path = OUTPUT_DIRECTORY / f"part{part_number}_summary.json"
    return json.loads(path.read_text(encoding="utf-8"))


def single_integrals() -> tuple[float, float, float]:
    """Return the mass and the two non-zero moments from three single integrals.

    Returns:
        The mass, the moment of x and the moment of z.
    """
    mass = 4.0 * float(integrate.quad(lambda height: 2.0 * (1.0 - height) ** 1.5, 0.0, 1.0)[0])
    moment_yz = float(integrate.quad(lambda height: 4.0 * (1.0 - height) ** 2.5, 0.0, 1.0)[0])
    moment_xy = 4.0 * float(integrate.quad(lambda height: height * 2.0 * (1.0 - height) ** 1.5, 0.0, 1.0)[0])
    return mass, moment_yz, moment_xy


def main() -> None:
    """Run every check of part 5 and write the record."""
    recorder = check_report.CheckRecorder(PART_NUMBER, PART_TITLE)

    mass, moment_yz, moment_xy = single_integrals()
    center = (moment_yz / mass, 0.0, moment_xy / mass)
    recorder.note(f"mass from three single integrals: {mass:.9f}")
    recorder.note(f"center from three single integrals: {center[0]:.9f}, {center[1]:.9f}, {center[2]:.9f}")

    recorder.compare_float(
        "mass from the single integrals",
        mass,
        float(EXACT_MASS),
        1.0e-9,
        "quadrature of three single integrals",
        "exact mass of part 2",
    )
    for index, name in enumerate(("x", "y", "z")):
        recorder.compare_float(
            f"center coordinate {name} from the single integrals",
            center[index],
            float(EXACT_CENTER[index]),
            1.0e-9,
            "ratio of two single integrals",
            "ratio of two symbolic moments of part 3",
        )

    # The records of the earlier parts must hold the same numbers.
    recorded = {part: read_record(part) for part in (2, 3, 4)}
    recorder.compare_text(
        "mass recorded by part 2",
        recorded[2]["values"]["p2_mass_decimal"],
        f"${mass:.6f}$",
        "value stored by code/part2_verify.py",
        "mass from three single integrals",
    )
    recorder.compare_text(
        "moment of x recorded by part 3",
        recorded[3]["values"]["p3_m_yz"],
        f"${problem_model.fraction_to_latex(Fraction(8, 7))}$",
        "value stored by code/part3_verify.py",
        "moment from a single integral",
    )
    recorder.compare_text(
        "moment of z recorded by part 3",
        recorded[3]["values"]["p3_m_xy"],
        f"${problem_model.fraction_to_latex(Fraction(32, 35))}$",
        "value stored by code/part3_verify.py",
        "moment from a single integral",
    )
    recorder.compare_text(
        "coordinate x of the center recorded by part 3",
        recorded[3]["values"]["p3_xbar"],
        f"${problem_model.fraction_to_latex(EXACT_CENTER[0])}$",
        "value stored by code/part3_verify.py",
        "ratio of two single integrals",
    )
    recorder.compare_text(
        "coordinate z of the center recorded by part 3",
        recorded[3]["values"]["p3_zbar"],
        f"${problem_model.fraction_to_latex(EXACT_CENTER[2])}$",
        "value stored by code/part3_verify.py",
        "ratio of two single integrals",
    )
    recorder.compare_text(
        "mass recorded by part 4",
        recorded[4]["values"]["p4_shadow_mass"],
        f"${mass:.9f}$",
        "value stored by code/part4_verify.py",
        "mass from three single integrals",
    )

    # The answer must lie inside the solid, and every coordinate must lie in its own range.
    ranges = {
        "x": (0.0, float(problem_model.length_in_x_at_height(0.0))),
        "y": (problem_model.COORDINATE_Y_LOWEST, problem_model.COORDINATE_Y_HIGHEST),
        "z": (0.0, 1.0),
    }
    for index, name in enumerate(("x", "y", "z")):
        lowest, highest = ranges[name]
        recorder.compare_text(
            f"coordinate {name} of the center lies in its range",
            "inside" if lowest - 1.0e-12 <= center[index] <= highest + 1.0e-12 else "outside",
            "inside",
            "range of the coordinate that the region gives",
            "coordinate of the center from the single integrals",
        )
    recorder.note(f"ranges of the solid: x in [{ranges['x'][0]:.1f}, {ranges['x'][1]:.1f}], "
                  f"y in [{ranges['y'][0]:.1f}, {ranges['y'][1]:.1f}], z in [{ranges['z'][0]:.1f}, {ranges['z'][1]:.1f}]")

    # Three wrong values that a reader may produce. Each one is computed here.
    triangle_area = 0.5
    naive_prism_mass = 4.0 * triangle_area
    naive_narrow_mass = 4.0 * float(integrate.quad(lambda height: (1.0 - height) ** 2, 0.0, 1.0)[0])
    naive_center_x = (float(Fraction(8, 7)) / float(Fraction(4, 5)))
    recorder.note(f"wrong mass of a prism over the projection: {naive_prism_mass:.6f}")
    recorder.note(f"wrong mass with the width 1 - z: {naive_narrow_mass:.6f}")
    recorder.note(f"wrong coordinate x from a division by the volume: {naive_center_x:.6f}")

    recorder.compare_text(
        "the wrong mass of the prism differs from the answer",
        "different" if abs(naive_prism_mass - mass) > 0.01 * mass else "equal",
        "different",
        "prism over the projection",
        "mass from three single integrals",
    )
    recorder.compare_text(
        "the wrong mass with the width 1 - z differs from the answer",
        "different" if abs(naive_narrow_mass - mass) > 0.01 * mass else "equal",
        "different",
        "width 1 - z instead of 2 sqrt(1 - z)",
        "mass from three single integrals",
    )
    recorder.compare_text(
        "the wrong coordinate x lies outside the solid",
        "outside"
        if not bool(
            problem_model.point_in_solid_by_width(
                np.array([naive_center_x]), np.array([0.0]), np.array([0.0])
            )[0]
        )
        else "inside",
        "outside",
        "membership test at the wrong coordinate",
        "range of the coordinate that the region gives",
    )

    recorder.set_value("p5_mass", f"${problem_model.fraction_to_latex(EXACT_MASS)}$")
    recorder.set_value("p5_mass_decimal", f"${float(EXACT_MASS):.6f}$")
    recorder.set_value("p5_volume", f"${problem_model.fraction_to_latex(EXACT_MASS / 4)}$")
    recorder.set_value("p5_center", f"$\\left({problem_model.fraction_to_latex(EXACT_CENTER[0])},\\ "
                                    f"{problem_model.fraction_to_latex(EXACT_CENTER[1])},\\ "
                                    f"{problem_model.fraction_to_latex(EXACT_CENTER[2])}\\right)$")
    recorder.set_value("p5_center_decimal", f"$({center[0]:.4f},\\ {center[1]:.4f},\\ {center[2]:.4f})$")
    recorder.set_value("p5_naive_prism_mass", f"${naive_prism_mass:.6f}$")
    recorder.set_value("p5_naive_narrow_mass", f"${naive_narrow_mass:.6f}$")
    recorder.set_value("p5_naive_center_x", f"${naive_center_x:.6f}$")

    recorder.finish()


if __name__ == "__main__":
    main()
