"""The six integration orders of Exercise 15.7.32.

Each order names the variables from the inner integral to the outer integral. An order
holds the limits as functions of the outer variables, a membership test that reads the
limits as a set, an exact symbolic value, and a nested quadrature of high order.

The membership test is the key object: it lets a verification script compare the set
that the printed limits describe with the set that the half-spaces define.

Constants:
    ORDERS: A dictionary of the six orders. The key is the order in words, such as "dz dx dy".
    LEVEL_COUNT: The number of nested integrals of every order.
"""

import numpy as np
import sympy

LEVEL_COUNT = 3


def _inside(first, second, third):
    """Return a boolean array for a chain of three non-strict interval tests."""
    return first & second & third


ORDERS = {}


def _register(name, latex, levels, membership):
    """Add one order to the ORDERS dictionary.

    Args:
        name: The order in words, such as "dz dx dy".
        latex: The LaTeX source of the iterated integral with the integrand f(x, y, z).
        levels: A tuple of three entries from the inner integral to the outer integral.
            Each entry is a variable name, a lower limit, and an upper limit.
        membership: A function of three float arrays that reads the limits as a set.
    """
    ORDERS[name] = {"latex": latex, "levels": levels, "membership": membership}


_register(
    "dz dx dy",
    r"\int_{0}^{2}\int_{2-y}^{2}\int_{0}^{\frac{x+y-2}{2}} f(x,y,z)\,dz\,dx\,dy",
    (
        ("z", lambda env: 0.0, lambda env: (env["x"] + env["y"] - 2.0) / 2.0),
        ("x", lambda env: 2.0 - env["y"], lambda env: 2.0),
        ("y", lambda env: 0.0, lambda env: 2.0),
    ),
    lambda x, y, z: _inside(
        (y >= 0.0) & (y <= 2.0),
        (x >= 2.0 - y) & (x <= 2.0),
        (z >= 0.0) & (z <= (x + y - 2.0) / 2.0),
    ),
)

_register(
    "dz dy dx",
    r"\int_{0}^{2}\int_{2-x}^{2}\int_{0}^{\frac{x+y-2}{2}} f(x,y,z)\,dz\,dy\,dx",
    (
        ("z", lambda env: 0.0, lambda env: (env["x"] + env["y"] - 2.0) / 2.0),
        ("y", lambda env: 2.0 - env["x"], lambda env: 2.0),
        ("x", lambda env: 0.0, lambda env: 2.0),
    ),
    lambda x, y, z: _inside(
        (x >= 0.0) & (x <= 2.0),
        (y >= 2.0 - x) & (y <= 2.0),
        (z >= 0.0) & (z <= (x + y - 2.0) / 2.0),
    ),
)

_register(
    "dy dx dz",
    r"\int_{0}^{1}\int_{2z}^{2}\int_{2-x+2z}^{2} f(x,y,z)\,dy\,dx\,dz",
    (
        ("y", lambda env: 2.0 - env["x"] + 2.0 * env["z"], lambda env: 2.0),
        ("x", lambda env: 2.0 * env["z"], lambda env: 2.0),
        ("z", lambda env: 0.0, lambda env: 1.0),
    ),
    lambda x, y, z: _inside(
        (z >= 0.0) & (z <= 1.0),
        (x >= 2.0 * z) & (x <= 2.0),
        (y >= 2.0 - x + 2.0 * z) & (y <= 2.0),
    ),
)

_register(
    "dy dz dx",
    r"\int_{0}^{2}\int_{0}^{\frac{x}{2}}\int_{2-x+2z}^{2} f(x,y,z)\,dy\,dz\,dx",
    (
        ("y", lambda env: 2.0 - env["x"] + 2.0 * env["z"], lambda env: 2.0),
        ("z", lambda env: 0.0, lambda env: env["x"] / 2.0),
        ("x", lambda env: 0.0, lambda env: 2.0),
    ),
    lambda x, y, z: _inside(
        (x >= 0.0) & (x <= 2.0),
        (z >= 0.0) & (z <= x / 2.0),
        (y >= 2.0 - x + 2.0 * z) & (y <= 2.0),
    ),
)

_register(
    "dx dy dz",
    r"\int_{0}^{1}\int_{2z}^{2}\int_{2-y+2z}^{2} f(x,y,z)\,dx\,dy\,dz",
    (
        ("x", lambda env: 2.0 - env["y"] + 2.0 * env["z"], lambda env: 2.0),
        ("y", lambda env: 2.0 * env["z"], lambda env: 2.0),
        ("z", lambda env: 0.0, lambda env: 1.0),
    ),
    lambda x, y, z: _inside(
        (z >= 0.0) & (z <= 1.0),
        (y >= 2.0 * z) & (y <= 2.0),
        (x >= 2.0 - y + 2.0 * z) & (x <= 2.0),
    ),
)

_register(
    "dx dz dy",
    r"\int_{0}^{2}\int_{0}^{\frac{y}{2}}\int_{2-y+2z}^{2} f(x,y,z)\,dx\,dz\,dy",
    (
        ("x", lambda env: 2.0 - env["y"] + 2.0 * env["z"], lambda env: 2.0),
        ("z", lambda env: 0.0, lambda env: env["y"] / 2.0),
        ("y", lambda env: 0.0, lambda env: 2.0),
    ),
    lambda x, y, z: _inside(
        (y >= 0.0) & (y <= 2.0),
        (z >= 0.0) & (z <= y / 2.0),
        (x >= 2.0 - y + 2.0 * z) & (x <= 2.0),
    ),
)


def symbolic_value(name, function_expression):
    """Return the exact value of one order for a given integrand.

    Args:
        name: The order in words, such as "dz dx dy".
        function_expression: A sympy expression in the symbols x, y, and z.

    Returns:
        The exact value as a sympy expression.
    """
    symbols = {letter: sympy.Symbol(letter) for letter in ("x", "y", "z")}
    value = function_expression
    for variable, lower, upper in ORDERS[name]["levels"]:
        environment = {key: symbols[key] for key in ("x", "y", "z")}
        bound_lower = sympy.nsimplify(sympy.sympify(lower(environment)), rational=True)
        bound_upper = sympy.nsimplify(sympy.sympify(upper(environment)), rational=True)
        value = sympy.integrate(value, (symbols[variable], bound_lower, bound_upper))
    return sympy.simplify(value)


def nested_gauss_value(name, function, points):
    """Return the value of one order by a nested Gauss-Legendre rule.

    Args:
        name: The order in words, such as "dz dx dy".
        function: A function of a dictionary with the keys x, y, and z.
        points: The number of Gauss-Legendre points on each interval.

    Returns:
        The numeric value as a float.
    """
    nodes, weights = np.polynomial.legendre.leggauss(points)
    levels = list(reversed(ORDERS[name]["levels"]))

    def integrate(level_index, environment):
        variable, lower, upper = levels[level_index]
        lower_bound = float(lower(environment))
        upper_bound = float(upper(environment))
        half_width = (upper_bound - lower_bound) / 2.0
        middle = (upper_bound + lower_bound) / 2.0
        total = 0.0
        for node, weight in zip(nodes, weights):
            local = dict(environment)
            local[variable] = middle + half_width * float(node)
            if level_index == LEVEL_COUNT - 1:
                total += float(weight) * function(local)
            else:
                total += float(weight) * integrate(level_index + 1, local)
        return total * half_width

    return integrate(0, {})
