"""Numerical tools for the triple integral of the tutorial.

The module holds the density of the problem, the six orders of the triple
integral over the solid, one nested Gauss-Legendre quadrature, one Monte Carlo
estimator, and one one-dimensional form of the mass integral. A verification
script compares the value of one method with the value of a different method.
"""

from __future__ import annotations

import math
from typing import Callable

import numpy as np

GAUSS_NODE_COUNT: int = 46
"""Number of Gauss-Legendre nodes on each coordinate of a nested integration."""

REFINED_NODE_COUNT: int = 92
"""Node count of the refinement that measures the discretization error."""

MONTE_CARLO_SAMPLE_COUNT: int = 2_000_000
"""Number of uniform samples of the Monte Carlo estimator."""

RANDOM_SEED: int = 20261123
"""Seed of the random number generator of the Monte Carlo estimator."""

QUANTITY_NAMES: tuple[str, ...] = (
    "volume",
    "density",
    "moment_x",
    "moment_y",
    "moment_z",
    "inertia",
)
"""Name of each integral that one order returns, in column order."""

# A bound entry is (variable name, lower function, upper function). Each function
# receives the tuple of the already chosen outer coordinates.
BoundEntry = tuple[str, Callable[[tuple[float, ...]], float], Callable[[tuple[float, ...]], float]]

ORDER_BOUNDS: dict[str, list[BoundEntry]] = {
    "dz dy dx": [
        ("x", lambda outer: -1.0, lambda outer: 1.0),
        ("y", lambda outer: outer[0] ** 2, lambda outer: 1.0),
        ("z", lambda outer: 0.0, lambda outer: 1.0 - outer[1]),
    ],
    "dy dz dx": [
        ("x", lambda outer: -1.0, lambda outer: 1.0),
        ("z", lambda outer: 0.0, lambda outer: 1.0 - outer[0] ** 2),
        ("y", lambda outer: outer[0] ** 2, lambda outer: 1.0 - outer[1]),
    ],
    "dz dx dy": [
        ("y", lambda outer: 0.0, lambda outer: 1.0),
        ("x", lambda outer: -math.sqrt(outer[0]), lambda outer: math.sqrt(outer[0])),
        ("z", lambda outer: 0.0, lambda outer: 1.0 - outer[0]),
    ],
    "dx dz dy": [
        ("y", lambda outer: 0.0, lambda outer: 1.0),
        ("z", lambda outer: 0.0, lambda outer: 1.0 - outer[0]),
        ("x", lambda outer: -math.sqrt(outer[0]), lambda outer: math.sqrt(outer[0])),
    ],
    "dy dx dz": [
        ("z", lambda outer: 0.0, lambda outer: 1.0),
        ("x", lambda outer: -math.sqrt(1.0 - outer[0]), lambda outer: math.sqrt(1.0 - outer[0])),
        ("y", lambda outer: outer[1] ** 2, lambda outer: 1.0 - outer[0]),
    ],
    "dx dy dz": [
        ("z", lambda outer: 0.0, lambda outer: 1.0),
        ("y", lambda outer: 0.0, lambda outer: 1.0 - outer[0]),
        ("x", lambda outer: -math.sqrt(outer[1]), lambda outer: math.sqrt(outer[1])),
    ],
}
"""Limits of the six orders of the integral over the solid.

Each key is written with the innermost differential first, as in an iterated
integral. The list of a key gives the outer coordinate first. Every limit
follows from the three defining inequalities x^2 <= y, 0 <= z, y + z <= 1.
"""


def quantity_vector(x: float, y: float, z: float) -> np.ndarray:
    """Return the integrand of each quantity at one point, in QUANTITY_NAMES order.

    Args:
        x: First coordinate of the point.
        y: Second coordinate of the point.
        z: Third coordinate of the point.

    Returns:
        One array of six values: the constant one, the density, the three
        first moments, and the squared distance times the density.
    """
    radius_squared = x * x + y * y
    density_value = math.sqrt(radius_squared) if isinstance(x, float) else np.sqrt(radius_squared)
    return np.array(
        [
            1.0,
            density_value,
            x * density_value,
            y * density_value,
            z * density_value,
            radius_squared * density_value,
        ]
    )


def integrate_order(order_name: str, node_count: int = GAUSS_NODE_COUNT) -> dict[str, float]:
    """Integrate the six quantities over the solid in one order of integration.

    Args:
        order_name: One key of ORDER_BOUNDS.
        node_count: Number of Gauss-Legendre nodes on each coordinate.

    Returns:
        One dictionary from each name of QUANTITY_NAMES to its integral.
    """
    specification = ORDER_BOUNDS[order_name]
    nesting = [entry[0] for entry in specification]
    position = {name: index for index, name in enumerate(nesting)}
    x_slot = position["x"]
    y_slot = position["y"]
    z_slot = position["z"]
    nodes, weights = np.polynomial.legendre.leggauss(node_count)

    def evaluate(values: tuple[float, ...]) -> np.ndarray:
        """Return the six integrands at one point of the nested integration."""
        return quantity_vector(values[x_slot], values[y_slot], values[z_slot])

    def recurse(level: int, outer: tuple[float, ...]) -> np.ndarray:
        """Integrate one coordinate over its limits and pass the result outward."""
        _, lower_function, upper_function = specification[level]
        lower = float(lower_function(outer))
        upper = float(upper_function(outer))
        middle = 0.5 * (lower + upper)
        half = 0.5 * (upper - lower)
        total = np.zeros(len(QUANTITY_NAMES))
        if level + 1 == len(specification):
            for node, weight in zip(nodes, weights):
                point = outer + (middle + half * float(node),)
                total = total + float(weight) * evaluate(point)
            return half * total
        for node, weight in zip(nodes, weights):
            point = outer + (middle + half * float(node),)
            total = total + float(weight) * recurse(level + 1, point)
        return half * total

    values = recurse(0, ())
    return {name: float(value) for name, value in zip(QUANTITY_NAMES, values)}


