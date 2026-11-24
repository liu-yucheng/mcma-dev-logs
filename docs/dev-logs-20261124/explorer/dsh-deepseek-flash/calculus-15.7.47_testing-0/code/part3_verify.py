"""Checks of Part 3: the mass integral and the density on the sections.

Run with the environment interpreter: code/.venv/Scripts/python.exe code/part3_verify.py
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
NODE_COUNT = 96


def density(x: float, y: float) -> float:
    """Return the density at one point of the solid.

    Args:
        x: First coordinate.
        y: Second coordinate.

    Returns:
        The value of sqrt(x^2 + y^2).
    """
    return math.hypot(x, y)


def section_mass_at_z(z: float) -> float:
    """Return the mass of the section at one z by a quadrature over the section.

    Args:
        z: Value of the third coordinate.

    Returns:
        The integral of the density over x^2 <= y <= 1 - z with |x| <= sqrt(1 - z).
    """
    extent = math.sqrt(max(0.0, 1.0 - z))
    upper_y = 1.0 - z
    nodes, weights = np.polynomial.legendre.leggauss(NODE_COUNT)
    xs = extent * nodes
    lower_y = xs * xs
    middle = 0.5 * (lower_y + upper_y)
    half = 0.5 * (upper_y - lower_y)
    ys = middle[:, None] + half[:, None] * nodes[None, :]
    values = np.hypot(xs[:, None], ys)
    weights_two = weights[:, None] * half[:, None] * weights[None, :]
    return float(extent * np.sum(weights_two * values))


def main() -> None:
    """Run every check of Part 3 and write the record of the part."""
    recorder = CheckRecorder("part3", OUTPUT_DIRECTORY)

    first_order = integration_tools.integrate_order("dx dz dy")
    second_order = integration_tools.integrate_order("dx dy dz")
    mass = first_order["density"]
    recorder.compare(
        "mass_of_two_orders",
        mass,
        second_order["density"],
        1e-9,
        "the order $dx\\,dz\\,dy$ against the order $dx\\,dy\\,dz$",
    )
    closed_form = integration_tools.integrate_mass_one_dimensional()
    recorder.compare(
        "mass_against_closed_form",
        mass,
        closed_form,
        1e-9,
        "the three-dimensional quadrature against the one-dimensional integral of the inner antiderivative",
    )
    monte_carlo = integration_tools.integrate_monte_carlo()
    mass_gap = abs(monte_carlo["density"] - closed_form)
    recorder.compare_bound(
        "mass_monte_carlo_inside_three_errors",
        mass_gap,
        3.0 * monte_carlo["density_standard_error"],
        "the gap between the Monte Carlo mean and the closed-form mass against three standard errors",
    )

    slice_values = [integration_tools.slice_mass(z, NODE_COUNT) for z in figure_anchors.Z_SLICES]
    for z, value in zip(figure_anchors.Z_SLICES, slice_values):
        recorder.compare(
            f"section_mass_at_z_equal_{z}",
            value,
            section_mass_at_z(z),
            1e-9,
            "the analytic inner integral over $y$ against a two-dimensional quadrature over the same section",
        )

    stacked, _ = quad(lambda z: integration_tools.slice_mass(z, NODE_COUNT),
                      0.0,
                      1.0,
                      points=[1.0],
                      epsabs=1e-12,
                      epsrel=1e-12,
                      )
    recorder.compare(
        "stacked_section_mass_against_mass",
        float(stacked),
        closed_form,
        1e-6,
        "the integral of the section mass over $z$ against the closed-form mass, where the adaptive"
        " quadrature of the stack carries its own error of order 1e-7",
    )

    density_apex = density(0.0, 0.0)
    density_corner = density(1.0, 1.0)
    recorder.compare(
        "density_at_corner_against_hypotenuse",
        density_corner,
        math.sqrt(2.0),
        1e-12,
        "the density at $(1, 1, 0)$ against the diagonal of the unit square",
    )
    recorder.compare(
        "density_at_axis_point",
        density_apex,
        0.0,
        1e-12,
        "the density at $(0, 0, 1)$ against zero, which no other point of the rim gives",
    )

    recorder.set_display("p3_mass", format_number(closed_form))
    recorder.set_display("p3_mass_order", format_number(mass))
    recorder.set_display("p3_mass_mc", format_number(monte_carlo["density"]))
    recorder.set_display("p3_mass_mc_se", format_number(monte_carlo["density_standard_error"]))
    recorder.set_display("p3_mass_mc_gap", format_number(mass_gap))
    recorder.set_display("p3_slice_mass_list", ", ".join(format_number(value) for value in slice_values))
    recorder.set_display("p3_density_corner", format_number(density_corner))
    recorder.set_display("p3_density_corner_exact", r"\sqrt{2}")
    recorder.save()


if __name__ == "__main__":
    main()
