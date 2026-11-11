"""Measure the base ellipse, the horizontal cross-sections, and the height of the solid.

The solid E is bounded below by the plane y = 0 and above by the elliptic paraboloid
y = 4 - x**2 - 4*z**2.  This script measures the geometry that the six orders of
integration use.

Usage:
    python part1_step1.py
"""

from math import pi, sqrt

from mpmath import mp, quad

mp.dps = 20


def inside(x_value: float, y_value: float, z_value: float) -> bool:
    """Return True when the point satisfies both defining inequalities.

    Args:
        x_value: The x coordinate.
        y_value: The y coordinate.
        z_value: The z coordinate.

    Returns:
        True when x**2 + 4*z**2 <= 4 and 0 <= y <= 4 - x**2 - 4*z**2.
    """
    disk = x_value**2 + 4.0 * z_value**2
    return disk <= 4.0 and 0.0 <= y_value <= 4.0 - disk


def main() -> None:
    """Print the base, the cross-sections, the volume, and four sample points."""
    print("base ellipse  x**2 + 4*z**2 = 4, that is x**2/4 + z**2 = 1")
    print("  semi-axis along x: 2")
    print("  semi-axis along z: 1")
    print(f"  area of the base: {pi * 2.0 * 1.0:.12f} = 2*pi")
    print()

    print("horizontal cross-section at height y: a = sqrt(4-y), b = a/2, area = pi*(4-y)/2")
    for y_value in (0.0, 1.0, 2.0, 3.0, 4.0):
        a_value = sqrt(max(4.0 - y_value, 0.0))
        b_value = a_value / 2.0
        print(f"  y = {y_value:4.1f}  a = {a_value:8.6f}  b = {b_value:8.6f}  area = {pi * a_value * b_value:.8f}")
    print()

    volume = quad(lambda y_value: pi * (4.0 - y_value) / 2.0, [0.0, 4.0])
    print(f"volume by summing the cross-section areas: {mp.nstr(volume, 18)}")
    print(f"four pi:                                   {mp.nstr(4.0 * mp.pi, 18)}")
    print()

    print("vertical fibres in the y-direction")
    for x_value, z_value in ((0.0, 0.0), (0.8, 0.5), (1.5, 0.4)):
        height = 4.0 - x_value**2 - 4.0 * z_value**2
        print(f"  at x = {x_value:3.1f}, z = {z_value:3.1f} the fibre runs from y = 0 to y = {height:.6f}")
    print()

    print("membership tests")
    for x_value, y_value, z_value in ((1.0, 2.0, 0.3), (0.5, 2.0, 0.5), (2.0, 0.5, 0.5), (0.5, 3.0, 0.5)):
        print(f"  ({x_value:3.1f}, {y_value:3.1f}, {z_value:3.1f}) inside E: {inside(x_value, y_value, z_value)}")


if __name__ == "__main__":
    main()
