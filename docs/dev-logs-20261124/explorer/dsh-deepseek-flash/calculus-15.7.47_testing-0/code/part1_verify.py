"""Checks of Part 1: the three surfaces, the limits of the solid, and the volume.

Run with the environment interpreter: code/.venv/Scripts/python.exe code/part1_verify.py
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.integrate import quad

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors
import integration_tools
from check_tools import CheckRecorder, format_number

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"


def projection_area_by_integral() -> float:
    """Return the area of the projection on the plane z = 0 by one integral in x.

    Returns:
        The value of the integral of 1 - x^2 over x from -1 to 1.
    """
    value, _ = quad(lambda x: 1.0 - x * x, -1.0, 1.0, epsabs=1e-13, epsrel=1e-13)
    return float(value)


def projection_area_by_shoelace(point_count: int = 200001) -> float:
    """Return the area of the same projection from the shoelace formula.

    Args:
        point_count: Count of points that sample the parabolic boundary.

    Returns:
        The absolute area of the closed polygon of the boundary.
    """
    x = np.linspace(-1.0, 1.0, point_count)
    y = x * x
    area = 0.5 * abs(float(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)))
    return area


def section_area_at_z(z: float, node_count: int = 60) -> float:
    """Return the area of the section at one height by a two-dimensional quadrature.

    Args:
        z: Value of the third coordinate.
        node_count: Count of Gauss-Legendre nodes on each coordinate.

    Returns:
        The area of the section, computed without the closed-form formula.
    """
    extent = math.sqrt(max(0.0, 1.0 - z))
    upper_y = 1.0 - z
    nodes, weights = np.polynomial.legendre.leggauss(node_count)
    total = 0.0
    for node_x, weight_x in zip(nodes, weights):
        x = extent * float(node_x)
        lower_y = x * x
        middle = 0.5 * (lower_y + upper_y)
        half = 0.5 * (upper_y - lower_y)
        total += float(weight_x) * half * float(np.sum(weights))
    return extent * total


def projection_area_yz() -> float:
    """Return the area of the projection on the plane x = 0 by one integral in y.

    Returns:
        The value of the integral of 1 - y over y from 0 to 1.
    """
    value, _ = quad(lambda y: 1.0 - y, 0.0, 1.0, epsabs=1e-13, epsrel=1e-13)
    return float(value)


def grid_extremes(point_count: int = 121) -> dict[str, float]:
    """Return the extreme coordinates of the grid points that belong to the solid.

    Args:
        point_count: Count of grid points on each coordinate.

    Returns:
        One dictionary with the smallest x, the largest x, and the largest y.
    """
    axis_x = np.linspace(-1.0, 1.0, point_count)
    axis_y = np.linspace(0.0, 1.0, point_count)
    axis_z = np.linspace(0.0, 1.0, point_count)
    grid_x, grid_y, grid_z = np.meshgrid(axis_x, axis_y, axis_z, indexing="ij")
    mask = integration_tools.inside_solid(grid_x, grid_y, grid_z)
    return {
        "min_x": float(grid_x[mask].min()),
        "max_x": float(grid_x[mask].max()),
        "max_y": float(grid_y[mask].max()),
        "min_y": float(grid_y[mask].min()),
        "point_count": float(mask.size),
        "inside_count": float(np.count_nonzero(mask)),
    }


def membership_masks_agree(sample_count: int = 300_000) -> int:
    """Return the count of points where two descriptions of the solid disagree.

    The first description uses the three defining inequalities. The second
    description uses the limits of the order dz dy dx.

    Args:
        sample_count: Count of uniform samples of the box around the solid.

    Returns:
        The count of samples that one description accepts and the other rejects.
    """
    generator = np.random.default_rng(20261124)
    x = generator.uniform(-1.0, 1.0, sample_count)
    y = generator.uniform(0.0, 1.0, sample_count)
    z = generator.uniform(0.0, 1.0, sample_count)
    by_inequalities = integration_tools.inside_solid(x, y, z)
    by_limits = (
        (x >= -1.0)
        & (x <= 1.0)
        & (y >= x * x)
        & (y <= 1.0)
        & (z >= 0.0)
        & (z <= 1.0 - y)
    )
    return int(np.count_nonzero(by_inequalities != by_limits))


def main() -> None:
    """Run every check of Part 1 and write the record of the part."""
    recorder = CheckRecorder("part1", OUTPUT_DIRECTORY)

    residuals = figure_anchors.residuals()
    largest_residual = max(abs(value) for value in residuals.values())
    recorder.compare(
        "label_points_on_their_surfaces",
        largest_residual,
        0.0,
        1e-12,
        "the equation of each surface is evaluated at the point where Figure 1 writes its label",
    )

    area_integral = projection_area_by_integral()
    area_shoelace = projection_area_by_shoelace()
    recorder.compare(
        "projection_area_integral_against_shoelace",
        area_integral,
        area_shoelace,
        1e-9,
        "one integral in x and one polygon area of the same boundary",
    )
    recorder.compare(
        "projection_area_against_exact_third",
        area_integral,
        float(Fraction(4, 3)),
        1e-10,
        "the quadrature against the exact fraction 4/3 of the same integral",
    )

    recorder.compare(
        "section_area_at_zero_against_projection",
        section_area_at_z(0.0),
        area_integral,
        1e-9,
        "a two-dimensional quadrature of the section at $z = 0$ against the one-dimensional projection integral",
    )

    area_yz = projection_area_yz()
    recorder.compare(
        "yz_projection_area_against_triangle",
        area_yz,
        0.5,
        1e-12,
        "the integral of $1 - y$ against the area of the right triangle with legs of length one",
    )

    first_order = integration_tools.integrate_order("dz dy dx")
    second_order = integration_tools.integrate_order("dy dz dx")
    recorder.compare(
        "volume_of_two_orders",
        first_order["volume"],
        second_order["volume"],
        1e-9,
        "the order $dz\\,dy\\,dx$ against the order $dy\\,dz\\,dx$",
    )
    recorder.compare(
        "volume_against_exact_fraction",
        first_order["volume"],
        float(Fraction(8, 15)),
        1e-9,
        "the nested quadrature against the exact fraction $\\frac{8}{15}$",
    )
    monte_carlo = integration_tools.integrate_monte_carlo()
    volume_gap = abs(monte_carlo["volume"] - float(Fraction(8, 15)))
    recorder.compare_bound(
        "volume_monte_carlo_inside_three_errors",
        volume_gap,
        3.0 * monte_carlo["volume_standard_error"],
        "the gap between the Monte Carlo estimate and $\\frac{8}{15}$ against three standard errors",
    )

    extremes = grid_extremes()
    recorder.compare_bound("grid_y_at_most_one", extremes["max_y"], 1.0, "the plane $y + z = 1$ with $z \\ge 0$")
    recorder.compare(
        "grid_y_attains_one",
        extremes["max_y"],
        1.0,
        0.0,
        "the largest y of the grid against the intercept $y = 1$ of the plane at $z = 0$",
    )
    recorder.compare_bound("grid_x_at_most_one", extremes["max_x"], 1.0, "the bound $x^{2} \\le y \\le 1$")
    recorder.compare_bound("grid_minus_x_at_most_one", -extremes["min_x"], 1.0, "the bound $x^{2} \\le y \\le 1$")
    recorder.compare(
        "grid_x_attains_minus_one", extremes["min_x"], -math.sqrt(extremes["max_y"]), 0.0, "$x^{2} \\le 1$ at $y = 1$"
    )
    recorder.compare(
        "grid_x_attains_one", extremes["max_x"], math.sqrt(extremes["max_y"]), 0.0, "$x^{2} \\le 1$ at $y = 1$"
    )
    recorder.compare(
        "membership_masks_agree",
        float(membership_masks_agree()),
        0.0,
        0.0,
        "the three defining inequalities against the limits of the order $dz\\,dy\\,dx$ on 300000 samples",
    )

    recorder.set_display("p1_x_min_text", format_number(-math.sqrt(extremes["max_y"]), 0))
    recorder.set_display("p1_x_max_text", format_number(extremes["max_x"], 0))
    recorder.set_display("p1_y_min_text", format_number(extremes["min_y"], 0))
    recorder.set_display("p1_y_max_text", format_number(extremes["max_y"], 0))
    recorder.set_display("p1_projection_area", format_number(area_integral))
    recorder.set_display("p1_projection_area_exact", r"\frac{4}{3}")
    recorder.set_display("p1_projection_yz_area", format_number(area_yz))
    recorder.set_display("p1_projection_yz_area_exact", r"\frac{1}{2}")
    recorder.set_display("p1_volume", format_number(first_order["volume"]))
    recorder.set_display("p1_volume_exact", r"\frac{8}{15}")
    recorder.set_display("p1_volume_mc", format_number(monte_carlo["volume"]))
    recorder.set_display("p1_volume_mc_se", format_number(monte_carlo["volume_standard_error"]))
    recorder.set_display("p1_volume_mc_gap", format_number(volume_gap))
    recorder.set_display("p1_grid_point_count", format_number(extremes["point_count"], 0))
    recorder.set_display("p1_grid_inside_count", format_number(extremes["inside_count"], 0))
    recorder.set_display("p1_cylinder_label", format_number(figure_anchors.CYLINDER_LABEL_POINT[0], 2))
    recorder.set_display("p1_floor_label_y", format_number(figure_anchors.FLOOR_LABEL_POINT[1], 2))
    recorder.set_display("p1_top_label_z", format_number(figure_anchors.TOP_LABEL_POINT[2], 2))
    recorder.set_display("p1_residual", f"{largest_residual:.2e}")
    recorder.save()


if __name__ == "__main__":
    main()
