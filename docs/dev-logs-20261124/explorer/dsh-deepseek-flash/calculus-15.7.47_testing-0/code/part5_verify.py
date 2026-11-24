"""Checks of Part 5: the moment of inertia about the z axis.

Run with the environment interpreter: code/.venv/Scripts/python.exe code/part5_verify.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad

sys.path.insert(0, str(Path(__file__).resolve().parent))

import integration_tools
from check_tools import CheckRecorder, format_number

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"
NODE_COUNT = 96


def section_inertia_by_quadrature(z: float) -> float:
    """Return the contribution of one section to the moment of inertia about the z axis.

    Args:
        z: Value of the third coordinate.

    Returns:
        The integral of (x^2 + y^2) times the density over the section at that z.
    """
    extent = math.sqrt(max(0.0, 1.0 - z))
    upper_y = 1.0 - z
    nodes, weights = np.polynomial.legendre.leggauss(NODE_COUNT)
    xs = extent * nodes
    lower_y = xs * xs
    middle = 0.5 * (lower_y + upper_y)
    half = 0.5 * (upper_y - lower_y)
    ys = middle[:, None] + half[:, None] * nodes[None, :]
    radius_squared = xs[:, None] ** 2 + ys**2
    values = np.hypot(xs[:, None], ys) * radius_squared
    weights_two = weights[:, None] * half[:, None] * weights[None, :]
    return float(extent * np.sum(weights_two * values))


def inertia_by_sections() -> float:
    """Return the moment of inertia about the z axis from a stack of sections.

    Returns:
        The integral over z of the contribution of the section at that z.
    """
    value, _ = quad(
        section_inertia_by_quadrature,
        0.0,
        1.0,
        epsabs=1e-12,
        epsrel=1e-12,
        limit=100,
    )
    return float(value)


def inertia_in_polar_coordinates() -> float:
    """Return the moment of inertia from one integral in x of a closed inner form.

    Returns:
        The integral over x of the inner integral of (x^2 + y^2) sqrt(x^2 + y^2)
        over the part of the section at z = 0 that x cuts, taken over the whole
        solid by an inner quadrature in y and z.
    """
    total = 0.0
    nodes, weights = np.polynomial.legendre.leggauss(NODE_COUNT)
    for node_x, weight_x in zip(nodes, weights):
        x = float(node_x)
        lower_y = x * x
        middle = 0.5 * (lower_y + 1.0)
        half = 0.5 * (1.0 - lower_y)
        inner = 0.0
        for node_y, weight_y in zip(nodes, weights):
            y = middle + half * float(node_y)
            height = 1.0 - y
            inner += float(weight_y) * half * height * (x * x + y * y) * math.hypot(x, y)
        total += float(weight_x) * inner
    return total


def main() -> None:
    """Run every check of Part 5 and write the record of the part."""
    recorder = CheckRecorder("part5", OUTPUT_DIRECTORY)

    first_order = integration_tools.integrate_order("dx dz dy")
    second_order = integration_tools.integrate_order("dx dy dz")
    inertia = first_order["inertia"]
    recorder.compare(
        "inertia_of_two_orders",
        inertia,
        second_order["inertia"],
        1e-9,
        "the order $dx\\,dz\\,dy$ against the order $dx\\,dy\\,dz$",
    )

    stacked = inertia_by_sections()
    recorder.compare(
        "inertia_by_sections",
        inertia,
        stacked,
        1e-7,
        "the three-dimensional quadrature against the stack of section contributions over $z$",
    )

    polar = inertia_in_polar_coordinates()
    recorder.compare(
        "inertia_by_one_integral_in_x",
        inertia,
        polar,
        1e-6,
        "the three-dimensional quadrature against one integral in $x$ of a two-dimensional inner quadrature",
    )

    monte_carlo = integration_tools.integrate_monte_carlo()
    gap = abs(monte_carlo["inertia"] - inertia)
    recorder.compare_bound(
        "inertia_monte_carlo_inside_three_errors",
        gap,
        3.0 * monte_carlo["inertia_standard_error"],
        "the gap between the Monte Carlo mean and the quadrature value against three standard errors",
    )

    mass = first_order["density"]
    recorder.compare(
        "inertia_against_density_times_radius",
        inertia / mass,
        stacked / integration_tools.integrate_mass_one_dimensional(),
        1e-6,
        "the ratio of the inertia to the mass against the same ratio built from the stacked values",
    )

    section_values = [section_inertia_by_quadrature(z) for z in (0.0, 0.5, 0.8)]
    recorder.set_display("p5_inertia", format_number(inertia))
    recorder.set_display("p5_inertia_alt", format_number(stacked))
    recorder.set_display("p5_inertia_polar", format_number(polar))
    recorder.set_display("p5_inertia_mc", format_number(monte_carlo["inertia"]))
    recorder.set_display("p5_inertia_mc_se", format_number(monte_carlo["inertia_standard_error"]))
    recorder.set_display("p5_inertia_gap", format_number(gap))
    recorder.set_display("p5_section_inertia_list", ", ".join(format_number(value) for value in section_values))
    recorder.set_display("p5_inertia_over_mass", format_number(inertia / mass))
    recorder.save()


if __name__ == "__main__":
    main()
