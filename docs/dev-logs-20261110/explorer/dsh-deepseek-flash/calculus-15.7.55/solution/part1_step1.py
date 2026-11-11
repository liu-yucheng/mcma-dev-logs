"""Check the sign of the integrand and estimate the integral over the ellipsoid.

The integrand g = 1 - x**2 - 2*y**2 - 3*z**2 is positive inside the ellipsoid
x**2 + 2*y**2 + 3*z**2 < 1 and negative outside it. This script tests that
claim on random points, reports the three axis intercepts, and estimates the
volume and the integral over the ellipsoid by Monte Carlo sampling.
"""

import numpy as np

random_generator = np.random.default_rng(20261110)


def integrand(x_value, y_value, z_value):
    """Return the value of 1 - x**2 - 2*y**2 - 3*z**2."""
    return 1.0 - x_value**2 - 2.0 * y_value**2 - 3.0 * z_value**2


print("semi-axes of the ellipsoid x^2 + 2 y^2 + 3 z^2 = 1:")
print(f"  along the x-axis: a = {1.0:.6f}")
print(f"  along the y-axis: b = {1.0 / np.sqrt(2.0):.6f}")
print(f"  along the z-axis: c = {1.0 / np.sqrt(3.0):.6f}")

sample_count = 4_000_000
sample_x = random_generator.uniform(-1.0, 1.0, sample_count)
sample_y = random_generator.uniform(-1.0, 1.0, sample_count)
sample_z = random_generator.uniform(-1.0, 1.0, sample_count)

quadratic_form = sample_x**2 + 2.0 * sample_y**2 + 3.0 * sample_z**2
inside = quadratic_form <= 1.0
values = integrand(sample_x, sample_y, sample_z)

disagreement = int(np.count_nonzero((values > 0.0) != inside))
print()
print(f"points tested inside and outside the ellipsoid: {sample_count}")
print(f"points where the sign of g contradicts the ellipsoid test: {disagreement}")

box_volume = 2.0 * 2.0 * 2.0
volume_estimate = box_volume * float(np.mean(inside))
integral_estimate = box_volume * float(np.mean(values * inside))

volume_standard_error = box_volume * float(np.std(inside)) / np.sqrt(sample_count)
integral_standard_error = box_volume * float(np.std(values * inside)) / np.sqrt(sample_count)

volume_exact = 4.0 * np.pi / (3.0 * np.sqrt(6.0))
integral_exact = 4.0 * np.pi * np.sqrt(6.0) / 45.0

print()
print(f"Monte Carlo volume:  {volume_estimate:.5f}  (exact 4*pi/(3*sqrt(6)) = {volume_exact:.5f})")
print(f"volume standard error: {volume_standard_error:.5f}")
print(f"Monte Carlo integral:{integral_estimate:.5f}  (exact 4*pi*sqrt(6)/45 = {integral_exact:.5f})")
print(f"integral standard error: {integral_standard_error:.5f}")
print(f"integral deviation in standard errors: {(integral_estimate - integral_exact) / integral_standard_error:+.2f}")
print(f"Monte Carlo average g over the ellipsoid: {integral_estimate / volume_estimate:.5f}  (exact 2/5)")
