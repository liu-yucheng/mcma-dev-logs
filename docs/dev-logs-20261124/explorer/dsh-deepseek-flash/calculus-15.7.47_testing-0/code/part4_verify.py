"""Checks of Part 4: the first moments and the center of mass.

Run with the environment interpreter: code/.venv/Scripts/python.exe code/part4_verify.py
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


def density(x: float, y: float) -> float:
    """Return the density at one point of the solid.

    Args:
        x: First coordinate.
        y: Second coordinate.

    Returns:
        The value of sqrt(x^2 + y^2).
    """
    return math.hypot(x, y)


def section_mass_by_quadrature(z: float) -> float:
    """Return the mass of the section at one z by a two-dimensional quadrature.

    Args:
        z: Value of the third coordinate.

    Returns:
        The integral of the density over the section x^2 <= y <= 1 - z.
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


def line_density_integral(y: float) -> float:
    """Return the integral of the density along one line of constant y and z.

    Args:
        y: Value of the second coordinate.

    Returns:
        The integral of sqrt(x^2 + y^2) over x from -sqrt(y) to sqrt(y).
    """
    half_width = math.sqrt(y)
    value, _ = quad(
        lambda x: density(x, y),
        -half_width,
        half_width,
        epsabs=1e-13,
        epsrel=1e-13,
        limit=200,
    )
    return float(value)


def moment_y_by_sections() -> float:
    """Return the first moment of y from a one-dimensional stack of sections.

    Returns:
        The integral of y times the density over the solid, computed as the
        integral over y of y (1 - y) times the line integral at that y.
    """
    value, _ = quad(
        lambda y: y * (1.0 - y) * line_density_integral(y),
        0.0,
        1.0,
        epsabs=1e-12,
        epsrel=1e-12,
        limit=200,
    )
    return float(value)


def moment_z_by_sections() -> float:
    """Return the first moment of z from a stack of horizontal sections.

    Returns:
        The integral over z of z times the mass of the section at that z.
    """
    value, _ = quad(
        lambda z: z * section_mass_by_quadrature(z),
        0.0,
        1.0,
        epsabs=1e-12,
        epsrel=1e-12,
        limit=100,
    )
    return float(value)


def main() -> None:
    """Run every check of Part 4 and write the record of the part."""
    recorder = CheckRecorder("part4", OUTPUT_DIRECTORY)

    first_order = integration_tools.integrate_order("dx dz dy")
    second_order = integration_tools.integrate_order("dx dy dz")
    mass = first_order["density"]
    recorder.compare(
        "moment_y_of_two_orders",
        first_order["moment_y"],
        second_order["moment_y"],
        1e-9,
        "the order $dx\\,dz\\,dy$ against the order $dx\\,dy\\,dz$",
    )
    recorder.compare(
        "moment_z_of_two_orders",
        first_order["moment_z"],
        second_order["moment_z"],
        1e-9,
        "the order $dx\\,dz\\,dy$ against the order $dx\\,dy\\,dz$",
    )
    recorder.compare(
        "moment_x_vanishes",
        first_order["moment_x"],
        0.0,
        1e-12,
        "the region and the density are unchanged by $x \\mapsto -x$, so the integral of the odd function $x\\sqrt{x^{2}+y^{2}}$ is zero",
    )

    y_bar = first_order["moment_y"] / mass
    z_bar = first_order["moment_z"] / mass
    x_bar = first_order["moment_x"] / mass

    moment_y_alt = moment_y_by_sections()
    moment_z_alt = moment_z_by_sections()
    recorder.compare(
        "moment_y_by_sections",
        first_order["moment_y"],
        moment_y_alt,
        1e-8,
        "the three-dimensional quadrature against the stack of line integrals at constant $y$",
    )
    recorder.compare(
        "moment_z_by_sections",
        first_order["moment_z"],
        moment_z_alt,
        1e-7,
        "the three-dimensional quadrature against the stack of section masses at constant $z$",
    )

    recorder.compare(
        "y_bar_against_sections",
        y_bar,
        moment_y_alt / integration_tools.integrate_mass_one_dimensional(),
        1e-6,
        "the quotient of the quadrature moments against the quotient of the stacked moments",
    )
    recorder.compare(
        "z_bar_against_sections",
        z_bar,
        moment_z_alt / integration_tools.integrate_mass_one_dimensional(),
        1e-6,
        "the quotient of the quadrature moments against the quotient of the stacked moments",
    )
    recorder.compare_bound(
        "x_bar_below_resolution",
        abs(x_bar),
        1e-12,
        "the center of mass lies on the plane $x = 0$ by symmetry, so $\\bar{x}$ is zero within the resolution of the quadrature",
    )

    recorder.set_display("p4_mass", format_number(mass))
    recorder.set_display("p4_moment_x", format_number(first_order["moment_x"]))
    recorder.set_display("p4_moment_y", format_number(first_order["moment_y"]))
    recorder.set_display("p4_moment_z", format_number(first_order["moment_z"]))
    recorder.set_display("p4_xbar", format_number(x_bar))
    recorder.set_display("p4_ybar", format_number(y_bar))
    recorder.set_display("p4_zbar", format_number(z_bar))
    recorder.set_display("p4_moment_y_alt", format_number(moment_y_alt))
    recorder.set_display("p4_moment_z_alt", format_number(moment_z_alt))
    recorder.set_display("p4_ybar_alt", format_number(moment_y_alt / mass))
    recorder.set_display("p4_zbar_alt", format_number(moment_z_alt / mass))
    recorder.save()


if __name__ == "__main__":
    main()
