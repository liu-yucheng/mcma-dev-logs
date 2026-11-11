"""Evaluate the six orders of integration for f = 1 with SymPy.

Each order is reduced one integral at a time.  When a limit contains a square root, the
script uses a positive symbol for the radius, so the algebra stays exact.

Usage:
    python part1_step2.py
"""

from sympy import Rational, cos, integrate, pi, simplify, sin, sqrt, symbols

x, y, z = symbols("x y z", real=True)
half = symbols("half", positive=True)
radius = symbols("radius", positive=True)
c2 = symbols("c2", positive=True)
s2 = symbols("s2", positive=True)


def show(label: str, value: object) -> None:
    """Print one intermediate integral result.

    Args:
        label: The text that names the quantity.
        value: The SymPy expression to print.
    """
    print(f"  {label}: {simplify(value)}")


def main() -> None:
    """Print the chain of integrals for each of the six orders and the common value."""
    height = 4 - x**2 - 4 * z**2
    target = 4 * pi

    print("order 1: dy dx dz")
    inner_1 = integrate(1, (y, 0, height))
    show("inner, y from 0 to 4-x^2-4*z^2", inner_1)
    middle_1 = integrate(inner_1, (x, -2 * sqrt(1 - z**2), 2 * sqrt(1 - z**2)))
    show("middle, x between the two halves of the ellipse", middle_1)
    value_1 = simplify(integrate(middle_1, (z, -1, 1)))
    show("outer, z from -1 to 1", value_1)
    print()

    print("order 2: dy dz dx")
    inner_2 = integrate(1, (y, 0, height))
    show("inner, y from 0 to 4-x^2-4*z^2", inner_2)
    middle_2 = integrate(inner_2, (z, -sqrt(4 - x**2) / 2, sqrt(4 - x**2) / 2))
    show("middle, z between the two halves of the ellipse", middle_2)
    value_2 = simplify(integrate(middle_2, (x, -2, 2)))
    show("outer, x from -2 to 2", value_2)
    print()

    print("order 3: dx dy dz")
    inner_3 = integrate(1, (x, -half, half))
    show("inner, x from -half to half, with half = sqrt(4-4*z^2-y)", inner_3)
    middle_3 = integrate(2 * sqrt(c2 - y), (y, 0, c2))
    show("middle, y from 0 to c2, with c2 = 4-4*z^2", middle_3)
    outer_3 = (Rational(4, 3) * (4 - 4 * z**2) ** Rational(3, 2))
    value_3 = simplify(integrate(outer_3, (z, -1, 1)))
    show("outer, z from -1 to 1", value_3)
    print()

    print("order 4: dx dz dy")
    show("inner, x from -sqrt(4-y-4*z^2) to +sqrt(4-y-4*z^2)", 2 * sqrt(4 - y - 4 * z**2))
    middle_4 = integrate(2 * sqrt(radius**2 - 4 * z**2), (z, -radius / 2, radius / 2))
    show("middle, z between the two halves, with radius = sqrt(4-y)", middle_4)
    value_4 = simplify(integrate(pi * (4 - y) / 2, (y, 0, 4)))
    show("outer, y from 0 to 4", value_4)
    print()

    print("order 5: dz dy dx")
    show("inner, z from -sqrt(4-x^2-y)/2 to +sqrt(4-x^2-y)/2", sqrt(4 - x**2 - y))
    middle_5 = integrate(sqrt(s2 - y), (y, 0, s2))
    show("middle, y from 0 to s2, with s2 = 4-x^2", middle_5)
    value_5 = simplify(integrate(Rational(2, 3) * (4 - x**2) ** Rational(3, 2), (x, -2, 2)))
    show("outer, x from -2 to 2", value_5)
    print()

    print("order 6: dz dx dy")
    show("inner, z from -sqrt(4-y-x^2)/2 to +sqrt(4-y-x^2)/2", sqrt(4 - y - x**2))
    middle_6 = integrate(sqrt(radius**2 - x**2), (x, -radius, radius))
    show("middle, x between the two halves, with radius = sqrt(4-y)", middle_6)
    value_6 = simplify(integrate(pi * (4 - y) / 2, (y, 0, 4)))
    show("outer, y from 0 to 4", value_6)
    print()

    print("standard integrals used on the page")
    show("integral of (1-z^2)^(3/2) from z = -1 to 1", integrate((1 - z**2) ** Rational(3, 2), (z, -1, 1)))
    show("integral of (4-x^2)^(3/2) from x = -2 to 2", integrate((4 - x**2) ** Rational(3, 2), (x, -2, 2)))
    print()

    print("scaled check for f = x^2*z^2 with x = 2u, z = v, y = w")
    r_radius, theta = symbols("r_radius theta", positive=True)
    radial = integrate(r_radius**5 * (1 - r_radius**2), (r_radius, 0, 1))
    show("radial integral, r from 0 to 1", radial)
    angular = integrate(cos(theta) ** 2 * sin(theta) ** 2, (theta, 0, 2 * pi))
    show("angular integral, theta from 0 to 2*pi", angular)
    scaled = simplify(32 * radial * angular)
    show("32 times the product of the two", scaled)
    print(f"  scaled check = {float(scaled):.12f}, pi/3 = {float(pi / 3):.12f}")
    print()

    values = [value_1, value_2, value_3, value_4, value_5, value_6]
    print("all six orders")
    for index, value in enumerate(values, start=1):
        print(f"  order {index}: {simplify(value)}   difference from 4*pi: {simplify(value - target)}")
    print(f"  4*pi = {float(target):.12f}")


if __name__ == "__main__":
    main()
