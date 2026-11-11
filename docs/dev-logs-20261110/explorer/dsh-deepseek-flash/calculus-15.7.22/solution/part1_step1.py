"""Check the description of the solid and estimate its volume by sampling.

The solid is bounded by the cylinder x**2 + z**2 = 4 and by the planes y = -1 and
y + z = 4. The script confirms that the slanted plane lies above the flat plane on
the whole cylinder, then estimates the volume with Monte Carlo sampling.
"""

import numpy as np

random_generator = np.random.default_rng(20261110)

# The two planes must not cross inside the cylinder. On the cylinder |z| <= 2, so
# the roof height y = 4 - z is at least 4 - 2 = 2, which is above the floor y = -1.
height_values = 4.0 - np.linspace(-2.0, 2.0, 5)
print(f"roof height y = 4 - z at z = -2, -1, 0, 1, 2: {np.round(height_values, 3)}")
print(f"minimum roof height: {height_values.min():.3f}, floor height: -1.000")

# The projection of the solid onto the xz-plane is the disk x**2 + z**2 <= 4.
disk_area = 4.0 * np.pi
print(f"projection area, pi * 2**2: {disk_area:.6f}")

# The thickness of the solid above a point (x, z) of the disk is 4 - z - (-1) = 5 - z.
for z_value in (-2.0, 0.0, 2.0):
    print(f"z = {z_value:+.1f}: thickness 5 - z = {5.0 - z_value:.3f}")

# Monte Carlo estimate over the box [-2, 2] x [-1, 6] x [-2, 2].
sample_count = 4_000_000
sample_x = random_generator.uniform(-2.0, 2.0, sample_count)
sample_y = random_generator.uniform(-1.0, 6.0, sample_count)
sample_z = random_generator.uniform(-2.0, 2.0, sample_count)
inside = (sample_x**2 + sample_z**2 <= 4.0) & (sample_y >= -1.0) & (sample_y <= 4.0 - sample_z)
box_volume = 4.0 * 7.0 * 4.0
estimate = box_volume * float(np.mean(inside))
standard_error = box_volume * float(np.std(inside)) / np.sqrt(sample_count)
exact_value = 20.0 * np.pi
print(f"Monte Carlo volume estimate: {estimate:.5f}")
print(f"exact value 20*pi:           {exact_value:.5f}")
print(f"estimated standard error:    {standard_error:.5f}")
print(f"deviation in standard errors: {(estimate - exact_value) / standard_error:+.2f}")
