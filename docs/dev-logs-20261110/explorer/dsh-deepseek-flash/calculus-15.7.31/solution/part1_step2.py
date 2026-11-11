"""Evaluate the six orders of integration for Exercise 15.7.31.

Each entry lists the integrations from the innermost variable to the
outermost one. The script evaluates every order for the constant integrand 1
and for the test integrand y**2*z**2, then checks that all six values agree.
"""

from sympy import Rational, integrate, simplify, sqrt, symbols

x, y, z = symbols("x y z")

ORDERS = {
    "dz dy dx": [("z", 0, 2 - y / 2), ("y", x**2, 4), ("x", -2, 2)],
    "dz dx dy": [("z", 0, 2 - y / 2), ("x", -sqrt(y), sqrt(y)), ("y", 0, 4)],
    "dy dz dx": [("y", x**2, 4 - 2 * z), ("z", 0, 2 - x**2 / 2), ("x", -2, 2)],
    "dy dx dz": [("y", x**2, 4 - 2 * z), ("x", -sqrt(4 - 2 * z), sqrt(4 - 2 * z)),
                 ("z", 0, 2)],
    "dx dy dz": [("x", -sqrt(y), sqrt(y)), ("y", 0, 4 - 2 * z), ("z", 0, 2)],
    "dx dz dy": [("x", -sqrt(y), sqrt(y)), ("z", 0, 2 - y / 2), ("y", 0, 4)],
}


def evaluate(integrand, order):
    """Integrate the integrand through one order from the inside out."""
    result = integrand
    for variable, low, high in order:
        result = integrate(result, (variable, low, high))
    return simplify(result)


def main():
    """Print the value of every order for both test integrands."""
    for label, integrand in (("f = 1", 1), ("f = y^2 z^2", y**2 * z**2)):
        print(f"integrand {label}")
        values = {}
        for name, order in ORDERS.items():
            values[name] = evaluate(integrand, order)
            print(f"  {name:>9} : {values[name]}")
        assert len(set(values.values())) == 1
        print(f"  all six orders agree: {next(iter(values.values()))}")
        print(f"  decimal            : {float(next(iter(values.values()))):.12f}")

    print("stages for order dz dy dx with f = 1")
    inner = integrate(1, (z, 0, 2 - y / 2))
    middle = simplify(integrate(inner, (y, x**2, 4)))
    outer = simplify(integrate(middle, (x, -2, 2)))
    print(f"  2 - y/2 -> {middle} -> {outer}")
    assert outer == Rational(128, 15)


if __name__ == "__main__":
    main()
