"""Verify the three first moments of the solid E and the center of mass.

The script computes every moment as a symbolic triple integral in two orders, as a single integral of a section, and
as a Monte Carlo estimate. It then derives the center of mass by two independent routes.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import sympy
from scipy import integrate

import check_report
import problem_model

PART_NUMBER = 3
PART_TITLE = "Compute the first moments and the center of mass"

GENERATOR = np.random.default_rng(check_report.RANDOM_SEED + PART_NUMBER)

MONTE_CARLO_POINTS = 4_000_000
"""The number of random points of the box that estimate each moment."""

BOX_VOLUME = 2.0
"""The volume of the box that contains the solid."""

EXACT_MASS = Fraction(16, 5)
"""The mass that code/part2_verify.py prints, used as the divisor of every center coordinate."""

SAMPLING_TOLERANCE = 0.01
"""Four standard errors of a sampled center coordinate, rounded up."""


def moments_from_two_orders() -> tuple[dict[str, sympy.Expr], dict[str, sympy.Expr]]:
    """Return the three first moments of E from two orders of the triple integral.

    Returns:
        Two dictionaries of exact expressions, one for each order.
    """
    symbol_x, symbol_y, symbol_z = sympy.symbols("x y z", real=True)
    density = sympy.Integer(4)
    integrands = {"x": density * symbol_x, "y": density * symbol_y, "z": density * symbol_z}
    first_order = {
        name: sympy.integrate(
            integrand,
            (symbol_y, -sympy.sqrt(1 - symbol_z), sympy.sqrt(1 - symbol_z)),
            (symbol_x, 0, 1 - symbol_z),
            (symbol_z, 0, 1),
        )
        for name, integrand in integrands.items()
    }
    second_order = {
        name: sympy.integrate(
            integrand,
            (symbol_x, 0, 1 - symbol_z),
            (symbol_z, 0, 1 - symbol_y**2),
            (symbol_y, -1, 1),
        )
        for name, integrand in integrands.items()
    }
    return (
        {name: sympy.simplify(value) for name, value in first_order.items()},
        {name: sympy.simplify(value) for name, value in second_order.items()},
    )


def as_fraction(expression: sympy.Expr) -> Fraction:
    """Return an exact rational number for a symbolic expression.

    Args:
        expression: A symbolic expression that must be rational.

    Returns:
        The same number as a Fraction.
    """
    rational = sympy.Rational(expression)
    return Fraction(int(sympy.numer(rational)), int(sympy.denom(rational)))


def mass_from_y_sections() -> float:
    """Return the mass from the quadrature of the trapezoid section area.

    Returns:
        The mass.
    """
    return float(
        integrate.quad(
            lambda coordinate_y: 4.0 * float(problem_model.cross_section_area_at_y(coordinate_y)),
            problem_model.COORDINATE_Y_LOWEST,
            problem_model.COORDINATE_Y_HIGHEST,
        )[0]
    )


def main() -> None:
    """Run every check of part 3 and write the record."""
    recorder = check_report.CheckRecorder(PART_NUMBER, PART_TITLE)

    first_order, second_order = moments_from_two_orders()
    for name in ("x", "y", "z"):
        recorder.note(f"moment of {name} from the order dy dx dz: {first_order[name]}")
        recorder.note(f"moment of {name} from the order dx dz dy: {second_order[name]}")

    for name, label in (("x", "M_yz"), ("y", "M_xz"), ("z", "M_xy")):
        recorder.compare_exact(
            f"{label} from two orders",
            as_fraction(first_order[name]),
            as_fraction(second_order[name]),
            "triple integral in the order dy dx dz",
            "triple integral in the order dx dz dy",
        )

    moment_yz = as_fraction(first_order["x"])
    moment_xz = as_fraction(first_order["y"])
    moment_xy = as_fraction(first_order["z"])

    recorder.compare_float(
        "mass from the quadrature of the y sections",
        mass_from_y_sections(),
        float(EXACT_MASS),
        1.0e-10,
        "adaptive quadrature of the trapezoid area",
        "exact mass of part 2",
    )

    # The moment of y vanishes because the region and the density are symmetric in y.
    sample = problem_model.sample_box(MONTE_CARLO_POINTS, GENERATOR)
    inside = problem_model.point_in_solid_by_width(sample[:, 0], sample[:, 1], sample[:, 2])
    mirrored = problem_model.point_in_solid_by_width(sample[:, 0], -sample[:, 1], sample[:, 2])
    recorder.compare_text(
        "membership of the mirrored points",
        "identical" if np.array_equal(inside, mirrored) else "different",
        "identical",
        "membership of the sampled points",
        "membership of the mirrored points",
    )

    # Single integrals of the sections give the same two non-zero moments.
    moment_yz_from_sections = float(
        integrate.quad(
            lambda height: 4.0 * (1.0 - height) ** 2 / 2.0 * (1.0 - height) ** 0.5 * 2.0, 0.0, 1.0
        )[0]
    )
    recorder.compare_float(
        "M_yz from the section integral",
        moment_yz_from_sections,
        float(moment_yz),
        1.0e-10,
        "quadrature of the inner moment of x at each height",
        "exact triple integral",
    )
    moment_xy_from_sections = float(
        integrate.quad(
            lambda height: 4.0 * height * float(problem_model.cross_section_area_at_z(height)), 0.0, 1.0
        )[0]
    )
    recorder.compare_float(
        "M_xy from the section integral",
        moment_xy_from_sections,
        float(moment_xy),
        1.0e-10,
        "quadrature of 4 z times the section area",
        "exact triple integral",
    )
    moment_xz_by_oddness = float(
        integrate.quad(
            lambda coordinate_y: 4.0 * coordinate_y * float(problem_model.cross_section_area_at_y(coordinate_y)),
            -1.0,
            1.0,
        )[0]
    )
    recorder.compare_float(
        "M_xz from an odd integrand over symmetric bounds",
        moment_xz_by_oddness,
        float(moment_xz),
        1.0e-11,
        "quadrature of an odd integrand over symmetric bounds",
        "exact triple integral",
    )

    # Sampling estimates of the three moments.
    sample_fraction = float(np.mean(inside.astype(float)))
    sampled_x = 4.0 * BOX_VOLUME * float(np.mean(inside * sample[:, 0]))
    sampled_y = 4.0 * BOX_VOLUME * float(np.mean(inside * sample[:, 1]))
    sampled_z = 4.0 * BOX_VOLUME * float(np.mean(inside * sample[:, 2]))
    sampled_center = np.array([sampled_x, sampled_y, sampled_z]) / (4.0 * BOX_VOLUME * sample_fraction)
    recorder.note(f"M_yz from sampling: {sampled_x:.4f}")
    recorder.note(f"M_xz from sampling: {sampled_y:.4f}")
    recorder.note(f"M_xy from sampling: {sampled_z:.4f}")
    recorder.note(f"share of the box inside the solid: {sample_fraction:.6f}")

    center_of_mass = np.array(
        [float(moment_yz), float(moment_xz), float(moment_xy)]
    ) / float(EXACT_MASS)
    for index, name in enumerate(("x", "y", "z")):
        recorder.compare_float(
            f"center coordinate {name} from sampling",
            float(sampled_center[index]),
            float(center_of_mass[index]),
            SAMPLING_TOLERANCE,
            "ratio of two sampled moments",
            "ratio of two exact moments",
        )

    # The center of mass must lie inside the solid; a division by the volume moves it outside.
    inside_center = problem_model.point_in_solid_by_width(
        np.array([float(center_of_mass[0])]), np.array([float(center_of_mass[1])]),
        np.array([float(center_of_mass[2])])
    )[0]
    recorder.compare_text(
        "the center of mass lies inside the solid",
        "inside" if bool(inside_center) else "outside",
        "inside",
        "membership test at the exact center",
        "statement of the problem",
    )
    naive_ratio = float(moment_yz) / float(EXACT_MASS / 4)
    inside_naive = problem_model.point_in_solid_by_width(
        np.array([naive_ratio]), np.array([0.0]), np.array([0.0])
    )[0]
    recorder.note(f"M_yz divided by the volume instead of the mass: {naive_ratio:.6f}")
    recorder.compare_text(
        "the moment divided by the volume lies outside the solid",
        "inside" if bool(inside_naive) else "outside",
        "outside",
        "membership test at the wrong ratio",
        "statement of the problem",
    )

    x_bar = as_fraction(sympy.Rational(moment_yz, 1) / sympy.Rational(int(EXACT_MASS.numerator),
                                                                     int(EXACT_MASS.denominator)))
    z_bar = as_fraction(sympy.Rational(moment_xy, 1) / sympy.Rational(int(EXACT_MASS.numerator),
                                                                     int(EXACT_MASS.denominator)))

    recorder.set_value("p3_m_yz", f"${problem_model.fraction_to_latex(moment_yz)}$")
    recorder.set_value("p3_m_yz_decimal", f"${float(moment_yz):.6f}$")
    recorder.set_value("p3_m_xz", f"${problem_model.fraction_to_latex(moment_xz)}$")
    recorder.set_value("p3_m_xy", f"${problem_model.fraction_to_latex(moment_xy)}$")
    recorder.set_value("p3_m_xy_decimal", f"${float(moment_xy):.6f}$")
    recorder.set_value("p3_xbar", f"${problem_model.fraction_to_latex(x_bar)}$")
    recorder.set_value("p3_zbar", f"${problem_model.fraction_to_latex(z_bar)}$")
    recorder.set_value("p3_xbar_decimal", f"${float(center_of_mass[0]):.6f}$")
    recorder.set_value("p3_zbar_decimal", f"${float(center_of_mass[2]):.6f}$")
    recorder.set_value("p3_naive_ratio", f"${naive_ratio:.6f}$")
    recorder.set_value("p3_sampled_x", f"${sampled_x:.4f}$")
    recorder.set_value("p3_sampled_y", f"${sampled_y:.4f}$")
    recorder.set_value("p3_sampled_z", f"${sampled_z:.4f}$")
    recorder.set_value(
        "p3_sampled_center",
        f"$({sampled_center[0]:.4f},\\ {sampled_center[1]:.4f},\\ {sampled_center[2]:.4f})$",
    )

    recorder.finish()


if __name__ == "__main__":
    main()
