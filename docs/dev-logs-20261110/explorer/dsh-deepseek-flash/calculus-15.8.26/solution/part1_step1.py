"""Find the volume that the cylinder r = a cos(theta) cuts out of a sphere.

The derivation keeps the radius a symbolic. The script prints each stage: the
vertical extent, the antiderivative in r, the slice volume on the wall, the
integral over theta, and the volume for a = 1 and a = 2.
"""

from sympy import Rational, Symbol, cos, integrate, pi, simplify, sin, sqrt


def main():
    """Carry out the derivation symbolically."""
    a = Symbol("a", positive=True)
    theta = Symbol("theta", real=True)
    radius = Symbol("r", positive=True)

    print("sphere: x^2 + y^2 + z^2 = a^2, so z = +-sqrt(a^2 - r^2)")
    print("cylinder: r = a cos(theta) with -pi/2 <= theta <= pi/2")
    print("solid: 0 <= r <= a cos(theta), -sqrt(a^2 - r^2) <= z <= sqrt(a^2 - r^2)")

    vertical_extent = simplify(2 * sqrt(a**2 - (a * cos(theta)) ** 2))
    print(f"vertical extent on the wall of the cylinder: {vertical_extent}")

    antiderivative = Rational(2, 3) * (a**3 - (a**2 - radius**2) ** Rational(3, 2))
    print()
    print("antiderivative of 2 sqrt(a^2 - r^2) r with respect to r:")
    print(f"  {antiderivative}")

    residual = simplify((a**2 - (a * cos(theta)) ** 2) - a**2 * sin(theta) ** 2)
    print(f"check a^2 - (a cos(theta))^2 - a^2 sin^2(theta) = {residual}")
    print("so the height at the wall is a |sin(theta)|\n")

    slice_volume = Rational(2, 3) * a**3 * (1 - abs(sin(theta)))
    print("slice volume at angle theta:")
    print(f"  (2/3) a^3 (1 - |sin(theta)|)")

    half_angle = Symbol("phi", positive=True)
    sine_cube = integrate(sin(half_angle) ** 3, (half_angle, 0, pi / 2))
    print()
    print(f"integral of sin^3 over [0, pi/2]: {sine_cube}")

    right_half = integrate(Rational(2, 3) * a**3 * (1 - sin(theta) ** 3), (theta, 0, pi / 2))
    print(f"half of the theta integral: {simplify(right_half)}")

    volume = simplify(2 * right_half)
    closed = Rational(2, 3) * a**3 * (pi - Rational(4, 3))
    print(f"total volume: {volume}")
    print(f"difference from (2/3) a^3 (pi - 4/3): {simplify(volume - closed)}")

    for value in (1, 2):
        numeric = volume.subs(a, value)
        print(f"a = {value}: V = {simplify(numeric)} = {float(numeric):.6f}")


if __name__ == "__main__":
    main()
