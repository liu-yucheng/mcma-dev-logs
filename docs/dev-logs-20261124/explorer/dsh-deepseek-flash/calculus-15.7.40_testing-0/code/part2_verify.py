"""Verify the mass of the solid E from four independent computations.

The script evaluates the same mass as a triple integral in two orders, as a single integral of the section area, as
a substituted integral, and as a Monte Carlo estimate. Every pair of computations is asserted.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import sympy
from scipy import integrate

import check_report
import figure_anchors
import problem_model

PART_NUMBER = 2
PART_TITLE = "Compute the mass of the solid"

GENERATOR = np.random.default_rng(check_report.RANDOM_SEED + PART_NUMBER)

MONTE_CARLO_POINTS = 4_000_000
"""The number of random points of the box that estimate the mass."""

HEIGHTS_CHECKED_AGAINST_THE_INNER_INTEGRAL = (0.0, 0.4, 0.8)
"""The three heights at which the inner integral of y is compared with the section area."""


def mass_from_two_orders() -> tuple[sympy.Expr, sympy.Expr]:
    """Return the mass from two orders of the triple integral.

    Returns:
        A pair of exact expressions, one for each order.
    """
    symbol_x, symbol_y, symbol_z = sympy.symbols("x y z", real=True)
    density = sympy.Integer(4)
    first_order = sympy.integrate(
        density,
        (symbol_y, -sympy.sqrt(1 - symbol_z), sympy.sqrt(1 - symbol_z)),
        (symbol_x, 0, 1 - symbol_z),
        (symbol_z, 0, 1),
    )
    second_order = sympy.integrate(
        density,
        (symbol_x, 0, 1 - symbol_z),
        (symbol_z, 0, 1 - symbol_y**2),
        (symbol_y, -1, 1),
    )
    return sympy.simplify(first_order), sympy.simplify(second_order)


def mass_from_substitution() -> sympy.Expr:
    """Return the mass from the substitution u = sqrt(1 - z) of the single integral.

    Returns:
        The exact mass.
    """
    symbol_u = sympy.Symbol("u", positive=True)
    return sympy.integrate(16 * symbol_u**4, (symbol_u, 0, 1))


def mass_from_section_area() -> sympy.Expr:
    """Return the mass from the single integral of the section area.

    Returns:
        The exact mass.
    """
    symbol_z = sympy.Symbol("z", real=True)
    return sympy.integrate(4 * 2 * (1 - symbol_z) ** sympy.Rational(3, 2), (symbol_z, 0, 1))


def mass_from_inner_integral_two_forms() -> tuple[sympy.Expr, sympy.Expr, sympy.Expr]:
    """Return the mass from the inner integral over z in two forms.

    The first form integrates the density times the length in x over z symbolically. The second form uses the
    expanded polynomial that the same integral has after the substitution u = 1 - y**2 is written out.

    Returns:
        Three exact expressions: the mass from the symbolic inner integral, the mass from the expanded polynomial,
        and the expanded polynomial itself.
    """
    symbol_y, symbol_z = sympy.symbols("y z", real=True)
    inner_symbolic = sympy.integrate(sympy.Integer(4) * (1 - symbol_z), (symbol_z, 0, 1 - symbol_y**2))
    expanded = sympy.Integer(4) * (1 - symbol_y**2) - sympy.Integer(2) * (1 - symbol_y**2) ** 2
    first_form = sympy.integrate(inner_symbolic, (symbol_y, -1, 1))
    second_form = sympy.integrate(sympy.expand(expanded), (symbol_y, -1, 1))
    return first_form, second_form, sympy.expand(expanded)


def main() -> None:
    """Run every check of part 2 and write the record."""
    recorder = check_report.CheckRecorder(PART_NUMBER, PART_TITLE)

    first_order, second_order = mass_from_two_orders()
    substituted = mass_from_substitution()
    from_area = mass_from_section_area()
    exact_mass = Fraction(int(sympy.numer(first_order)), int(sympy.denom(first_order)))
    recorder.note(f"mass from the order dy dx dz: {first_order}")
    recorder.note(f"mass from the order dz dx dy: {second_order}")
    recorder.note(f"mass from the substituted integral: {substituted}")
    recorder.note(f"mass from the section area: {from_area}")

    inner_symbolic_mass, inner_expanded_mass, expanded_inner = mass_from_inner_integral_two_forms()
    recorder.note(f"the integral over z equals {expanded_inner}")
    recorder.note(f"mass from the inner integral over z: {inner_symbolic_mass}")
    recorder.note(f"mass from the expanded inner polynomial: {inner_expanded_mass}")
    recorder.compare_exact(
        "mass from the inner integral over z against its expanded form",
        Fraction(int(sympy.numer(inner_symbolic_mass)), int(sympy.denom(inner_symbolic_mass))),
        Fraction(int(sympy.numer(inner_expanded_mass)), int(sympy.denom(inner_expanded_mass))),
        "symbolic integral of the z integral",
        "integral of the expanded polynomial in y",
    )
    recorder.compare_exact(
        "mass from two orders of the triple integral",
        Fraction(int(sympy.numer(first_order)), int(sympy.denom(first_order))),
        Fraction(int(sympy.numer(second_order)), int(sympy.denom(second_order))),
        "triple integral in the order dy dx dz",
        "triple integral in the order dz dx dy",
    )
    recorder.compare_exact(
        "mass from the substituted integral",
        Fraction(int(sympy.numer(substituted)), int(sympy.denom(substituted))),
        exact_mass,
        "substituted integral of 16 u^4",
        "triple integral in the order dy dx dz",
    )
    recorder.compare_exact(
        "mass from the section area",
        Fraction(int(sympy.numer(from_area)), int(sympy.denom(from_area))),
        exact_mass,
        "single integral of 4 times the section area",
        "triple integral in the order dy dx dz",
    )

    # The inner integral of y must reproduce the section area of part 1 at every height.
    for height in HEIGHTS_CHECKED_AGAINST_THE_INNER_INTEGRAL:
        length_in_y = float(
            integrate.quad(
                lambda coordinate_y: 1.0,
                -float(problem_model.half_width_at_height(height)),
                float(problem_model.half_width_at_height(height)),
            )[0]
        )
        recorder.compare_float(
            f"inner integral of y at z = {height:.1f}",
            length_in_y,
            float(problem_model.cross_section_area_at_z(height) / (1.0 - height)),
            1.0e-10,
            "integral of 1 over the y bounds",
            "section area divided by the x length",
        )

    mass_from_area_integral = float(
        integrate.quad(lambda height: 4.0 * float(problem_model.cross_section_area_at_z(height)), 0.0, 1.0)[0]
    )
    recorder.compare_float(
        "mass from the numerical single integral",
        mass_from_area_integral,
        float(exact_mass),
        1.0e-10,
        "adaptive quadrature of the section area",
        "exact triple integral",
    )

    mass_from_y_sections = float(
        integrate.quad(
            lambda coordinate_y: 4.0 * float(problem_model.cross_section_area_at_y(coordinate_y)),
            problem_model.COORDINATE_Y_LOWEST,
            problem_model.COORDINATE_Y_HIGHEST,
        )[0]
    )
    recorder.compare_float(
        "mass from the integral of the y sections",
        mass_from_y_sections,
        float(exact_mass),
        1.0e-10,
        "adaptive quadrature over y of the trapezoid area",
        "exact triple integral",
    )

    sample = problem_model.sample_box(MONTE_CARLO_POINTS, GENERATOR)
    inside = problem_model.point_in_solid_by_width(sample[:, 0], sample[:, 1], sample[:, 2])
    fraction_inside = float(np.count_nonzero(inside)) / MONTE_CARLO_POINTS
    box_volume = 2.0
    mass_from_sampling = 4.0 * box_volume * fraction_inside
    standard_error = 4.0 * box_volume * float(np.sqrt(fraction_inside * (1.0 - fraction_inside) / MONTE_CARLO_POINTS))
    recorder.compare_float(
        "mass from rejection sampling",
        mass_from_sampling,
        float(exact_mass),
        4.0 * standard_error,
        "Monte Carlo estimate from the box",
        "exact triple integral",
    )
    recorder.note(f"mass from rejection sampling: {mass_from_sampling:.6f} with standard error {standard_error:.6f}")

    # A reader may forget that the thickness in y varies. Each naive value below is computed, not typed.
    triangle_area = problem_model.polygon_area(
        np.column_stack((figure_anchors.projection_polygon(), np.zeros(3))), 0, 1
    )
    naive_prism_mass = 4.0 * triangle_area
    naive_narrow_mass = 4.0 * float(integrate.quad(lambda height: (1.0 - height) ** 2, 0.0, 1.0)[0])
    recorder.note(f"naive mass of a prism of thickness 1 over the projection: {naive_prism_mass:.6f}")
    recorder.note(f"naive mass if the y half width were 1 - z instead of sqrt(1 - z): {naive_narrow_mass:.6f}")
    recorder.note(f"exact mass: {float(exact_mass):.6f}")

    recorder.set_value("p2_mass_exact", f"${problem_model.fraction_to_latex(exact_mass)}$")
    recorder.set_value("p2_mass_decimal", f"${float(exact_mass):.6f}$")
    recorder.set_value("p2_volume_exact", f"${problem_model.fraction_to_latex(exact_mass / 4)}$")
    recorder.set_value("p2_volume_decimal", f"${float(exact_mass) / 4:.6f}$")
    recorder.set_value("p2_section_area_latex", "$2(1 - z)^{3/2}$")
    recorder.set_value("p2_inner_integral_latex", "$2\\sqrt{1 - z}$")
    recorder.set_value("p2_naive_prism_mass", f"${naive_prism_mass:.6f}$")
    recorder.set_value("p2_naive_narrow_mass", f"${naive_narrow_mass:.6f}$")
    recorder.set_value("p2_sampling_mass", f"${mass_from_sampling:.4f}$")
    recorder.set_value("p2_sampling_error", f"${standard_error:.4f}$")
    recorder.set_value("p2_sampling_points", f"{MONTE_CARLO_POINTS}")
    recorder.set_value("p2_area_integral_mass", f"${mass_from_area_integral:.9f}$")
    recorder.set_value("p2_y_section_mass", f"${mass_from_y_sections:.9f}$")
    recorder.set_value("p2_symbolic_mass", f"${sympy.latex(first_order)}$")

    recorder.finish()


if __name__ == "__main__":
    main()
