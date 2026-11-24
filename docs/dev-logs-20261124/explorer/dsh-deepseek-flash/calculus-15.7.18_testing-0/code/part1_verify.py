"""Verify the geometry of Part 1: the solid, its three projections, and its slices.

Method one is a defining inequality: a point belongs to the solid when it satisfies all four bounds.
Method two is an independent count of points, an independent quadrature, or a closed form.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Callable
from pathlib import Path

import numpy as np
from scipy import integrate

from check_registry import CheckRegistry, latex_fraction, write_values
from geometry_anchors import (
    CYLINDER_RADIUS,
    GRID_SIDE,
    MONTE_CARLO_SAMPLE_COUNT,
    PLANE_SLOPE,
    RANDOM_SEED,
    SAMPLE_HEIGHTS_Y,
    SAMPLE_HEIGHTS_Z,
    SHAPE_HEIGHTS_Y,
    SHAPE_HEIGHTS_Z,
    SURFACE_LABEL_POINTS,
)

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"
"""Directory that holds the JSON record of every part."""

COUNTING_TOLERANCE = 8.0e-3
"""Largest accepted relative difference of a counting grid against a closed form."""

OUTSIDE_TOLERANCE = 1.0e-12
"""Largest accepted arithmetic error of a point that should lie on a boundary surface."""

SNAP_DECIMALS = 9
"""Number of decimals that identifies two corner points of a slice."""


def inside_solid(
    x: np.ndarray, y: np.ndarray, z: np.ndarray, tolerance: float = 1.0e-12
) -> np.ndarray:
    """Return a mask that is true where the point satisfies the four defining inequalities.

    Args:
        x: Array of the first coordinate.
        y: Array of the second coordinate.
        z: Array of the third coordinate.
        tolerance: Slack that absorbs the rounding of a printed coordinate.
    """
    return (
        (y * y + z * z <= CYLINDER_RADIUS**2 + tolerance)
        & (x >= -tolerance)
        & (y >= PLANE_SLOPE * x - tolerance)
        & (z >= -tolerance)
    )


def area_by_counting(
    inside_mask: Callable[[np.ndarray, np.ndarray], np.ndarray], first_range: tuple[float, float], second_range: tuple[float, float]
) -> float:
    """Return the area of a plane region by a count of a regular grid of cell centres.

    Args:
        inside_mask: Function of two coordinate arrays that returns a boolean mask.
        first_range: Lowest and highest value of the first coordinate of a bounding rectangle.
        second_range: Lowest and highest value of the second coordinate of a bounding rectangle.
    """
    first = np.linspace(first_range[0], first_range[1], GRID_SIDE)
    second = np.linspace(second_range[0], second_range[1], GRID_SIDE)
    first_step = (first_range[1] - first_range[0]) / (GRID_SIDE - 1)
    second_step = (second_range[1] - second_range[0]) / (GRID_SIDE - 1)
    grid_first, grid_second = np.meshgrid(first, second)
    return float(np.count_nonzero(inside_mask(grid_first, grid_second)) * first_step * second_step)


def volume_by_counting() -> float:
    """Return the volume of the solid by a count of one random point in each cell of a grid.

    One random point in each cell removes the first-order bias that a cell-centre count has
    at a slanted boundary, so the estimate carries noise of order one tenth of one percent.
    """
    side = 240
    generator = np.random.default_rng(RANDOM_SEED)
    x_step = 1.0 / side
    y_step = CYLINDER_RADIUS / side
    z_step = CYLINDER_RADIUS / side
    cell = x_step * y_step * z_step
    row_index, column_index = np.meshgrid(np.arange(side), np.arange(side), indexing="ij")
    total = 0
    for slice_index in range(side):
        z_value = (slice_index + generator.random()) * z_step
        x_value = (row_index + generator.random((side, side))) * x_step
        y_value = (column_index + generator.random((side, side))) * y_step
        total += int(np.count_nonzero(inside_solid(x_value, y_value, z_value)))
    return float(total * cell)


def volume_by_monte_carlo() -> tuple[float, float]:
    """Return the volume of the solid and the standard error of one Monte Carlo estimate."""
    generator = np.random.default_rng(RANDOM_SEED)
    box_volume = 1.0 * CYLINDER_RADIUS * CYLINDER_RADIUS
    x = generator.uniform(0.0, 1.0, MONTE_CARLO_SAMPLE_COUNT)
    y = generator.uniform(0.0, CYLINDER_RADIUS, MONTE_CARLO_SAMPLE_COUNT)
    z = generator.uniform(0.0, CYLINDER_RADIUS, MONTE_CARLO_SAMPLE_COUNT)
    indicator = inside_solid(x, y, z).astype(float)
    mean = float(indicator.mean())
    standard_error = float(indicator.std(ddof=1) / math.sqrt(MONTE_CARLO_SAMPLE_COUNT))
    return box_volume * mean, box_volume * standard_error


def slice_at_fixed_y(height: float) -> dict[str, object]:
    """Return the corners, the kind, and the area of the slice of the solid at one height y.

    The derivation reads the two inequalities y^2 + z^2 <= 9 and 3x <= y with z >= 0 and x >= 0.
    For a fixed y in the closed interval from 0 to 3 they give 0 <= x <= y/3 and 0 <= z <= sqrt(9-y^2).

    Args:
        height: Value of the coordinate y, from 0 to 3.
    """
    x_high = height / PLANE_SLOPE
    z_high = math.sqrt(max(CYLINDER_RADIUS**2 - height * height, 0.0))
    corners = [
        (0.0, height, 0.0),
        (x_high, height, 0.0),
        (x_high, height, z_high),
        (0.0, height, z_high),
    ]
    kind, unique_corners = classify_corners(corners)
    return {
        "parameter": "y",
        "value": height,
        "corners": unique_corners,
        "kind": kind,
        "area": x_high * z_high,
        "x_high": x_high,
        "z_high": z_high,
    }


def slice_at_fixed_z(height: float) -> dict[str, object]:
    """Return the corners, the kind, and the area of the slice of the solid at one height z.

    For a fixed z the bounds y^2 <= 9 - z^2 and 3x <= y give a triangle with the corners
    (0, 0), (0, sqrt(9-z^2)), and (sqrt(9-z^2)/3, sqrt(9-z^2)) in the plane of that z.

    Args:
        height: Value of the coordinate z, from 0 to 3.
    """
    y_high = math.sqrt(max(CYLINDER_RADIUS**2 - height * height, 0.0))
    corners = [
        (0.0, 0.0, height),
        (0.0, y_high, height),
        (y_high / PLANE_SLOPE, y_high, height),
    ]
    kind, unique_corners = classify_corners(corners)
    return {
        "parameter": "z",
        "value": height,
        "corners": unique_corners,
        "kind": kind,
        "area": 0.5 * y_high * (y_high / PLANE_SLOPE),
        "y_high": y_high,
    }


def classify_corners(corners: list[tuple[float, float, float]]) -> tuple[str, list[tuple[float, float, float]]]:
    """Name the shape of one slice from its corner list.

    Args:
        corners: Corner points that the bounds of the slice produce, with repeats allowed.
    """
    unique: list[tuple[float, float, float]] = []
    for corner in corners:
        snapped = tuple(round(coordinate, SNAP_DECIMALS) for coordinate in corner)
        if snapped not in unique:
            unique.append(snapped)
    if len(unique) == 1:
        return "point", unique
    if len(unique) == 2:
        return "segment", unique
    if len(unique) == 3:
        return "triangle", unique
    if len(unique) == 4:
        first_edge = np.subtract(unique[1], unique[0])
        second_edge = np.subtract(unique[3], unique[0])
        if abs(float(np.dot(first_edge, second_edge))) <= 1.0e-9:
            return "rectangle", unique
        return "quadrilateral", unique
    return "polygon", unique


def slice_area_by_counting(parameter: str, value: float) -> float:
    """Return the area of one slice by a count of a grid inside the slice.

    Args:
        parameter: Name of the fixed coordinate, "y" or "z".
        value: Fixed value of that coordinate.
    """
    if parameter == "y":
        x_high = value / PLANE_SLOPE
        z_high = math.sqrt(max(CYLINDER_RADIUS**2 - value * value, 0.0))
        if x_high == 0.0 or z_high == 0.0:
            return 0.0
        return area_by_counting(
            lambda first, second: (first >= 0.0) & (first <= x_high) & (second >= 0.0) & (second <= z_high),
            (0.0, x_high),
            (0.0, z_high),
        )
    y_high = math.sqrt(max(CYLINDER_RADIUS**2 - value * value, 0.0))
    if y_high == 0.0:
        return 0.0
    return area_by_counting(
        lambda first, second: (first >= 0.0) & (PLANE_SLOPE * first <= second) & (second <= y_high),
        (0.0, y_high / PLANE_SLOPE),
        (0.0, y_high),
    )


def main() -> None:
    """Run every check of Part 1 and write the values of the part."""
    registry = CheckRegistry("part1")
    values: dict[str, object] = {}

    quarter_disk = math.pi * CYLINDER_RADIUS**2 / 4.0
    quarter_disk_quad = integrate.quad(
        lambda z: math.sqrt(CYLINDER_RADIUS**2 - z * z), 0.0, CYLINDER_RADIUS, limit=200
    )[0]
    quarter_disk_count = area_by_counting(
        lambda y, z: (y * y + z * z <= CYLINDER_RADIUS**2) & (y >= 0.0) & (z >= 0.0),
        (0.0, CYLINDER_RADIUS),
        (0.0, CYLINDER_RADIUS),
    )
    registry.compare(
        "part1.yz_projection_quad",
        quarter_disk_quad,
        quarter_disk,
        1.0e-10,
        "Quadrature of sqrt(9-z^2) against the closed form pi*r^2/4.",
    )
    registry.compare(
        "part1.yz_projection_count",
        quarter_disk_count,
        quarter_disk,
        COUNTING_TOLERANCE,
        "Grid count of the quarter disk against the closed form pi*r^2/4.",
    )

    xz_area = math.pi * CYLINDER_RADIUS**2 / 12.0
    xz_quad = integrate.quad(
        lambda z: math.sqrt(max(CYLINDER_RADIUS**2 - z * z, 0.0)) / PLANE_SLOPE, 0.0, CYLINDER_RADIUS, limit=200
    )[0]
    xz_count = area_by_counting(
        lambda x, z: (z >= 0.0)
        & (z <= CYLINDER_RADIUS)
        & (x >= 0.0)
        & (PLANE_SLOPE * x <= np.sqrt(np.maximum(CYLINDER_RADIUS**2 - z * z, 0.0))),
        (0.0, CYLINDER_RADIUS / PLANE_SLOPE),
        (0.0, CYLINDER_RADIUS),
    )
    registry.compare(
        "part1.xz_projection_quad", xz_quad, xz_area, 1.0e-10, "Quadrature of sqrt(9-z^2)/3 against pi*r^2/12."
    )
    registry.compare(
        "part1.xz_projection_count",
        xz_count,
        xz_area,
        COUNTING_TOLERANCE,
        "Grid count of the xz region against the closed form pi*r^2/12.",
    )

    xy_area = CYLINDER_RADIUS**2 / (2.0 * PLANE_SLOPE)
    xy_quad = integrate.quad(lambda y: y / PLANE_SLOPE, 0.0, CYLINDER_RADIUS, limit=200)[0]
    xy_count = area_by_counting(
        lambda x, y: (x >= 0.0) & (y >= PLANE_SLOPE * x) & (y <= CYLINDER_RADIUS),
        (0.0, CYLINDER_RADIUS / PLANE_SLOPE),
        (0.0, CYLINDER_RADIUS),
    )
    registry.compare(
        "part1.xy_projection_quad", xy_quad, xy_area, 1.0e-10, "Quadrature of y/3 against the triangle area r^2/(2m)."
    )
    registry.compare(
        "part1.xy_projection_count",
        xy_count,
        xy_area,
        COUNTING_TOLERANCE,
        "Grid count of the xy triangle against the closed form r^2/(2m).",
    )

    volume_exact = Fraction(int(CYLINDER_RADIUS) ** 3, int(3 * PLANE_SLOPE))
    volume_closed = float(volume_exact)
    volume_slice_y = integrate.quad(
        lambda y: (y / PLANE_SLOPE) * math.sqrt(max(CYLINDER_RADIUS**2 - y * y, 0.0)), 0.0, CYLINDER_RADIUS
    )[0]
    volume_slice_z = integrate.quad(
        lambda z: (CYLINDER_RADIUS**2 - z * z) / (2.0 * PLANE_SLOPE), 0.0, CYLINDER_RADIUS
    )[0]
    volume_count = volume_by_counting()
    volume_monte_carlo, volume_standard_error = volume_by_monte_carlo()
    registry.compare(
        "part1.volume_slice_y",
        volume_slice_y,
        volume_closed,
        1.0e-10,
        "Quadrature of the slice area at fixed y against the closed form r^3/(3m).",
    )
    registry.compare(
        "part1.volume_slice_z",
        volume_slice_z,
        volume_closed,
        1.0e-10,
        "Quadrature of the slice area at fixed z against the closed form r^3/(3m).",
    )
    registry.compare(
        "part1.volume_slice_pair",
        volume_slice_z,
        volume_slice_y,
        1.0e-10,
        "Two different slicings of the same solid must give one volume.",
    )
    registry.compare(
        "part1.volume_count",
        volume_count,
        volume_closed,
        COUNTING_TOLERANCE,
        "Count of one random point per cell of a 240-cube grid against the closed form r^3/(3m).",
    )
    registry.compare(
        "part1.volume_monte_carlo",
        volume_monte_carlo,
        volume_closed,
        5.0e-3,
        "Monte Carlo estimate against the closed form, inside five standard errors.",
    )
    standard_error_ratio = abs(volume_monte_carlo - volume_closed) / volume_standard_error

    for height in SAMPLE_HEIGHTS_Y:
        row = slice_at_fixed_y(height)
        registry.compare(
            f"part1.slice_y_{height}_count",
            slice_area_by_counting("y", height),
            float(row["area"]),
            COUNTING_TOLERANCE,
            "Grid count inside the slice at fixed y against the closed form (y/3)*sqrt(9-y^2).",
        )
    for height in SAMPLE_HEIGHTS_Z:
        row = slice_at_fixed_z(height)
        if float(row["area"]) > 0.0:
            registry.compare(
                f"part1.slice_z_{height}_count",
                slice_area_by_counting("z", height),
                float(row["area"]),
                COUNTING_TOLERANCE,
                "Grid count inside the slice at fixed z against the closed form (9-z^2)/6.",
            )

    shape_rows: list[dict[str, object]] = []
    for height in SHAPE_HEIGHTS_Y:
        shape_rows.append(slice_at_fixed_y(height))
    for height in SHAPE_HEIGHTS_Z:
        shape_rows.append(slice_at_fixed_z(height))

    for row in shape_rows:
        for corner in row["corners"]:
            inside = bool(
                inside_solid(*(np.array([[coordinate]]) for coordinate in corner), tolerance=1.0e-6)
            )
            if not inside:
                raise AssertionError(f"corner {corner} of the slice at {row['parameter']} is outside the solid")
        print(
            f"slice at {row['parameter']} = {row['value']}: corners={row['corners']} "
            f"kind={row['kind']} area={row['area']:.9f}"
        )

    registry.compare(
        "part1.slice_y_rectangle_count",
        float(sum(1 for row in shape_rows if row["kind"] == "rectangle")),
        1.0,
        1.0e-12,
        "One interior slice at fixed y must be a rectangle, the count of the corner list gives one.",
    )
    registry.compare(
        "part1.slice_z_triangle_count",
        float(sum(1 for row in shape_rows if row["kind"] == "triangle")),
        2.0,
        1.0e-12,
        "Two interior slices at fixed z must be triangles, the count of the corner list gives two.",
    )
    registry.compare(
        "part1.slice_y_degenerate_count",
        float(sum(1 for row in shape_rows if row["kind"] == "segment")),
        2.0,
        1.0e-12,
        "The two limits of y must give a segment, the count of the corner list gives two.",
    )

    for name, point in SURFACE_LABEL_POINTS.items():
        x, y, z = point
        if name == "cylinder":
            residual = y * y + z * z - CYLINDER_RADIUS**2
        elif name == "plane_x_zero":
            residual = x
        elif name == "plane_y_three_x":
            residual = y - PLANE_SLOPE * x
        else:
            residual = z
        registry.compare_absolute(
            f"part1.label_point_{name}_on_surface",
            abs(residual),
            0.0,
            1.0e-12,
            "Equation residual of the label point against zero, the point must lie on its surface.",
        )
        if not bool(inside_solid(np.array([x]), np.array([y]), np.array([z]))):
            raise AssertionError(f"label point {point} of {name} is outside the solid")

    registry.write(OUTPUT_DIRECTORY / "part1_checks.json")
    values.update(
        {
            "p1_yz_area_latex": f"\\dfrac{{9\\pi}}{{4}}",
            "p1_yz_area_decimal": f"{quarter_disk:.9f}",
            "p1_xz_area_latex": f"\\dfrac{{3\\pi}}{{4}}",
            "p1_xz_area_decimal": f"{xz_area:.9f}",
            "p1_xy_area_latex": latex_fraction(3, 2),
            "p1_xy_area_decimal": f"{xy_area:.9f}",
            "p1_volume_latex": latex_fraction(volume_exact.numerator, volume_exact.denominator),
            "p1_volume_decimal": f"{volume_closed:.9f}",
            "p1_volume_monte_carlo": f"{volume_monte_carlo:.9f}",
            "p1_volume_standard_error": f"{volume_standard_error:.9f}",
            "p1_volume_standard_error_ratio": f"{standard_error_ratio:.6f}",
            "p1_volume_count": f"{volume_count:.9f}",
            "p1_shape_rows": [
                {
                    "parameter": row["parameter"],
                    "value": f"{float(row['value']):.3f}",
                    "kind": str(row["kind"]),
                    "corners": "; ".join(
                        "(" + ", ".join(f"{coordinate:.3f}" for coordinate in corner) + ")"
                        for corner in row["corners"]
                    ),
                    "corner_count": str(len(row["corners"])),
                    "area": f"{float(row['area']):.9f}",
                }
                for row in shape_rows
            ],
            "p1_check_count": str(registry.passed_count()),
        }
    )
    write_values(OUTPUT_DIRECTORY / "part1_values.json", values)


if __name__ == "__main__":
    main()
