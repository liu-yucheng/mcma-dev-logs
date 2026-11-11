"""Check the description of the solid and its volume.

The solid E is the part of the cylinder y**2 + z**2 = 9 between the planes
x = -2 and x = 2. This script confirms the two defining inequalities and
computes the volume from one iterated integral.
"""

from sympy import integrate, pi, simplify, sqrt, symbols

x, y, z = symbols("x y z", real=True)

cylinder_radius = 3
plane_distance = 4

print("solid: y^2 + z^2 <= 9 with -2 <= x <= 2")
print(f"cylinder radius: {cylinder_radius}")
print(f"distance between the planes x = -2 and x = 2: {plane_distance}")


def is_inside(point_x, point_y, point_z):
    """Return True when the point satisfies both defining inequalities."""
    return abs(point_x) <= 2 and point_y**2 + point_z**2 <= 9


samples = [
    (0, 0, 0),
    (2, 0, 3),
    (-2, 3, 0),
    (2.1, 0, 0),
    (0, 2, 2.6),
    (0, 0, 3.1),
]
print("membership checks:")
for point_x, point_y, point_z in samples:
    print(f"  ({point_x}, {point_y}, {point_z}) inside E: {is_inside(point_x, point_y, point_z)}")

# Volume from the order dz dy dx. The middle integral is the area of the disk.
inner = integrate(1, (z, -sqrt(9 - y**2), sqrt(9 - y**2)))
print(f"inner integral over z: {simplify(inner)}")
disk_area = integrate(inner, (y, -3, 3))
print(f"middle integral over y (area of the disk): {simplify(disk_area)}")
volume = simplify(integrate(disk_area, (x, -2, 2)))
print(f"outer integral over x: {volume}")
print(f"volume as a decimal: {float(volume.evalf(15)):.9f}")

# The same disk area from the other slicing, with z fixed.
disk_area_again = integrate(2 * sqrt(9 - z**2), (z, -3, 3))
print(f"disk area from the slicing with z fixed: {simplify(disk_area_again)}")
assert simplify(disk_area_again - disk_area) == 0

geometric_volume = pi * cylinder_radius**2 * plane_distance
print(f"pi * r^2 * length: {geometric_volume}")
print(f"pi * r^2 * length as a decimal: {float(geometric_volume.evalf(15)):.9f}")
assert simplify(volume - geometric_volume) == 0
print("the iterated integral and the geometric formula agree")
