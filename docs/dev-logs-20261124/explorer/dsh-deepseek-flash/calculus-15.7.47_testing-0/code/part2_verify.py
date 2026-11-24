"""Checks of Part 2: the two families of cross sections and their shapes.

Run with the environment interpreter: code/.venv/Scripts/python.exe code/part2_verify.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors
import integration_tools
from check_tools import CheckRecorder, format_number

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"
NODE_COUNT = 60


def rectangle_area_by_quadrature(y: float) -> float:
    """Return the area of the section at one y by a quadrature over the rectangle.

    Args:
        y: Value of the second coordinate.

    Returns:
        The area of the rectangle |x| <= sqrt(y), 0 <= z <= 1 - y.
    """
    half_width = math.sqrt(y)
    height = 1.0 - y
    nodes, weights = np.polynomial.legendre.leggauss(NODE_COUNT)
    total = float(np.sum(weights)) * float(np.sum(weights))
    return half_width * 0.5 * height * total


def parabolic_area_by_quadrature(z: float) -> float:
    """Return the area of the section at one z by a quadrature over the region.

    The region is x^2 <= y <= 1 - z with |x| <= sqrt(1 - z).

    Args:
        z: Value of the third coordinate.

    Returns:
        The area of the parabolic section.
    """
    extent = math.sqrt(max(0.0, 1.0 - z))
    upper_y = 1.0 - z
    nodes, weights = np.polynomial.legendre.leggauss(NODE_COUNT)
    total = 0.0
    for node_x, weight_x in zip(nodes, weights):
        x = extent * float(node_x)
        lower_y = x * x
        total += float(weight_x) * (upper_y - lower_y)
    return extent * total


def section_corners_at_y(y: float) -> list[tuple[float, float, float]]:
    """Return the extreme points of the rectangle of the section at one y.

    Args:
        y: Value of the second coordinate.

    Returns:
        Four points, in the order low x with z = 0, high x with z = 0, high x
        with the largest z, and low x with the largest z.
    """
    half_width = math.sqrt(y)
    height = 1.0 - y
    return [
        (-half_width, y, 0.0),
        (half_width, y, 0.0),
        (half_width, y, height),
        (-half_width, y, height),
    ]


def section_corners_at_z(z: float) -> list[tuple[float, float, float]]:
    """Return the extreme points of the parabolic section at one z.

    Args:
        z: Value of the third coordinate.

    Returns:
        The two rim points and the apex point of the section.
    """
    extent = math.sqrt(max(0.0, 1.0 - z))
    return [(-extent, 1.0 - z, z), (extent, 1.0 - z, z), (0.0, 0.0, z)]


def describe_shape(corners: list[tuple[float, float, float]]) -> str:
    """Return the name of the shape that a corner list closes.

    Args:
        corners: Extreme points of one section.

    Returns:
        A short name with the measured sizes, taken from the corner coordinates.
    """
    extent_x = max(point[0] for point in corners) - min(point[0] for point in corners)
    extent_z = max(point[2] for point in corners) - min(point[2] for point in corners)
    if abs(extent_x) < 1e-12 and abs(extent_z) < 1e-12:
        return "one point"
    if abs(extent_z) < 1e-12:
        return f"segment along x of length {format_number(extent_x, 6)}"
    if abs(extent_x) < 1e-12:
        return f"vertical segment of length {format_number(extent_z, 6)}"
    return f"face of width {format_number(extent_x, 6)} and height {format_number(extent_z, 6)}"


def describe_shape_at_z(corners: list[tuple[float, float, float]]) -> str:
    """Return the name of the shape that a corner list of a section at fixed z closes.

    The two coordinates that can vary inside a section at a fixed z are x and y.

    Args:
        corners: Extreme points of one section at a fixed z.

    Returns:
        A short name with the measured sizes, taken from the corner coordinates.
    """
    extent_x = max(point[0] for point in corners) - min(point[0] for point in corners)
    extent_y = max(point[1] for point in corners) - min(point[1] for point in corners)
    if abs(extent_x) < 1e-12 and abs(extent_y) < 1e-12:
        return "one point"
    if abs(extent_y) < 1e-12:
        return f"segment along x of length {format_number(extent_x, 6)}"
    if abs(extent_x) < 1e-12:
        return f"vertical segment of length {format_number(extent_y, 6)}"
    return (
        f"parabolic segment of width {format_number(extent_x, 6)} in x"
        f" and height {format_number(extent_y, 6)} in y"
    )


def main() -> None:
    """Run every check of Part 2 and write the record of the part."""
    recorder = CheckRecorder("part2", OUTPUT_DIRECTORY)

    for y in figure_anchors.Y_SLICES:
        recorder.compare(
            f"rectangle_area_at_y_equal_{y}",
            integration_tools.slice_area_at_y(y),
            rectangle_area_by_quadrature(y),
            1e-9,
            "the closed-form area $2\\sqrt{y}(1 - y)$ against a quadrature over the same rectangle",
        )
    for z in figure_anchors.Z_SLICES:
        recorder.compare(
            f"parabolic_area_at_z_equal_{z}",
            integration_tools.slice_area_at_z(z),
            parabolic_area_by_quadrature(z),
            1e-9,
            "the closed-form area $\\frac{4}{3}(1 - z)^{3/2}$ against a quadrature over the same section",
        )

    stacked, _ = quad(integration_tools.slice_area_at_z, 0.0, 1.0, points=[1.0], epsabs=1e-12, epsrel=1e-12)
    volume_from_order = integration_tools.integrate_order("dz dy dx")["volume"]
    recorder.compare(
        "stacked_section_area_against_volume",
        float(stacked),
        volume_from_order,
        1e-8,
        "the integral of the section area over $z$ against the volume of the order $dz\\,dy\\,dx$",
    )

    shapes_y = {y: describe_shape(section_corners_at_y(y)) for y in figure_anchors.BOUNDARY_Y_VALUES}
    shapes_z = {z: describe_shape_at_z(section_corners_at_z(z)) for z in figure_anchors.BOUNDARY_Z_VALUES}

    corner_y_one = section_corners_at_y(1.0)
    length_at_y_one = max(point[0] for point in corner_y_one) - min(point[0] for point in corner_y_one)
    recorder.compare(
        "section_at_y_one_is_a_segment",
        length_at_y_one,
        2.0 * math.sqrt(1.0),
        1e-12,
        "the corner list at $y = 1$ against the width $2\\sqrt{y}$ of the rectangle",
    )
    corner_z_one = section_corners_at_z(1.0)
    spread_at_z_one = max(abs(point[0]) + abs(point[1]) for point in corner_z_one)
    recorder.compare(
        "section_at_z_one_is_one_point",
        spread_at_z_one,
        0.0,
        1e-12,
        "the corner list at $z = 1$ against the single point of zero extent",
    )
    area_at_y_zero = integration_tools.slice_area_at_y(0.0)
    recorder.compare(
        "section_at_y_zero_is_a_segment",
        area_at_y_zero,
        0.0,
        1e-12,
        "the closed-form area at $y = 0$ against zero, which marks a segment and not a face",
    )

    recorder.set_display("p2_z_slices", ", ".join(format_number(z, 1) for z in figure_anchors.Z_SLICES))
    recorder.set_display("p2_y_slices", ", ".join(format_number(y, 2) for y in figure_anchors.Y_SLICES))
    recorder.set_display(
        "p2_area_z_list",
        ", ".join(format_number(integration_tools.slice_area_at_z(z)) for z in figure_anchors.Z_SLICES),
    )
    recorder.set_display(
        "p2_area_y_list",
        ", ".join(format_number(integration_tools.slice_area_at_y(y)) for y in figure_anchors.Y_SLICES),
    )
    recorder.set_display("p2_stacked_area", format_number(float(stacked)))
    recorder.set_display("p2_shape_y_list", "; ".join(f"y = {y}: {shapes_y[y]}" for y in figure_anchors.BOUNDARY_Y_VALUES))
    recorder.set_display("p2_shape_z_list", "; ".join(f"z = {z}: {shapes_z[z]}" for z in figure_anchors.BOUNDARY_Z_VALUES))
    recorder.set_display(
        "p2_corner_y_one",
        "; ".join("(" + ", ".join(format_number(value, 3) for value in point) + ")" for point in corner_y_one),
    )
    recorder.set_display(
        "p2_corner_z_one",
        "; ".join("(" + ", ".join(format_number(value, 3) for value in point) + ")" for point in corner_z_one),
    )
    recorder.save()


if __name__ == "__main__":
    main()
