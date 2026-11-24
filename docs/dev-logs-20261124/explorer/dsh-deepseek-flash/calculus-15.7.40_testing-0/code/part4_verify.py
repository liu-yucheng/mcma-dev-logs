"""Verify the mass and the moments of E with the shadow method.

The shadow method integrates z first. The inner integral of a fixed pair (x, y) runs from 0 to the height
min(1 - y^2, 1 - x). The script checks that height against a bisection search, then reproduces the mass and the two
non-zero moments by nested quadrature over the shadow.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import sympy
from scipy import integrate

import check_report
import figure_anchors
import problem_model

PART_NUMBER = 4
PART_TITLE = "Check the answer with the shadow method"

GENERATOR = np.random.default_rng(check_report.RANDOM_SEED + PART_NUMBER)

POINTS_CHECKED_FOR_THE_HEIGHT = 64
"""The number of shadow points at which the analytic height is compared with a bisection search."""

SHADOW_QUADRATURE_TOLERANCE = 1.0e-8
"""The tolerance of the nested quadrature over the shadow, which meets a kink at x = y^2."""

UNIFORM_POINTS = 4_000_000
"""The number of candidate points of the shadow sampling scheme."""


def analytic_height(coordinate_x: float, coordinate_y: float) -> float:
    """Return the height of the solid above a point of the shadow.

    Args:
        coordinate_x: The x coordinate of the shadow point.
        coordinate_y: The y coordinate of the shadow point.

    Returns:
        The upper limit of z at that shadow point.
    """
    return min(1.0 - coordinate_y**2, 1.0 - coordinate_x)


def height_from_bisection(coordinate_x: float, coordinate_y: float) -> float:
    """Return the height of the solid above a point of the shadow by a bisection search.

    Args:
        coordinate_x: The x coordinate of the shadow point.
        coordinate_y: The y coordinate of the shadow point.

    Returns:
        The largest z that lies in the solid above the shadow point.
    """
    lowest, highest = 0.0, 2.0
    for _ in range(80):
        middle = 0.5 * (lowest + highest)
        inside = problem_model.point_in_solid_by_width(
            np.array([coordinate_x]), np.array([coordinate_y]), np.array([middle])
        )[0]
        if bool(inside):
            lowest = middle
        else:
            highest = middle
    return 0.5 * (lowest + highest)


def shadow_mass_symbolic() -> sympy.Expr:
    """Return the mass from a symbolic integral of the height over the shadow.

    Returns:
        The exact mass.
    """
    symbol_x, symbol_y = sympy.symbols("x y", real=True)
    height = sympy.Piecewise((1 - symbol_y**2, symbol_x <= symbol_y**2), (1 - symbol_x, True))
    return sympy.simplify(sympy.integrate(4 * height, (symbol_x, 0, 1), (symbol_y, -1, 1)))


def shadow_quadrature(weight) -> float:
    """Return a nested quadrature over the shadow.

    Args:
        weight: A function of x, y and the height that returns the integrand.

    Returns:
        The value of the integral.
    """
    return float(
        integrate.quad(
            lambda coordinate_y: integrate.quad(
                lambda coordinate_x: weight(coordinate_x, coordinate_y,
                                            analytic_height(coordinate_x, coordinate_y)),
                0.0,
                1.0,
                points=[min(coordinate_y**2, 1.0)],
            )[0],
            -1.0,
            1.0,
        )[0]
    )


def main() -> None:
    """Run every check of part 4 and write the record."""
    recorder = check_report.CheckRecorder(PART_NUMBER, PART_TITLE)

    largest_difference = 0.0
    for index in range(POINTS_CHECKED_FOR_THE_HEIGHT):
        coordinate_x = (index + 0.5) / POINTS_CHECKED_FOR_THE_HEIGHT
        for fraction in (-0.9, -0.4, 0.0, 0.35, 0.85):
            coordinate_y = fraction * np.sqrt(1.0 - 0.5)
            analytic = analytic_height(coordinate_x, coordinate_y)
            searched = height_from_bisection(coordinate_x, coordinate_y)
            largest_difference = max(largest_difference, abs(analytic - searched))
    recorder.compare_float(
        "largest difference between the analytic height and the searched height",
        largest_difference,
        0.0,
        1.0e-12,
        "closed form min(1 - y^2, 1 - x)",
        "bisection search with the membership test",
    )
    recorder.note(f"largest height difference over {POINTS_CHECKED_FOR_THE_HEIGHT * 5} shadow points: {largest_difference:.3e}")

    symbolic_mass = shadow_mass_symbolic()
    recorder.note(f"mass from the symbolic shadow integral: {symbolic_mass}")
    recorder.compare_exact(
        "mass from the symbolic shadow integral",
        Fraction(int(sympy.numer(sympy.Rational(symbolic_mass))), int(sympy.denom(sympy.Rational(symbolic_mass)))),
        Fraction(16, 5),
        "symbolic integral of the height over the shadow",
        "exact mass of part 2",
    )

    quadrature_mass = shadow_quadrature(lambda coordinate_x, coordinate_y, height: 4.0 * height)
    recorder.compare_float(
        "mass from the quadrature over the shadow",
        quadrature_mass,
        float(symbolic_mass),
        SHADOW_QUADRATURE_TOLERANCE,
        "nested quadrature of the height over the shadow",
        "symbolic integral of the height over the shadow",
    )

    quadrature_moment_yz = shadow_quadrature(
        lambda coordinate_x, coordinate_y, height: 4.0 * coordinate_x * height
    )
    exact_moment_yz = Fraction(8, 7)
    recorder.compare_float(
        "M_yz from the quadrature over the shadow",
        quadrature_moment_yz,
        float(exact_moment_yz),
        SHADOW_QUADRATURE_TOLERANCE,
        "nested quadrature of 4 x times the height over the shadow",
        "exact moment of part 3",
    )

    quadrature_moment_xy = shadow_quadrature(
        lambda coordinate_x, coordinate_y, height: 4.0 * height**2 / 2.0
    )
    exact_moment_xy = Fraction(32, 35)
    recorder.compare_float(
        "M_xy from the quadrature over the shadow",
        quadrature_moment_xy,
        float(exact_moment_xy),
        SHADOW_QUADRATURE_TOLERANCE,
        "nested quadrature of the inner moment of z over the shadow",
        "exact moment of part 3",
    )

    shadow_area = problem_model.polygon_area(
        np.array([[0.0, -1.0, 0.0], [1.0, -1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]), 0, 1
    )
    projection_area = problem_model.polygon_area(
        np.column_stack((figure_anchors.projection_polygon(), np.zeros(3))), 0, 1
    )
    recorder.note(f"area of the shadow on the plane z = 0: {shadow_area:.6f}")
    recorder.note(f"area of the projection on the plane y = 0: {projection_area:.6f}")

    # Sampling scheme of the shadow: accept a shadow point with probability equal to its height.
    candidate_x = GENERATOR.uniform(0.0, 1.0, UNIFORM_POINTS)
    candidate_y = GENERATOR.uniform(-1.0, 1.0, UNIFORM_POINTS)
    candidate_height = np.minimum(1.0 - candidate_y**2, 1.0 - candidate_x)
    accepted = GENERATOR.random(UNIFORM_POINTS) < candidate_height
    accepted_count = int(np.count_nonzero(accepted))
    sampled_volume = 2.0 * float(np.mean(candidate_height))
    recorder.compare_float(
        "volume from the shadow sampling",
        sampled_volume,
        float(Fraction(4, 5)),
        1.0e-3,
        "mean accepted height times the shadow area",
        "exact volume of part 2",
    )

    point_x = candidate_x[accepted]
    point_y = candidate_y[accepted]
    point_z = GENERATOR.uniform(0.0, 1.0, accepted_count) * candidate_height[accepted]
    sampled_center = np.array([float(np.mean(point_x)), float(np.mean(point_y)), float(np.mean(point_z))])
    exact_center = np.array([float(Fraction(5, 14)), 0.0, float(Fraction(2, 7))])
    spread = np.array(
        [
            float(np.std(point_x)) / np.sqrt(accepted_count),
            float(np.std(point_y)) / np.sqrt(accepted_count),
            float(np.std(point_z)) / np.sqrt(accepted_count),
        ]
    )
    for index, name in enumerate(("x", "y", "z")):
        recorder.compare_float(
            f"center coordinate {name} from the shadow sampling",
            float(sampled_center[index]),
            float(exact_center[index]),
            4.0 * float(spread[index]),
            "mean of the points that the shadow scheme accepts",
            "ratio of two exact moments",
        )
    recorder.note(f"accepted points of the shadow scheme: {accepted_count}")
    recorder.note(f"sampled center: {sampled_center[0]:.4f}, {sampled_center[1]:.4f}, {sampled_center[2]:.4f}")
    recorder.note(f"standard error of the sampled center: {spread[0]:.5f}, {spread[1]:.5f}, {spread[2]:.5f}")

    recorder.set_value("p4_height_latex", "$\\min(1 - y^{2},\\ 1 - x)$")
    recorder.set_value("p4_shadow_area", f"${shadow_area:.6f}$")
    recorder.set_value("p4_projection_area", f"${projection_area:.6f}$")
    recorder.set_value("p4_shadow_mass", f"${quadrature_mass:.9f}$")
    recorder.set_value("p4_shadow_moment_yz", f"${quadrature_moment_yz:.9f}$")
    recorder.set_value("p4_shadow_moment_xy", f"${quadrature_moment_xy:.9f}$")
    recorder.set_value("p4_sampled_center", f"$({sampled_center[0]:.4f},\\ {sampled_center[1]:.4f},\\ {sampled_center[2]:.4f})$")
    recorder.set_value("p4_accepted_points", f"{accepted_count}")
    recorder.set_value("p4_height_points", f"{POINTS_CHECKED_FOR_THE_HEIGHT * 5}")

    recorder.finish()


if __name__ == "__main__":
    main()
