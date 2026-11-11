"""Check the description of the wedge and estimate its volume by sampling.

The wedge lies in the first octant, inside the cylinder y**2 + z**2 = 1, between the
planes y = x and x = 1. The script checks the corner points and estimates the volume
with Monte Carlo sampling over the unit cube.
"""

import numpy as np

random_generator = np.random.default_rng(20261110)

# Corner points of the wedge. Each one must satisfy all four inequalities.
corner_points = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (0.0, 0.0, 1.0)]
print("corner points and their membership in the wedge:")
for x_value, y_value, z_value in corner_points:
    inside_cylinder = y_value**2 + z_value**2 <= 1.0 + 1e-12
    above_plane = x_value >= y_value - 1e-12
    print(f"  ({x_value:.0f}, {y_value:.0f}, {z_value:.0f}): "
          f"y^2+z^2 = {y_value**2 + z_value**2:.3f} <= 1 is {inside_cylinder}, "
          f"x >= y is {above_plane}")

# On the plane y = x the cylinder gives the quarter circle x = y, y**2 + z**2 = 1.
print("intersection of y = x with the cylinder: y = x, y**2 + z**2 = 1, y >= 0")

# The projection onto the xy-plane is the triangle 0 <= y <= x <= 1 with area 1/2.
print(f"area of the projection triangle 0 <= y <= x <= 1: {0.5:.3f}")

sample_count = 4_000_000
sample_x = random_generator.uniform(0.0, 1.0, sample_count)
sample_y = random_generator.uniform(0.0, 1.0, sample_count)
sample_z = random_generator.uniform(0.0, 1.0, sample_count)
inside = (sample_y**2 + sample_z**2 <= 1.0) & (sample_x >= sample_y)
estimate = float(np.mean(inside))
standard_error = float(np.std(inside)) / np.sqrt(sample_count)
exact_value = np.pi / 4.0 - 1.0 / 3.0
print(f"Monte Carlo volume estimate over the unit cube: {estimate:.6f}")
print(f"exact value pi/4 - 1/3:                         {exact_value:.6f}")
print(f"estimated standard error:                        {standard_error:.6f}")
print(f"deviation in standard errors:                    {(estimate - exact_value) / standard_error:+.2f}")

# Slice check: at fixed y the section is the rectangle y <= x <= 1, 0 <= z <= sqrt(1-y^2).
for y_value in (0.0, 0.5, 0.6, 1.0):
    print(f"y = {y_value:.1f}: x from {y_value:.1f} to 1, z from 0 to {np.sqrt(max(0.0, 1.0 - y_value**2)):.3f}")
