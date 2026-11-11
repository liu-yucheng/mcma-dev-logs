"""Check the geometric description of the solid and estimate the integral.

The solid E is bounded by the paraboloid x = 4*y**2 + 4*z**2 and the plane x = 4.
This script checks the region description and estimates the triple integral of x
with Monte Carlo sampling.
"""

import numpy as np

random_generator = np.random.default_rng(20261109)

# The projection of E onto the yz-plane is the disk y**2 + z**2 <= 1, because
# the two surfaces meet where 4*y**2 + 4*z**2 = 4, that is, y**2 + z**2 = 1.
sample_count = 4000000
sample_y = random_generator.uniform(-1.0, 1.0, sample_count)
sample_z = random_generator.uniform(-1.0, 1.0, sample_count)
sample_x = random_generator.uniform(0.0, 4.0, sample_count)

inside = (4.0 * (sample_y**2 + sample_z**2) <= sample_x) & (sample_x <= 4.0)
box_volume = 4.0 * 2.0 * 2.0
estimate = box_volume * float(np.mean(sample_x * inside))
exact_value = 16.0 * np.pi / 3.0
standard_error = box_volume * float(np.std(sample_x * inside)) / np.sqrt(sample_count)

print(f"Monte Carlo estimate of the integral: {estimate:.5f}")
print(f"Exact value 16*pi/3:                  {exact_value:.5f}")
print(f"Estimated standard error:             {standard_error:.5f}")
print(f"Signed deviation:                     {estimate - exact_value:+.5f}")
print(f"Deviation in standard errors:         {(estimate - exact_value) / standard_error:+.2f}")

# Confirm the intersection curve of the two surfaces.
intersection_r = 1.0
paraboloid_height = 4.0 * intersection_r**2
print(f"At y^2+z^2=1 the paraboloid gives x={paraboloid_height:.3f}, the plane gives x=4.000")

# Confirm that the region is the region 4*r^2 <= x <= 4 with 0 <= r <= 1.
test_radii = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
for radius in test_radii:
    print(f"r={radius:.2f}: paraboloid x={4.0 * radius**2:.3f}, thickness={4.0 - 4.0 * radius**2:.3f}")
