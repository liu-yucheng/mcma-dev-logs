"""Verify the solid region E and its projection on the plane z = 0.

The script derives every statement of Part 1 from the two defining surfaces,
z = 1 - x^2 - y^2 and z = 0. Each check compares a value that one method
computes with a value that a different method computes. Run the script with the
interpreter of the session environment.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from matplotlib.path import Path
from scipy.optimize import minimize_scalar

BISECTION_STEPS = 200
PROJECTION_SAMPLES = 481
POLYGON_VERTICES = 720
GRID_SAMPLES = 1201
VOLUME_SAMPLES = 201
NUMERICAL_TOLERANCE = 1.0e-9
AREA_TOLERANCE = 5.0e-3
VOLUME_TOLERANCE = 2.0e-2


def paraboloid_height(radius_squared: float) -> float:
    """Return the height of the paraboloid z = 1 - r^2 above a point of radius r."""
    return 1.0 - radius_squared


def find_root_by_bisection(function, lower: float, upper: float, steps: int) -> float:
    """Return one root of a monotone function on an interval that changes sign."""
    low = float(lower)
    high = float(upper)
    if function(low) * function(high) > 0.0:
        raise ValueError("the interval does not change sign")
    for _ in range(steps):
        middle = 0.5 * (low + high)
        if function(low) * function(middle) <= 0.0:
            high = middle
        else:
            low = middle
    return 0.5 * (low + high)


def intersection_curve(vertex_count: int) -> np.ndarray:
    """Return the curve where the paraboloid meets the plane, found by a root search.

    Each ray at an angle theta is scanned from radius 0 to radius 3, and the
    crossing of the height function through zero is located by bisection. The
    method reads the two surfaces only, so it does not use the closed form of
    the radius.
    """
    angles = np.linspace(0.0, 2.0 * math.pi, vertex_count, endpoint=False)
    radii: list[float] = []
    for angle in angles:
        direction = (math.cos(angle), math.sin(angle))
        radius = find_root_by_bisection(
            lambda r: paraboloid_height((direction[0] * r) ** 2 + (direction[1] * r) ** 2),
            0.0,
            3.0,
            BISECTION_STEPS,
        )
        radii.append(radius)
    radius_array = np.asarray(radii)
    return np.column_stack((radius_array * np.cos(angles), radius_array * np.sin(angles)))


def polygon_area(vertices: np.ndarray) -> float:
    """Return the area of a closed polygon with the shoelace formula."""
    x_values = vertices[:, 0]
    y_values = vertices[:, 1]
    return 0.5 * abs(float(np.dot(x_values, np.roll(y_values, -1)) - np.dot(y_values, np.roll(x_values, -1))))


def classify_section(radius_squared: float) -> str:
    """Return the shape of the vertical section at one radius squared.

    The section at a point of radius squared s is the closed interval from z = 0
    to z = 1 - s. The function reports the shape from the length of that
    interval, so the word in the tutorial follows the computed interval.
    """
    upper = paraboloid_height(radius_squared)
    if upper < 0.0:
        return "empty"
    if upper == 0.0:
        return "point"
    return "segment"


def main() -> None:
    """Run every check of Part 1 and print each computed value beside its reference."""
    # BEGIN CHECK boundary_radius
    radius_by_root_search = find_root_by_bisection(lambda r: paraboloid_height(r * r), 0.5, 2.0, BISECTION_STEPS)
    radius_by_closed_form = float(Fraction(1, 1)) ** 0.5
    print("boundary radius by bisection on the surfaces :", radius_by_root_search)
    print("boundary radius by the closed form sqrt(1)   :", radius_by_closed_form)
    assert abs(radius_by_root_search - radius_by_closed_form) < NUMERICAL_TOLERANCE
    # END CHECK boundary_radius

    # BEGIN CHECK projection_membership
    curve = intersection_curve(POLYGON_VERTICES)
    polygon = Path(curve)
    axis = np.linspace(-1.3, 1.3, PROJECTION_SAMPLES)
    grid_x, grid_y = np.meshgrid(axis, axis)
    sample_points = np.column_stack((grid_x.ravel(), grid_y.ravel()))
    inside_by_polygon = polygon.contains_points(sample_points)
    inside_by_inequality = (sample_points[:, 0] ** 2 + sample_points[:, 1] ** 2) <= 1.0
    disagreement = int(np.count_nonzero(inside_by_polygon != inside_by_inequality))
    print("plane points tested                          :", sample_points.shape[0])
    print("disagreements between polygon test and disk  :", disagreement)
    assert disagreement == 0
    # END CHECK projection_membership

    # BEGIN CHECK projection_area
    area_by_polygon = polygon_area(curve)
    area_by_grid = float(np.count_nonzero(inside_by_inequality)) * (axis[1] - axis[0]) ** 2
    radii = np.linspace(0.0, 1.0, GRID_SAMPLES)
    area_by_radial_integral = float(np.trapezoid(2.0 * math.pi * radii, radii))
    area_by_reference = math.pi
    print("area of the projection by shoelace           :", area_by_polygon)
    print("area of the projection by grid count         :", area_by_grid)
    print("area of the projection by the radial integral:", area_by_radial_integral)
    print("area of the unit disk, pi                    :", area_by_reference)
    assert abs(area_by_polygon - area_by_reference) < 1.0e-4
    assert abs(area_by_grid - area_by_reference) / area_by_reference < AREA_TOLERANCE
    assert abs(area_by_radial_integral - area_by_reference) / area_by_reference < AREA_TOLERANCE
    # END CHECK projection_area

    # BEGIN CHECK section_shapes
    printed_shapes = []
    for radius_squared in (0.0, 0.25, 0.75, 1.0, 1.44):
        upper = paraboloid_height(radius_squared)
        shape = classify_section(radius_squared)
        printed_shapes.append(shape)
        print(
            "radius squared",
            radius_squared,
            "corners (z lower, z upper) =",
            (0.0, upper),
            "shape =",
            shape,
        )
    assert printed_shapes == ["segment", "segment", "segment", "point", "empty"]
    # END CHECK section_shapes

    # BEGIN CHECK height_extreme
    grid_radius = np.linspace(0.0, 1.0, 4001)
    grid_heights = paraboloid_height(grid_radius**2)
    grid_maximum = float(np.max(grid_heights))
    optimised = minimize_scalar(lambda r: -paraboloid_height(r * r), bounds=(0.0, 1.0), method="bounded")
    optimised_maximum = -float(optimised.fun)
    print("largest height over the disk, grid           :", grid_maximum)
    print("largest height over the disk, bounded search  :", optimised_maximum)
    print("height at the disk centre, closed form        :", paraboloid_height(0.0))
    assert abs(grid_maximum - optimised_maximum) < NUMERICAL_TOLERANCE
    assert abs(optimised_maximum - 1.0) < NUMERICAL_TOLERANCE
    assert float(np.min(grid_heights)) >= -NUMERICAL_TOLERANCE
    # END CHECK height_extreme

    # BEGIN CHECK volume_by_cell_count
    cell_axis = np.linspace(-1.0, 1.0, VOLUME_SAMPLES)
    cell_x, cell_y = np.meshgrid(cell_axis, cell_axis)
    cell_radius_squared = cell_x**2 + cell_y**2
    cell_height = np.maximum(0.0, paraboloid_height(cell_radius_squared))
    volume_by_cells = float(np.sum(cell_height)) * (cell_axis[1] - cell_axis[0]) ** 2
    volume_reference = math.pi / 2.0
    print("volume of E by a column sum                  :", volume_by_cells)
    print("volume of E, pi / 2                          :", volume_reference)
    assert abs(volume_by_cells - volume_reference) / volume_reference < VOLUME_TOLERANCE
    # END CHECK volume_by_cell_count

    print("part1_verify: all checks passed")


if __name__ == "__main__":
    main()
