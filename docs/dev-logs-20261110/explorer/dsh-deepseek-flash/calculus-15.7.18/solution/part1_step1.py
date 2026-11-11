"""Check the description of the solid and estimate the integral by sampling.

The solid E lies in the first octant, inside the cylinder y**2 + z**2 = 9, and
between the planes x = 0 and y = 3*x. This script confirms the three bounding
surfaces and estimates the triple integral of z by Monte Carlo sampling.
"""

import numpy as np

random_generator = np.random.default_rng(20261109)

# The cylinder cuts the first octant in the quarter disk 0 <= y <= 3,
# 0 <= z <= sqrt(9 - y**2). The plane y = 3*x then gives 0 <= x <= y/3.
sample_count = 4000000
sample_y = random_generator.uniform(0.0, 3.0, sample_count)
sample_z = random_generator.uniform(0.0, 3.0, sample_count)
sample_x = random_generator.uniform(0.0, 1.0, sample_count)

inside = (sample_y**2 + sample_z**2 <= 9.0) & (sample_x <= sample_y / 3.0)
box_volume = 3.0 * 3.0 * 1.0
estimate = box_volume * float(np.mean(sample_z * inside))
standard_error = box_volume * float(np.std(sample_z * inside)) / np.sqrt(sample_count)
exact_value = 27.0 / 8.0

print(f"Monte Carlo estimate of the integral: {estimate:.5f}")
print(f"Exact value 27/8:                     {exact_value:.5f}")
print(f"Estimated standard error:             {standard_error:.5f}")
print(f"Deviation in standard errors:         {(estimate - exact_value) / standard_error:+.2f}")
print(f"Sampled fraction inside E:            {float(np.mean(inside)):.5f}")

# Confirm the three surfaces that bound E.
print()
print("boundary check")
for y_value in (0.0, 1.5, 3.0):
    print(
        f"  y={y_value:.1f}: cylinder top z={np.sqrt(9.0 - y_value**2):.4f}, "
        f"plane y=3x gives x={y_value / 3.0:.4f}"
    )
print(f"  at y=3 the cylinder height is {np.sqrt(9.0 - 3.0**2):.1f}, so E closes at y=3")
print(f"  the plane x=y/3 meets the rim y=3 at x={3.0 / 3.0:.1f}")

# The volume of the box that contains E, for scale.
print(f"  box 0<=x<=1, 0<=y<=3, 0<=z<=3 has volume {box_volume:.1f}")