def inside_solid(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return the mask of the points that satisfy the three defining inequalities.

    Args:
        x: Array of first coordinates.
        y: Array of second coordinates.
        z: Array of third coordinates.

    Returns:
        One boolean array. A true entry marks a point of the solid.
    """
    return (y >= x * x) & (y <= 1.0) & (z >= 0.0) & (y + z <= 1.0)


def integrate_monte_carlo(sample_count: int = MONTE_CARLO_SAMPLE_COUNT, seed: int = RANDOM_SEED) -> dict:
    """Estimate the six quantities by uniform sampling of a box around the solid.

    The box is the unit cube of the first octant with x in [-1, 1], so its volume
    is two. Every sample is tested against the three defining inequalities.

    Args:
        sample_count: Number of uniform samples.
        seed: Seed of the random number generator.

    Returns:
        One dictionary with the estimate and the standard error of each quantity.
    """
    generator = np.random.default_rng(seed)
    x = generator.uniform(-1.0, 1.0, sample_count)
    y = generator.uniform(0.0, 1.0, sample_count)
    z = generator.uniform(0.0, 1.0, sample_count)
    mask = inside_solid(x, y, z)
    box_volume = 2.0
    inside_count = int(np.count_nonzero(mask))
    weights = np.zeros(sample_count)
    radius_squared = x[mask] ** 2 + y[mask] ** 2
    density_value = np.sqrt(radius_squared)
    columns = {
        "volume": np.ones(inside_count),
        "density": density_value,
        "moment_x": x[mask] * density_value,
        "moment_y": y[mask] * density_value,
        "moment_z": z[mask] * density_value,
        "inertia": radius_squared * density_value,
    }
    result = {"inside_count": inside_count, "sample_count": sample_count}
    for name, column in columns.items():
        weights[mask] = column
        contribution = weights * box_volume
        estimate = float(contribution.mean())
        standard_error = float(contribution.std(ddof=1) / math.sqrt(sample_count))
        result[name] = estimate
        result[name + "_standard_error"] = standard_error
    return result


def mass_inner_integral(x: float) -> float:
    """Return the integral of the density over y and z at one value of x.

    The inner integral has a closed form. The expression of the antiderivative
    of (1 - y) sqrt(x^2 + y^2) in y is a sum of three terms.

    Args:
        x: Value of the first coordinate.

    Returns:
        The value of the integral over y from x^2 to 1 and over z from 0 to 1 - y.
    """

    def antiderivative(y: float) -> float:
        """Return one antiderivative of (1 - y) sqrt(x^2 + y^2) in y."""
        radius = math.hypot(x, y)
        logarithmic = 0.0 if radius + y <= 0.0 else math.log(y + radius)
        return 0.5 * y * radius + 0.5 * x * x * logarithmic - radius**3 / 3.0

    return antiderivative(1.0) - antiderivative(x * x)


def integrate_mass_one_dimensional() -> float:
    """Return the mass from the closed form of the inner integral and one quadrature.

    Returns:
        The value of the mass integral over x in [-1, 1].
    """
    from scipy.integrate import quad

    value, _ = quad(mass_inner_integral, -1.0, 1.0, points=[0.0], limit=400, epsabs=1e-13, epsrel=1e-13)
    return float(value)


def slice_mass(z: float, node_count: int = 24) -> float:
    """Return the integral of the density over the section of the solid at one z.

    Args:
        z: Value of the third coordinate. The section is empty when z is above one.
        node_count: Number of Gauss-Legendre nodes on each coordinate.

    Returns:
        The value of the integral of the density over the section.
    """
    if z < 0.0 or z > 1.0:
        return 0.0
    extent = math.sqrt(1.0 - z)
    nodes, weights = np.polynomial.legendre.leggauss(node_count)
    total = 0.0
    for node_x, weight_x in zip(nodes, weights):
        x = extent * float(node_x)
        lower = x * x
        upper = 1.0 - z
        middle = 0.5 * (lower + upper)
        half = 0.5 * (upper - lower)
        inner = 0.0
        for node_y, weight_y in zip(nodes, weights):
            y = middle + half * float(node_y)
            inner += float(weight_y) * math.hypot(x, y)
        total += float(weight_x) * half * inner
    return extent * total


def slice_area_at_z(z: float) -> float:
    """Return the area of the section of the solid at one value of z.

    Args:
        z: Value of the third coordinate.

    Returns:
        The area of the parabolic section at that height.
    """
    if z < 0.0 or z > 1.0:
        return 0.0
    return (4.0 / 3.0) * (1.0 - z) ** 1.5


def slice_area_at_y(y: float) -> float:
    """Return the area of the section of the solid at one value of y.

    Args:
        y: Value of the second coordinate.

    Returns:
        The area of the rectangular section at that coordinate.
    """
    if y < 0.0 or y > 1.0:
        return 0.0
    return 2.0 * math.sqrt(y) * (1.0 - y)
