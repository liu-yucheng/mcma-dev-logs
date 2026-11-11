"""Check the solid of Exercise 15.7.31 and integrate 1 over it.

The solid E is bounded by the parabolic cylinder y = x**2, the plane z = 0,
and the plane y + 2*z = 4. This script tests sample points against the three
defining inequalities, then integrates the constant 1 over E in the order
dz dy dx. It prints the inner, the middle, and the outer integral and checks
the volume against a cross-section count.
"""

from sympy import Rational, integrate, simplify, symbols

x, y, z = symbols("x y z")


def in_solid(point):
    """Return True when the point satisfies the three defining inequalities."""
    px, py, pz = point
    return py >= px**2 and pz >= 0 and py + 2 * pz <= 4


def main():
    """Print the membership tests, the three stages, and the volume check."""
    samples = [
        ((0, 1, 0.5), True),
        ((1, 1.5, 0.4), True),
        ((-1.5, 3, 0.2), True),
        ((0, 4, 0), True),
        ((2, 3, 0.5), False),
        ((0, 1, 1.6), False),
        ((0, 4.2, 0.1), False),
        ((0, 2, -0.5), False),
    ]
    print("membership tests for y >= x**2, z >= 0, y + 2*z <= 4")
    for point, expected in samples:
        got = in_solid(point)
        print(f"  {str(point):>16}  in E = {got!s:>5}  expected {expected!s:>5}")
        assert got is expected

    inner = integrate(1, (z, 0, 2 - y / 2))
    middle = simplify(integrate(inner, (y, x**2, 4)))
    volume = simplify(integrate(middle, (x, -2, 2)))
    print("order dz dy dx")
    print(f"  inner  int_0^(2-y/2) 1 dz        = {inner}")
    print(f"  middle int_(x^2)^4 (2 - y/2) dy  = {middle}")
    print(f"  outer  int_(-2)^2 A(x) dx        = {volume}")
    print(f"  decimal volume                   = {float(volume):.12f}")

    big_triangle = Rational(1, 2) * 4 * 2
    cut_trapezoid = x**2 * (2 - x**2 / 4)
    section = simplify(big_triangle - cut_trapezoid)
    assert simplify(section - middle) == 0
    print(f"  cross-section area A(x)          = {section}")
    print(f"  big yz triangle                  = {big_triangle}")
    print(f"  trapezoid removed at fixed x     = {cut_trapezoid}")
    assert simplify(integrate(section, (x, -2, 2)) - volume) == 0
    print("  cross-section count agrees")


if __name__ == "__main__":
    main()
