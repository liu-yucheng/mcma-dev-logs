"""Verification of Part 5, the checks of the six formulas.

This script checks that the six orders agree on one polynomial, that a numerical
quadrature without a symbolic bound agrees with them, that the indicator quadrature
converges, and that the six printed formulas are six different expressions.

Constants:
    POLYNOMIAL_COEFFICIENTS: The coefficients of the test function 2 + x*y - z.
    MONTE_CARLO_COUNT: The number of random points of the box quadrature.
    MONTE_CARLO_SEED: The random seed of the box quadrature.
    RIEMANN_RESOLUTIONS: The cell counts of the indicator quadrature, one per axis.
    CONVERGENCE_FACTOR: The least ratio of two successive errors of the quadrature.
"""

import os
import sys
from fractions import Fraction

import numpy as np
import sympy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import orders
import solid
from verify_common import as_text, check, record

POLYNOMIAL_COEFFICIENTS = (2.0, 1.0, -1.0)
MONTE_CARLO_COUNT = 4_000_000
MONTE_CARLO_SEED = 20261123
RIEMANN_RESOLUTIONS = (20, 40, 80, 160, 320)
CONVERGENCE_FACTOR = 1.3
INTEGER_VERTICES = [(2, 2, 0), (2, 2, 1), (2, 0, 0), (0, 2, 0)]


def test_function(x_value, y_value, z_value):
    """Return the value of the polynomial 2 + x*y - z.

    Args:
        x_value: The first coordinate.
        y_value: The second coordinate.
        z_value: The third coordinate.

    Returns:
        The value of the polynomial at the point.
    """
    constant, product_weight, z_weight = POLYNOMIAL_COEFFICIENTS
    return constant + product_weight * x_value * y_value + z_weight * z_value


def monte_carlo_value(count, seed):
    """Integrate the polynomial over the box with the indicator of E.

    Args:
        count: The number of random points.
        seed: The random seed.

    Returns:
        A tuple of the estimate and its standard error.
    """
    generator = np.random.default_rng(seed)
    lower = np.array(solid.BOX_LOWER, dtype=float)
    upper = np.array(solid.BOX_UPPER, dtype=float)
    points = generator.uniform(lower, upper, size=(count, 3))
    inside = solid.contains(points)
    box_volume = float(np.prod(upper - lower))
    values = np.zeros(count)
    inner = points[inside]
    values[inside] = test_function(inner[:, 0], inner[:, 1], inner[:, 2])
    fraction = float(np.count_nonzero(inside)) / float(count)
    estimate = box_volume * float(np.mean(values))
    spread = box_volume * float(np.std(values)) / float(np.sqrt(count))
    return estimate, spread, fraction * box_volume


def riemann_value(resolution):
    """Integrate the polynomial over the box with an indicator on a cell grid.

    Args:
        resolution: The number of cells of each axis.

    Returns:
        The value of the midpoint rule with the indicator of E.
    """
    axes = []
    for axis_index in range(3):
        lower = solid.BOX_LOWER[axis_index]
        upper = solid.BOX_UPPER[axis_index]
        step = (upper - lower) / resolution
        axes.append(lower + step * (np.arange(resolution) + 0.5))
    grid = np.meshgrid(*axes, indexing="ij")
    x_value = grid[0].ravel()
    y_value = grid[1].ravel()
    z_value = grid[2].ravel()
    inside = solid.contains(np.column_stack([x_value, y_value, z_value]))
    cell_volume = 1.0 / resolution**3 * float(np.prod(np.array(solid.BOX_UPPER) - np.array(solid.BOX_LOWER)))
    values = test_function(x_value[inside], y_value[inside], z_value[inside])
    return float(np.sum(values) * cell_volume)


