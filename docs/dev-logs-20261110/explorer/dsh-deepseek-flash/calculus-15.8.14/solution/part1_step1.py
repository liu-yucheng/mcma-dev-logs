"""Locate the curve where the two paraboloids meet.

The solid lies between the paraboloid z = x^2 + y^2 and the paraboloid
z = 5 - x^2 - y^2. This script finds the intersection circle and checks that
both surfaces agree on it.
"""

from math import pi, sqrt

from sympy import Rational, solve, symbols


def main():
    """Solve for the radius and the height of the intersection circle."""
    radius = symbols("radius", positive=True)
    intersections = solve(radius**2 - (5 - radius**2), radius)
    circle_radius = [value for value in intersections if value.is_real][0]
    circle_height = Rational(5, 2)

    print("intersection equation: r^2 = 5 - r^2")
    print(f"circle radius  r = {circle_radius} = {float(circle_radius):.6f}")
    print(f"circle height  z = {circle_height} = {float(circle_height):.6f}")

    lower = float(circle_radius) ** 2
    upper = 5.0 - float(circle_radius) ** 2
    print(f"lower surface at the rim: z = {lower:.6f}")
    print(f"upper surface at the rim: z = {upper:.6f}")

    profile_radius = 0.8
    print()
    print("sample vertical cross-section at r = 0.8:")
    print(f"  lower surface z = {profile_radius**2:.6f}")
    print(f"  upper surface z = {5.0 - profile_radius**2:.6f}")

    top_height = 5.0
    print()
    print(f"highest point of the solid: z = {top_height:.6f} on the axis")
    print(f"widest extent: r = {float(circle_radius):.6f}")
    print(f"circumference of the rim: {2 * pi * float(circle_radius):.6f}")


if __name__ == "__main__":
    main()
