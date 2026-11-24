"""Verify the shape of the solid E: the four inequalities, the range of y, and the three families of sections.

Every check compares a value that one method computes with a value that a different method computes. The script
prints each corner list that the tutorial quotes.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import sympy
from scipy import integrate

import check_report
import figure_anchors
import problem_model

PART_NUMBER = 1
PART_TITLE = "Read the shape of the solid from the four inequalities"

GENERATOR = np.random.default_rng(check_report.RANDOM_SEED)

POINTS_CHECKED_AGAINST_SYMBOL = 200_000
"""The number of random points that the two readings of the cylinder classify."""

POINTS_CHECKED_FOR_PROJECTION = 20_000
"""The number of random points of the unit square that the projection test classifies."""

SAMPLES_PER_SECTION = 400_000
"""The number of random points that estimates one section area."""

HEIGHTS_OF_SECTIONS = (0.0, 0.5, 0.9)
"""The three heights z at which the script checks the horizontal section."""

COORDINATES_Y_OF_SECTIONS = (-0.6, 0.0, 0.5)
"""The three coordinates y at which the script checks the section in the plane of constant y."""

COORDINATES_X_OF_SECTIONS = (0.0, 0.4, 0.8, 1.0)
"""The four coordinates x at which the script checks the section in the plane of constant x."""


def exact_residual_of_cylinder(point: tuple[float, float, float]) -> Fraction:
    """Return the residual z - (1 - y^2) of the cylinder equation in exact rational arithmetic.

    Args:
        point: The point (x, y, z).

    Returns:
        The exact residual, read from the decimal text of the coordinates.
    """
    x_coordinate, y_coordinate, z_coordinate = (Fraction(str(value)) for value in point)
    del x_coordinate
    return z_coordinate - (Fraction(1) - y_coordinate**2)


def exact_residual_of_inclined_plane(point: tuple[float, float, float]) -> Fraction:
    """Return the residual x + z - 1 of the plane equation in exact rational arithmetic.

    Args:
        point: The point (x, y, z).

    Returns:
        The exact residual, read from the decimal text of the coordinates.
    """
    x_coordinate, y_coordinate, z_coordinate = (Fraction(str(value)) for value in point)
    del y_coordinate
    return x_coordinate + z_coordinate - Fraction(1)


def exact_point_in_solid(point: tuple[float, float, float]) -> bool:
    """Return True when the four inequalities hold at the point in exact rational arithmetic.

    Args:
        point: The point (x, y, z).

    Returns:
        True when every inequality of the solid holds.
    """
    x_coordinate, y_coordinate, z_coordinate = (Fraction(str(value)) for value in point)
    return bool(
        z_coordinate >= 0
        and z_coordinate <= 1 - y_coordinate**2
        and x_coordinate >= 0
        and x_coordinate <= 1 - z_coordinate
    )


def section_area_by_sampling(plane: str, value: float) -> float:
    """Estimate a section area from the indicator of the solid.

    Args:
        plane: The name of the coordinate that stays fixed: 'x', 'y', or 'z'.
        value: The fixed value of that coordinate.

    Returns:
        The estimated area of the section.
    """
    if plane == "z":
        first = GENERATOR.uniform(0.0, 1.0, SAMPLES_PER_SECTION)
        second = GENERATOR.uniform(-1.0, 1.0, SAMPLES_PER_SECTION)
        inside = problem_model.point_in_solid_by_width(first, second, value)
        box_area = 2.0
    elif plane == "y":
        first = GENERATOR.uniform(0.0, 1.0, SAMPLES_PER_SECTION)
        second = GENERATOR.uniform(0.0, 1.0, SAMPLES_PER_SECTION)
        inside = problem_model.point_in_solid_by_width(first, value, second)
        box_area = 1.0
    elif plane == "x":
        first = GENERATOR.uniform(-1.0, 1.0, SAMPLES_PER_SECTION)
        second = GENERATOR.uniform(0.0, 1.0, SAMPLES_PER_SECTION)
        inside = problem_model.point_in_solid_by_width(value, first, second)
        box_area = 2.0
    else:
        raise ValueError(f"unknown plane '{plane}'")
    return float(box_area * np.count_nonzero(inside) / SAMPLES_PER_SECTION)


def main() -> None:
    """Run every check of part 1 and write the record."""
    recorder = check_report.CheckRecorder(PART_NUMBER, PART_TITLE)

    # Anchor points of the four surface labels of figure 1.
    for index, label in enumerate(figure_anchors.SURFACE_LABELS):
        recorder.note(f"label {index + 1} for {label.surface_name} at {label.anchor_point}")
    cylinder_label = figure_anchors.SURFACE_LABELS[0]
    plane_label = figure_anchors.SURFACE_LABELS[1]
    wall_label = figure_anchors.SURFACE_LABELS[2]
    floor_label = figure_anchors.SURFACE_LABELS[3]

    recorder.compare_exact(
        "cylinder label lies on its surface",
        exact_residual_of_cylinder(cylinder_label.anchor_point),
        Fraction(0),
        "exact residual of the drawn anchor",
        "exact zero of the equation",
    )
    recorder.compare_exact(
        "inclined plane label lies on its surface",
        exact_residual_of_inclined_plane(plane_label.anchor_point),
        Fraction(0),
        "exact residual of the drawn anchor",
        "exact zero of the equation",
    )
    recorder.compare_exact(
        "wall label keeps x = 0",
        Fraction(str(wall_label.anchor_point[0])),
        Fraction(0),
        "exact coordinate of the drawn anchor",
        "exact zero of the equation x = 0",
    )
    recorder.compare_exact(
        "floor label keeps z = 0",
        Fraction(str(floor_label.anchor_point[2])),
        Fraction(0),
        "exact coordinate of the drawn anchor",
        "exact zero of the equation z = 0",
    )

    anchors = [label.anchor_point for label in figure_anchors.SURFACE_LABELS]
    inside_by_predicate = [
        bool(problem_model.point_in_solid_by_height(point[0], point[1], point[2])) for point in anchors
    ]
    inside_by_exact_arithmetic = [exact_point_in_solid(point) for point in anchors]
    recorder.compare_text(
        "the four label anchors lie inside E",
        "".join("T" if flag else "F" for flag in inside_by_predicate),
        "".join("T" if flag else "F" for flag in inside_by_exact_arithmetic),
        "floating-point predicate",
        "exact rational substitution",
    )

    # The two readings of the parabolic cylinder must classify every point in the same way.
    candidate = problem_model.sample_box(POINTS_CHECKED_AGAINST_SYMBOL, GENERATOR)
    by_height = problem_model.point_in_solid_by_height(candidate[:, 0], candidate[:, 1], candidate[:, 2])
    by_width = problem_model.point_in_solid_by_width(candidate[:, 0], candidate[:, 1], candidate[:, 2])
    disagreements = int(np.count_nonzero(by_height != by_width))
    recorder.compare_text(
        "height form and width form agree on every sample",
        f"{disagreements} disagreements in {POINTS_CHECKED_AGAINST_SYMBOL} points",
        f"0 disagreements in {POINTS_CHECKED_AGAINST_SYMBOL} points",
        "count of the height form",
        "count of the width form",
    )

    # The range of y follows from the single condition 1 - y^2 >= 0.
    symbol_y = sympy.Symbol("y", real=True)
    roots = sorted(sympy.solve(sympy.Eq(1 - symbol_y**2, 0), symbol_y))
    recorder.compare_text(
        "range of y from the cylinder equation",
        f"[{roots[0]}, {roots[1]}]",
        f"[{int(problem_model.COORDINATE_Y_LOWEST)}, {int(problem_model.COORDINATE_Y_HIGHEST)}]",
        "roots of 1 - y^2 = 0",
        "reading of the statement",
    )
    solid_sample = problem_model.sample_solid(POINTS_CHECKED_AGAINST_SYMBOL, GENERATOR)
    recorder.compare_float(
        "largest |y| in a random sample",
        float(np.max(np.abs(solid_sample[:, 1]))),
        1.0,
        1.0e-2,
        "Monte Carlo maximum",
        "closed-form bound of the cylinder",
    )
    recorder.compare_float(
        "largest z in a random sample",
        float(np.max(solid_sample[:, 2])),
        1.0,
        1.0e-2,
        "Monte Carlo maximum",
        "closed-form ceiling of the cylinder",
    )

    # Horizontal sections: a rectangle at each height.
    for height in HEIGHTS_OF_SECTIONS:
        corners = problem_model.corners_at_z(height)
        area_corners = problem_model.polygon_area(corners, 0, 1)
        area_formula = float(problem_model.cross_section_area_at_z(height))
        area_sampled = section_area_by_sampling("z", height)
        recorder.note(f"section at z = {height:.1f} has corners {problem_model.describe_points(corners)}")
        recorder.compare_float(
            f"area of the section at z = {height:.1f} from its corners",
            area_corners,
            area_formula,
            1.0e-12,
            "shoelace formula on the printed corners",
            "closed form 2 (1 - z)^(3/2)",
        )
        recorder.compare_float(
            f"area of the section at z = {height:.1f} by sampling",
            area_sampled,
            area_formula,
            8.0e-3,
            "indicator sampling of the inequalities",
            "closed form 2 (1 - z)^(3/2)",
        )

    # Sections in the plane of constant y: a right trapezoid.
    for coordinate_y in COORDINATES_Y_OF_SECTIONS:
        corners = problem_model.corners_at_y(coordinate_y)
        area_corners = problem_model.polygon_area(corners, 0, 2)
        area_formula = float(problem_model.cross_section_area_at_y(coordinate_y))
        area_sampled = section_area_by_sampling("y", coordinate_y)
        parallel_side = 1.0 - coordinate_y**2
        recorder.note(f"section at y = {coordinate_y:.1f} has corners {problem_model.describe_points(corners)}")
        recorder.compare_float(
            f"area of the section at y = {coordinate_y:.1f} from its corners",
            area_corners,
            area_formula,
            1.0e-12,
            "shoelace formula on the printed corners",
            f"closed form u - u^2 / 2 with u = {parallel_side:.4f}",
        )
        recorder.compare_float(
            f"area of the section at y = {coordinate_y:.1f} by sampling",
            area_sampled,
            area_formula,
            8.0e-3,
            "indicator sampling of the inequalities",
            f"closed form u - u^2 / 2 with u = {parallel_side:.4f}",
        )

    # Sections in the plane of constant x: the curvilinear region between the two branches of the curve.
    for coordinate_x in COORDINATES_X_OF_SECTIONS:
        corners = problem_model.corners_at_x(coordinate_x)
        area_formula = float(problem_model.cross_section_area_at_x(coordinate_x))
        area_by_integral = float(
            integrate.quad(lambda height: 2.0 * np.sqrt(max(1.0 - height, 0.0)), 0.0, 1.0 - coordinate_x)[0]
        )
        recorder.note(f"section at x = {coordinate_x:.1f} has corners {problem_model.describe_points(corners)}")
        recorder.compare_float(
            f"area of the section at x = {coordinate_x:.1f} from the width integral",
            area_by_integral,
            area_formula,
            1.0e-10,
            "integral of the width 2 sqrt(1 - z)",
            "closed form (4/3) (1 - x^(3/2))",
        )
        if coordinate_x < 1.0:
            area_sampled = section_area_by_sampling("x", coordinate_x)
            recorder.compare_float(
                f"area of the section at x = {coordinate_x:.1f} by sampling",
                area_sampled,
                area_formula,
                8.0e-3,
                "indicator sampling of the inequalities",
                "closed form (4/3) (1 - x^(3/2))",
            )
        else:
            distinct = np.unique(np.round(corners, 12), axis=0)
            segment_length = max(
                float(np.linalg.norm(distinct[first] - distinct[second]))
                for first in range(distinct.shape[0])
                for second in range(first + 1, distinct.shape[0])
            )
            recorder.compare_float(
                "the section at x = 1 is a segment of length 2",
                segment_length,
                2.0 * float(problem_model.half_width_at_height(0.0)),
                1.0e-12,
                "distance between the printed corner points",
                "width 2 sqrt(1 - z) at the only allowed height",
            )

    # The projection on the plane y = 0: a triangle, taken from an existence test and from the area formula.
    triangle = figure_anchors.projection_polygon()
    area_triangle = problem_model.polygon_area(
        np.column_stack((triangle, np.zeros(triangle.shape[0]))), 0, 1
    )
    area_integral = float(integrate.quad(lambda height: 1.0 - height, 0.0, 1.0)[0])
    recorder.compare_float(
        "area of the projection on the plane y = 0",
        area_triangle,
        area_integral,
        1.0e-12,
        "shoelace formula on the printed corners",
        "integral of the x length 1 - z",
    )

    first_coordinates = GENERATOR.uniform(0.0, 1.0, POINTS_CHECKED_FOR_PROJECTION)
    second_coordinates = GENERATOR.uniform(0.0, 1.0, POINTS_CHECKED_FOR_PROJECTION)
    triangle_test = (
        (first_coordinates >= 0.0)
        & (second_coordinates >= 0.0)
        & (first_coordinates + second_coordinates <= 1.0)
    )
    existence_test = np.zeros(POINTS_CHECKED_FOR_PROJECTION, dtype=bool)
    for coordinate_y in np.linspace(-1.0, 1.0, 401):
        existence_test |= problem_model.point_in_solid_by_width(
            first_coordinates, coordinate_y, second_coordinates
        )
    mismatches = int(np.count_nonzero(triangle_test != existence_test))
    recorder.compare_text(
        "the projection test equals the triangle test",
        f"{mismatches} mismatches in {POINTS_CHECKED_FOR_PROJECTION} pairs",
        f"0 mismatches in {POINTS_CHECKED_FOR_PROJECTION} pairs",
        "existence of a coordinate y on a grid",
        "closed form x + z <= 1 of the triangle",
    )

    recorder.set_value("p1_y_interval", f"$-1 \\le y \\le 1$")
    recorder.set_value("p1_sympy_roots", f"$y = {roots[0]}$ and $y = {roots[1]}$")
    recorder.set_value("p1_projection_area", problem_model.fraction_to_latex(Fraction(1, 2)))
    recorder.set_value("p1_projection_area_decimal", problem_model.format_decimal(area_triangle, 6))
    recorder.set_value("p1_shape_at_z", "a rectangle")
    recorder.set_value("p1_shape_at_y", "a right trapezoid")
    recorder.set_value("p1_shape_at_x", "the region between the two branches of $|y| = \\sqrt{1 - z}$")
    recorder.set_value(
        "p1_corners_at_z_half", problem_model.describe_points(problem_model.corners_at_z(0.5))
    )
    recorder.set_value(
        "p1_corners_at_y_zero", problem_model.describe_points(problem_model.corners_at_y(0.0))
    )
    recorder.set_value(
        "p1_corners_at_x_one", problem_model.describe_points(problem_model.corners_at_x(1.0))
    )
    recorder.set_value(
        "p1_corners_at_z_zero", problem_model.describe_points(problem_model.corners_at_z(0.0))
    )
    recorder.set_value("p1_samples", f"{POINTS_CHECKED_AGAINST_SYMBOL}")
    recorder.set_value("p1_disagreements", f"{disagreements}")
    recorder.set_value(
        "p1_area_at_z_table",
        " | ".join(
            f"$z = {height:.1f}$ : ${float(problem_model.cross_section_area_at_z(height)):.6f}$"
            for height in HEIGHTS_OF_SECTIONS
        ),
    )

    recorder.finish()


if __name__ == "__main__":
    main()
