"""Shared geometry, density, and numeric helpers for the tutorial scripts.

The solid E is the part of the first octant that the cylinder x^2 + y^2 = 1 and the planes
y = z, x = 0, and z = 0 bound. The density is rho(x, y, z) = 1 + x + y + z.
Every script of the tutorial imports this module, so all scripts use the same definition.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Callable

import numpy as np

RANDOM_SEED = 20261123
"""Seed of every random sample of the tutorial."""

MONTE_CARLO_SAMPLE_COUNT = 4_000_000
"""Count of the random points of a Monte Carlo check."""

GRID_SAMPLE_COUNT = 4000
"""Count of the midpoint cells on one side of a two-dimensional grid check."""

RESULT_DIRECTORY = Path(__file__).resolve().parent / "results"
"""Directory that holds the machine-readable record of each verified part."""

FIGURE_DIRECTORY = Path(__file__).resolve().parent / "figures"
"""Directory that holds the figures of the tutorial."""


def outer_radius(x_value: float) -> float:
    """Return the largest y of E at the given x, which is sqrt(1 - x^2)."""
    return float(np.sqrt(max(0.0, 1.0 - x_value * x_value)))


def density(x_value: float, y_value: float, z_value: float) -> float:
    """Return rho = 1 + x + y + z at one point."""
    return 1.0 + x_value + y_value + z_value


def density_array(x_values: np.ndarray, y_values: np.ndarray, z_values: np.ndarray) -> np.ndarray:
    """Return rho on three coordinate arrays of the same shape."""
    return 1.0 + x_values + y_values + z_values


def membership_mask(x_values: np.ndarray, y_values: np.ndarray, z_values: np.ndarray) -> np.ndarray:
    """Return the mask of the points that satisfy the four defining inequalities.

    A point belongs to E when x >= 0, y >= 0, z >= 0, x^2 + y^2 <= 1, and z <= y.
    """
    return (
        (x_values >= 0.0)
        & (y_values >= 0.0)
        & (z_values >= 0.0)
        & (x_values * x_values + y_values * y_values <= 1.0)
        & (z_values <= y_values)
    )


def monte_carlo_integral(
    integrand: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray],
) -> tuple[float, float]:
    """Return the mean and the standard error of a Monte Carlo estimate over the unit cube.

    The integrand must return the value zero outside E, so the estimate is the integral over E.
    The cube [0, 1]^3 contains E, and the cube volume is one.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    sample_count = MONTE_CARLO_SAMPLE_COUNT
    x_values = generator.random(sample_count)
    y_values = generator.random(sample_count)
    z_values = generator.random(sample_count)
    values = np.asarray(integrand(x_values, y_values, z_values), dtype=float)
    mean_value = float(values.mean())
    standard_error = float(values.std(ddof=1) / np.sqrt(sample_count))
    return mean_value, standard_error


def monte_carlo_ratio(
    numerator: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray],
    denominator: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray],
) -> tuple[float, float]:
    """Return a Monte Carlo ratio of two integrals over E and its standard error.

    The standard error comes from the delta method with the sample covariance of the two
    integrands. The denominator must stay away from zero.
    """
    generator = np.random.default_rng(RANDOM_SEED + 2)
    sample_count = MONTE_CARLO_SAMPLE_COUNT
    x_values = generator.random(sample_count)
    y_values = generator.random(sample_count)
    z_values = generator.random(sample_count)
    numerator_values = np.asarray(numerator(x_values, y_values, z_values), dtype=float)
    denominator_values = np.asarray(denominator(x_values, y_values, z_values), dtype=float)
    numerator_mean = float(numerator_values.mean())
    denominator_mean = float(denominator_values.mean())
    covariance = np.cov(numerator_values, denominator_values, ddof=1)
    ratio = numerator_mean / denominator_mean
    variance = (
        covariance[0, 0]
        + ratio**2 * covariance[1, 1]
        - 2.0 * ratio * covariance[0, 1]
    ) / (sample_count * denominator_mean**2)
    return ratio, float(np.sqrt(max(variance, 0.0)))


def masked_integrand(
    integrand: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray],
) -> Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]:
    """Return the integrand that is zero outside E."""

    def masked(x_values: np.ndarray, y_values: np.ndarray, z_values: np.ndarray) -> np.ndarray:
        """Return the integrand value inside E and zero outside E."""
        return np.where(membership_mask(x_values, y_values, z_values), integrand(x_values, y_values, z_values), 0.0)

    return masked


