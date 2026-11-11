"""Describe the silo surface and check its principal dimensions.

The silo is a cylinder of radius 3 and height 10 with a hemisphere of radius 3
on top. This script states the piecewise surface, the top height, and the
capacity, so that the drawing can be checked against exact numbers.
"""

from math import pi


def main():
    """Print the surface description and the derived dimensions."""
    radius = 3.0
    cylinder_height = 10.0
    top_height = cylinder_height + radius

    print("silo description")
    print(f"  cylinder: r = {radius}, 0 <= z <= {cylinder_height}")
    print(f"  hemisphere: x^2 + y^2 + (z - {cylinder_height})^2 = {radius**2}, "
          f"z >= {cylinder_height}")
    print(f"  base disk: r <= {radius} at z = 0")
    print()
    print(f"diameter of the silo: {2 * radius}")
    print(f"height of the cylindrical wall: {cylinder_height}")
    print(f"height of the domed roof: {radius}")
    print(f"total height at the apex: {top_height}")
    print()
    print("surface area")
    wall = 2 * pi * radius * cylinder_height
    dome = 2 * pi * radius**2
    base = pi * radius**2
    print(f"  cylindrical wall: 2 pi r h = {wall:.6f}")
    print(f"  hemisphere roof: 2 pi r^2 = {dome:.6f}")
    print(f"  base disk: pi r^2 = {base:.6f}")
    print()
    print("capacity")
    cylinder_volume = pi * radius**2 * cylinder_height
    dome_volume = (2.0 / 3.0) * pi * radius**3
    print(f"  cylinder: pi r^2 h = {cylinder_volume:.6f}")
    print(f"  hemisphere: (2/3) pi r^3 = {dome_volume:.6f}")
    print(f"  total: {cylinder_volume + dome_volume:.6f} = {108 * pi:.6f}")


if __name__ == "__main__":
    main()
