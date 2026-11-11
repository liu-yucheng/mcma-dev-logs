"""Check the region between the two paraboloids by Monte Carlo sampling.

The paraboloids y = x**2 + z**2 and y = 8 - x**2 - z**2 meet on the circle
x**2 + z**2 = 4 at height y = 4. This script confirms that boundary and
estimates the volume of the enclosed solid by sampling.
"""

import numpy as np

random_generator = np.random.default_rng(20261110)

sample_count = 4000000
sample_x = random_generator.uniform(-2.0, 2.0, sample_count)
sample_z = random_generator.uniform(-2.0, 2.0, sample_count)
sample_y = random_generator.uniform(0.0, 8.0, sample_count)

radius_squared = sample_x**2 + sample_z**2
inside = (sample_y >= radius_squared) & (sample_y <= 8.0 - radius_squared)
box_volume = 4.0 * 4.0 * 8.0
estimate = box_volume * float(np.mean(inside))
standard_error = box_volume * float(np.std(inside)) / np.sqrt(sample_count)
exact_value = 16.0 * np.pi

print(f"Monte Carlo estimate of the volume: {estimate:.5f}")
print(f"Exact value 16*pi:                  {exact_value:.5f}")
print(f"Estimated standard error:           {standard_error:.5f}")
print(f"Deviation in standard errors:       {(estimate - exact_value) / standard_error:+.2f}")
print(f"Sampled fraction inside the solid:  {float(np.mean(inside)):.5f}")

print()
print("boundary check")
for radius in (0.0, 1.0, 2.0):
    lower = radius**2
    upper = 8.0 - radius**2
    print(f"  r={radius:.1f}: lower paraboloid y={lower:.4f}, upper paraboloid y={upper:.4f}")
print(f"  the two surfaces agree at r=2: {2.0**2:.1f} = {8.0 - 2.0**2:.1f}")
print(f"  the greatest separation is at r=0: {8.0 - 0.0**2:.1f} - {0.0**2:.1f} = {8.0:.1f}")
print(f"  box -2<=x<=2, -2<=z<=2, 0<=y<=8 has volume {box_volume:.1f}")
