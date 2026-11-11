"""Sanity checks for the graph of part (b) of problem 15.8.26 (a = 1).

The sphere is r^2 + z^2 = 1 and the cylinder is r = cos(theta) (theta where
cos(theta) >= 0).  On the intersection we have r = cos(theta) AND
r^2 + z^2 = 1, hence z^2 = 1 - cos^2(theta) = sin^2(theta), i.e. the
Viviani curve  r = cos(theta),  z = +/- sin(theta),  |theta| <= pi/2.
In Cartesian coordinates the curve is x = cos^2(theta), y = cos(theta)
sin(theta), z = +/- sin(theta); the cylinder itself is the circle
(x - 1/2)^2 + y^2 = 1/4 of radius 1/2 centred at (1/2, 0).
"""

import numpy as np

a = 1.0
th = np.linspace(-np.pi / 2, np.pi / 2, 9)
r_cyl = a * np.cos(th)
z2_sphere = a**2 - r_cyl**2
z2_viv = np.sin(th) ** 2
print("theta       r_cyl      z^2 (sphere)   z^2 (Viviani)")
for t, rc, zs, zv in zip(th, r_cyl, z2_sphere, z2_viv):
    print(f"{t:8.5f}  {rc:8.6f}   {zs:9.6f}      {zv:9.6f}")
assert np.allclose(z2_sphere, z2_viv), "intersection z^2 must equal sin^2(theta)"

# Cartesian form of the cylinder: x^2 + y^2 = a*x.
x_c = r_cyl * np.cos(th)
y_c = r_cyl * np.sin(th)
assert np.allclose(x_c**2 + y_c**2, a * x_c), "cylinder is x^2+y^2 = x"
assert np.allclose((x_c - 0.5) ** 2 + y_c**2, 0.25), "circle (x-1/2)^2+y^2=1/4"
print("OK: intersection curve is r = cos(theta), z = +/- sin(theta)")
print("OK: cylinder is the circle (x-1/2)^2 + y^2 = 1/4 (a = 1)")
