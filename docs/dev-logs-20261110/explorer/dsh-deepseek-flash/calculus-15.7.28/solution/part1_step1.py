"""Check the reading of the solid and estimate its volume by sampling.

The iterated integral has the order dx dz dy, so the solid is the set of points
with 0 <= y <= 2, 0 <= z <= 2 - y, and 0 <= x <= 4 - y**2.  This script checks
that description against the bounding surfaces and estimates the volume with
Monte Carlo sampling.
"""

import numpy as np

random_generator = np.random.default_rng(20261110)

print("Bounding surfaces named by the three sets of limits")
print("  x = 4 - y^2   parabolic cylinder, curved front face")
print("  z = 2 - y     top plane, independent of x")
print("  z = 0         bottom plane")
print("  x = 0         back plane")
print("  y = 0         rectangle 0 <= x <= 4, 0 <= z <= 2")

# The limits must stay ordered on the whole range of y.
print()
for height in (0.0, 0.5, 1.0, 1.5, 2.0):
    x_limit = 4.0 - height**2
    z_limit = 2.0 - height
    print(f"y = {height:.2f}: x runs 0 to {x_limit:.3f}, z runs 0 to {z_limit:.3f}")

# Monte Carlo over the box [0, 4] x [0, 2] x [0, 2].
sample_count = 4000000
sample_y = random_generator.uniform(0.0, 2.0, sample_count)
sample_z = random_generator.uniform(0.0, 2.0, sample_count)
sample_x = random_generator.uniform(0.0, 4.0, sample_count)

inside_solid = (sample_z <= 2.0 - sample_y) & (sample_x <= 4.0 - sample_y**2)
box_volume = 4.0 * 2.0 * 2.0
estimate = box_volume * float(np.mean(inside_solid))
standard_error = box_volume * float(np.std(inside_solid)) / np.sqrt(sample_count)
exact_volume = 20.0 / 3.0

print()
print(f"sampled volume:        {estimate:.5f}")
print(f"volume 20/3:           {exact_volume:.5f}")
print(f"standard error:        {standard_error:.5f}")
print(f"deviation in errors:   {(estimate - exact_volume) / standard_error:+.2f}")
print(f"sampled share inside:  {float(np.mean(inside_solid)):.5f}")
