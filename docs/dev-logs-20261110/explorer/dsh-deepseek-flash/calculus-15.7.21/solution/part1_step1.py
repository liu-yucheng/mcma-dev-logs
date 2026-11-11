"""Check the region bounded by y = x**2, z = 0, and y + z = 1 by sampling.

The solid sits above the parabola y = x**2 and below the plane y + z = 1, so it
projects onto the region x**2 <= y <= 1 with -1 <= x <= 1. This script confirms
that description and estimates the volume by Monte Carlo sampling.
"""

import numpy as np

random_generator = np.random.default_rng(20261110)

sample_count = 4000000
sample_x = random_generator.uniform(-1.0, 1.0, sample_count)
sample_y = random_generator.uniform(0.0, 1.0, sample_count)
sample_z = random_generator.uniform(0.0, 1.0, sample_count)

inside = (sample_y >= sample_x**2) & (sample_z <= 1.0 - sample_y)
box_volume = 2.0 * 1.0 * 1.0
estimate = box_volume * float(np.mean(inside))
standard_error = box_volume * float(np.std(inside)) / np.sqrt(sample_count)
exact_value = 8.0 / 15.0

print(f"Monte Carlo estimate of the volume: {estimate:.5f}")
print(f"Exact value 8/15:                   {exact_value:.5f}")
print(f"Estimated standard error:           {standard_error:.5f}")
print(f"Deviation in standard errors:       {(estimate - exact_value) / standard_error:+.2f}")
print(f"Sampled fraction inside the solid:  {float(np.mean(inside)):.5f}")

print()
print("boundary check")
for coordinate in (-1.0, -0.5, 0.0, 0.5, 1.0):
    print(f"  x={coordinate:+.1f}: the wall y=x^2 gives y={coordinate**2:.4f}")
for height_y in (0.0, 0.5, 1.0):
    print(f"  y={height_y:.1f}: the roof y+z=1 gives z={1.0 - height_y:.4f}")
print(f"  the two bounding curves meet where x^2=1: x=+1 and x=-1 give y={1.0:.1f}")
print(f"  box -1<=x<=1, 0<=y<=1, 0<=z<=1 has volume {box_volume:.1f}")
