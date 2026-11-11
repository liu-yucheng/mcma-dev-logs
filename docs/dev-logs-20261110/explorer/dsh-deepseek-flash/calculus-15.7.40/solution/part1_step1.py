"""Check the description of the solid and estimate its mass by sampling.

The solid E is bounded by the parabolic cylinder z = 1 - y**2 and by the planes
x + z = 1, x = 0, and z = 0.  This script checks the resulting inequalities and
estimates the mass, with density 4, by Monte Carlo sampling of the bounding box.
"""

import numpy as np

random_generator = np.random.default_rng(20261109)

# The bounding box is 0 <= x <= 1, -1 <= y <= 1, and 0 <= z <= 1.
sample_count = 4000000
sample_x = random_generator.uniform(0.0, 1.0, sample_count)
sample_y = random_generator.uniform(-1.0, 1.0, sample_count)
sample_z = random_generator.uniform(0.0, 1.0, sample_count)

inside = (sample_z <= 1.0 - sample_y**2) & (sample_x <= 1.0 - sample_z)
box_volume = 1.0 * 2.0 * 1.0
weighted = 4.0 * inside
estimate = box_volume * float(np.mean(weighted))
exact_value = 16.0 / 5.0
standard_error = box_volume * float(np.std(weighted)) / np.sqrt(sample_count)

print(f"bounding box volume:                  {box_volume:.3f}")
print(f"Monte Carlo estimate of the mass:     {estimate:.5f}")
print(f"Exact value 16/5:                     {exact_value:.5f}")
print(f"Estimated standard error:             {standard_error:.5f}")
print(f"Deviation in standard errors:         {(estimate - exact_value) / standard_error:+.2f}")

# The two surfaces z = 1 - y**2 and x + z = 1 meet where both equalities hold.
# On the floor z = 0 the cylinder gives y = +-1, and the plane gives x = 1.
print("On the floor z = 0: the cylinder gives y = +-1.000, the plane gives x = 1.000")
print(f"At y = 0 the cylinder height is {1.0 - 0.0**2:.3f}, so the solid touches z = 1 only at x = 0.")

# The thickness in x shrinks to zero as z rises to 1.
print("Thickness in x at fixed y = 0.5, as a function of z:")
for z_value in (0.0, 0.25, 0.5, 0.75):
    roof = 1.0 - z_value
    print(f"  z={z_value:.2f}: x runs from 0.000 to {roof:.3f}")
