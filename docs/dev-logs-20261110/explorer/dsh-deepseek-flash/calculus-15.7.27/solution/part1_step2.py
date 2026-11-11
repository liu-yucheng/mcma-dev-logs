"""Evaluate the iterated integral and confirm the volume of the pyramid with SymPy.

The integral is int_0^1 int_0^{1-x} int_0^{2-2z} dy dz dx. The script integrates
from the inside out, compares the result with the pyramid formula, and checks the
volume again with horizontal slices.
"""

from sympy import Rational, expand, integrate, symbols

x, y, z = symbols("x y z", real=True)


def main():
    """Print every stage of the integration and both independent checks."""
    inner = integrate(1, (y, 0, 2 - 2 * z))
    middle = integrate(inner, (z, 0, 1 - x))
    outer = integrate(middle, (x, 0, 1))
    print(f"inner integral over y:                 {inner}")
    print(f"middle integral over z:                {middle}")
    print(f"middle integral expanded:              {expand(middle)}")
    print(f"outer integral over x:                 {outer}")
    print(f"decimal value:                         {float(outer):.12f}")

    slice_area = integrate(2 - 2 * z, (z, 0, 1 - x))
    trapezoid = Rational(1, 2) * (2 + 2 * x) * (1 - x)
    print(f"slice area at fixed x, integral:       {slice_area}")
    print(f"slice area at fixed x, trapezoid:      {expand(trapezoid)}")
    print(f"slice area at x = 1/2:                 {slice_area.subs(x, Rational(1, 2))}")
    assert expand(trapezoid) == expand(slice_area)

    pyramid = Rational(1, 3) * 2 * 1
    print(f"pyramid formula (1/3) * 2 * 1:         {pyramid}")

    slices = integrate(2 * (1 - z) ** 2, (z, 0, 1))
    print(f"horizontal slices, integral over z:    {slices}")

    assert outer == Rational(2, 3)
    assert pyramid == Rational(2, 3)
    assert slices == Rational(2, 3)
    print("all three routes give 2/3")


if __name__ == "__main__":
    main()
