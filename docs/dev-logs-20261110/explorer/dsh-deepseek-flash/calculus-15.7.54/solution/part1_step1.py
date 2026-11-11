"""Check the geometry of the paraboloid cap and estimate the average value.

The solid E lies between the plane z = 0 and the paraboloid z = 1 - x**2 - y**2.
This script confirms the circular projection, tabulates the cap height, and
estimates the average value of f = x**2*z + y**2*z by Monte Carlo sampling.
"""

import numpy as np

random_generator = np.random.default_rng(20261110)

# The paraboloid meets the plane z = 0 where 1 - x**2 - y**2 = 0, so the
# projection of E onto the xy-plane is the unit disk x**2 + y**2 <= 1.
print("cap height of the paraboloid above the unit disk:")
for radius in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"  r = {radius:.2f}:  z = 1 - r^2 = {1.0 - radius**2:.4f}")

sample_count = 4_000_000
sample_x = random_generator.uniform(-1.0, 1.0, sample_count)
sample_y = random_generator.uniform(-1.0, 1.0, sample_count)
sample_z = random_generator.uniform(0.0, 1.0, sample_count)

inside = (sample_x**2 + sample_y**2 <= 1.0) & (sample_z <= 1.0 - sample_x**2 - sample_y**2)
box_volume = 2.0 * 2.0 * 1.0
volume_estimate = box_volume * float(np.mean(inside))

# The average value of f over E is the mean of f over uniformly sampled points of E.
function_values = (sample_x**2 + sample_y**2) * sample_z
inside_values = function_values[inside]
average_estimate = float(np.mean(inside_values))
average_error = float(np.std(inside_values)) / np.sqrt(inside_values.size)

print()
print(f"Monte Carlo estimate of V(E): {volume_estimate:.5f}   (exact pi/2 = {np.pi / 2:.5f})")
print(f"Monte Carlo estimate of f_ave: {average_estimate:.5f}   (target 1/12 = {1.0 / 12.0:.5f})")
print(f"Estimated standard error:      {average_error:.5f}")
print(f"Signed deviation:              {average_estimate - 1.0 / 12.0:+.5f}")
print(f"Deviation in standard errors:  {(average_estimate - 1.0 / 12.0) / average_error:+.2f}")
print(f"Accepted sample count inside E: {inside_values.size}")