def main():
    """Check the six formulas together and write the record of Part 5."""
    checks = []
    values = {}

    x_symbol, y_symbol, z_symbol = sympy.symbols("x y z")
    expression = (
        sympy.Rational(int(round(POLYNOMIAL_COEFFICIENTS[0])))
        + sympy.Rational(int(round(POLYNOMIAL_COEFFICIENTS[1]))) * x_symbol * y_symbol
        + sympy.Rational(int(round(POLYNOMIAL_COEFFICIENTS[2]))) * z_symbol
    )

    exact_values = {}
    for name in orders.ORDERS:
        exact_values[name] = orders.symbolic_value(name, expression)
        values["latex_%s" % name.replace(" ", "")] = orders.ORDERS[name]["latex"]

    unified = set(exact_values.values())
    checks.append(check("the six orders give one common exact value", len(unified), 1))
    common_value = next(iter(unified))
    common_float = float(common_value)
    values["exact_common"] = as_text(common_float)
    values["exact_common_latex"] = sympy.latex(common_value)

    volume_unit = float(solid.determinant_volume(INTEGER_VERTICES))
    unit_values = {name: orders.symbolic_value(name, sympy.Integer(1)) for name in orders.ORDERS}
    checks.append(check("with f = 1 every order gives the volume by determinant", float(unit_values["dz dx dy"]), volume_unit, 1e-12))
    checks.append(check("the six orders with f = 1 give one value", len(set(unit_values.values())), 1))

    estimate, spread, inside_volume = monte_carlo_value(MONTE_CARLO_COUNT, MONTE_CARLO_SEED)
    values["monte_carlo"] = as_text(estimate)
    values["monte_carlo_spread"] = as_text(spread)
    values["monte_carlo_count"] = MONTE_CARLO_COUNT
    checks.append(check("box quadrature with the indicator of E against the exact value, four standard errors", estimate, common_float, 4.0 * spread + 1e-12))
    checks.append(check("box quadrature: random points inside E against the volume by determinant, four standard errors", inside_volume, volume_unit, 4.0 * spread + 1e-12))

    riemann_errors = []
    for resolution in RIEMANN_RESOLUTIONS:
        riemann = riemann_value(resolution)
        error = abs(riemann - common_float)
        riemann_errors.append(error)
        values["riemann_%d" % resolution] = as_text(riemann)
        values["riemann_error_%d" % resolution] = as_text(error)

    checks.append(check("indicator quadrature at the coarsest grid against the exact value, one tenth", riemann_errors[0], 0.0, 0.1 * abs(common_float)))
    checks.append(check("indicator quadrature at the finest grid against the exact value, one hundredth", riemann_errors[-1], 0.0, 0.01 * abs(common_float)))
    ratios = [riemann_errors[index] / riemann_errors[index + 1] for index in range(len(riemann_errors) - 1)]
    values["riemann_ratios"] = [as_text(ratio) for ratio in ratios]
    checks.append(check("every refinement lowers the error by more than CONVERGENCE_FACTOR", min(ratios), CONVERGENCE_FACTOR, comparison="above"))

    latex_strings = [orders.ORDERS[name]["latex"] for name in orders.ORDERS]
    checks.append(check("the six printed formulas are six different strings", len(set(latex_strings)), 6))
    values["latex_distinct"] = len(set(latex_strings))

    values["polynomial"] = "2 + xy - z"
    values["polynomial_values"] = [as_text(test_function(0.0, 0.0, 0.0)), as_text(test_function(2.0, 2.0, 1.0))]
    checks.append(check("the polynomial at the origin against its constant term", test_function(0.0, 0.0, 0.0), POLYNOMIAL_COEFFICIENTS[0]))
    checks.append(check("the polynomial at the apex against the constant term plus four minus one", test_function(2.0, 2.0, 1.0), POLYNOMIAL_COEFFICIENTS[0] + 4.0 * POLYNOMIAL_COEFFICIENTS[1] + POLYNOMIAL_COEFFICIENTS[2]))

    record(5, values, checks)


if __name__ == "__main__":
    main()