def integrate_with_nquad(
    integrand: Callable[[float, float, float], float],
    order: str = "z_y_x",
) -> tuple[float, float]:
    """Return the integral of one integrand over E with an adaptive nested quadrature.

    The integrand takes the arguments (x, y, z). The order names the sequence of the three
    integrations from the inner one to the outer one. Each limit below is one of the four
    inequalities of E, so the three orders integrate over the same point set.
    """
    from scipy.integrate import quad

    options = {"epsabs": 1e-13, "epsrel": 1e-13, "limit": 200}

    def upper_y(x_value: float) -> float:
        """Return the largest y of E at the given x."""
        return math.sqrt(max(0.0, 1.0 - x_value * x_value))

    if order == "z_y_x":

        def after_y(x_value: float) -> float:
            """Integrate z from 0 to y, then y from 0 to the cylinder."""
            inner = quad(lambda y_value: quad(lambda z_value: integrand(x_value, y_value, z_value), 0.0, y_value, **options)[0], 0.0, upper_y(x_value), **options)[0]
            return inner

        value, error = quad(after_y, 0.0, 1.0, **options)
    elif order == "y_z_x":

        def after_z(x_value: float) -> float:
            """Integrate y from z to the cylinder, then z from 0 to the cylinder."""
            inner = quad(lambda z_value: quad(lambda y_value: integrand(x_value, y_value, z_value), z_value, upper_y(x_value), **options)[0], 0.0, upper_y(x_value), **options)[0]
            return inner

        value, error = quad(after_z, 0.0, 1.0, **options)
    elif order == "x_z_y":

        def after_z_of_y(y_value: float) -> float:
            """Integrate x from 0 to the cylinder, then z from 0 to y."""
            inner = quad(lambda z_value: quad(lambda x_value: integrand(x_value, y_value, z_value), 0.0, upper_y(y_value), **options)[0], 0.0, y_value, **options)[0]
            return inner

        value, error = quad(after_z_of_y, 0.0, 1.0, **options)
    else:
        raise ValueError(f"unknown order {order!r}")
    return float(value), float(error)


def triangle_vertices(outer: float) -> list[tuple[float, float]]:
    """Return the vertices of the section of E at a fixed x, as pairs (y, z).

    The section is the triangle with the vertices (0, 0), (outer, 0), and (outer, outer).
    A zero outer radius collapses the triangle to the point (0, 0).
    """
    if outer <= 0.0:
        return [(0.0, 0.0)]
    return [(0.0, 0.0), (outer, 0.0), (outer, outer)]


def polygon_area(vertices: list[tuple[float, float]]) -> float:
    """Return the area of a polygon with the shoelace formula."""
    if len(vertices) < 3:
        return 0.0
    total = 0.0
    for index, (first, second) in enumerate(vertices):
        next_first, next_second = vertices[(index + 1) % len(vertices)]
        total += first * next_second - next_first * second
    return abs(total) / 2.0


def triangle_grid_integral(
    outer: float,
    integrand: Callable[[np.ndarray, np.ndarray], np.ndarray],
) -> float:
    """Return the integral over the section triangle with a midpoint grid.

    The grid covers the square [0, outer] x [0, outer]. The kernel keeps the cells with z <= y.
    """
    if outer <= 0.0:
        return 0.0
    cell_count = GRID_SAMPLE_COUNT
    edges = (np.arange(cell_count) + 0.5) * outer / cell_count
    y_grid, z_grid = np.meshgrid(edges, edges, indexing="ij")
    weights = (outer / cell_count) ** 2
    return float(np.sum(integrand(y_grid, z_grid) * (z_grid <= y_grid)) * weights)


def slice_area_quad(z_value: float) -> float:
    """Return the area of the section of E at a fixed z with one numerical quadrature."""
    from scipy.integrate import quad

    if z_value >= 1.0:
        return 0.0
    value, _ = quad(lambda y_value: np.sqrt(max(0.0, 1.0 - y_value * y_value)), z_value, 1.0, epsabs=1e-13, epsrel=1e-13)
    return float(value)


def slice_grid_area(z_value: float) -> float:
    """Return the area of the section of E at a fixed z with a midpoint grid.

    The section is the set of the points (x, y) with z <= y <= 1 and 0 <= x <= sqrt(1 - y^2).
    """
    if z_value >= 1.0:
        return 0.0
    cell_count = GRID_SAMPLE_COUNT
    edges = (np.arange(cell_count) + 0.5) / cell_count
    y_grid, x_grid = np.meshgrid(edges, edges, indexing="ij")
    keep = (y_grid >= z_value) & (x_grid * x_grid + y_grid * y_grid <= 1.0)
    return float(np.sum(keep) / cell_count**2)


def check_close(
    label: str,
    computed: float,
    expected: float,
    tolerance: float,
) -> dict[str, object]:
    """Print a comparison of two independently computed values and assert the tolerance.

    The function returns a record for the machine-readable result file. The printed line holds
    the computed value, the expected value, the difference, and the tolerance, so the page can
    quote the same numbers that the assertion tested.
    """
    difference = abs(float(computed) - float(expected))
    print(
        f"[check] {label}: computed={computed:.12g} expected={expected:.12g} "
        f"difference={difference:.3e} tolerance={tolerance:.3e}"
    )
    if not difference <= tolerance:
        raise AssertionError(
            f"{label}: computed {computed!r} and expected {expected!r} differ by {difference:.6e}, "
            f"which is more than the tolerance {tolerance:.3e}."
        )
    return {
        "label": label,
        "computed": float(computed),
        "expected": float(expected),
        "difference": difference,
        "tolerance": float(tolerance),
    }


def write_result(part_number: int, payload: dict[str, object]) -> Path:
    """Write the machine-readable record of one part and return its path."""
    RESULT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    path = RESULT_DIRECTORY / f"part{part_number}_results.json"
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(payload, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(f"[result] wrote {path}")
    return path


def decimal(value: float, digits: int = 6) -> str:
    """Return a fixed-point text of a value with the given count of digits."""
    return f"{value:.{digits}f}"
