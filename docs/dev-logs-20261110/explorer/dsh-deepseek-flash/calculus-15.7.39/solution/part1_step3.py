"""Confirm the mass, the moments, and the centroid numerically.

The inner z-integral is exact because the top surface is a plane, so each
quantity is a double integral over D. mpmath evaluates those double integrals,
and a Monte Carlo sample of the solid gives an independent geometric check.
"""

import numpy as np
from mpmath import mp, mpf, quad, sqrt

mp.dps = 20


def height(x, y):
    """Return the roof height z = 1 + x + y."""
    return 1 + x + y


mass = 2 * quad(lambda x: quad(lambda y: height(x, y), [0, sqrt(x)]), [0, 1])
moment_yz = 2 * quad(lambda x: quad(lambda y: x * height(x, y), [0, sqrt(x)]), [0, 1])
moment_xz = 2 * quad(lambda x: quad(lambda y: y * height(x, y), [0, sqrt(x)]), [0, 1])
moment_xy = 2 * quad(
    lambda x: quad(lambda y: height(x, y) ** 2 / 2, [0, sqrt(x)]), [0, 1]
)
base_area = quad(lambda x: sqrt(x), [0, 1])

print(f"base area of D: {mp.nstr(base_area, 12)}")
print(f"mass from quadrature: {mp.nstr(mass, 12)}")
print(f"M_yz from quadrature: {mp.nstr(moment_yz, 12)}")
print(f"M_xz from quadrature: {mp.nstr(moment_xz, 12)}")
print(f"M_xy from quadrature: {mp.nstr(moment_xy, 12)}")
print(f"x-bar: {mp.nstr(moment_yz / mass, 12)}")
print(f"y-bar: {mp.nstr(moment_xz / mass, 12)}")
print(f"z-bar: {mp.nstr(moment_xy / mass, 12)}")
print(f"mass minus 79/30: {mp.nstr(mass - mpf(79) / 30, 3)}")
print(f"M_yz minus 179/105: {mp.nstr(moment_yz - mpf(179) / 105, 3)}")
print(f"M_xz minus 11/10: {mp.nstr(moment_xz - mpf(11) / 10, 3)}")
print(f"M_xy minus 571/210: {mp.nstr(moment_xy - mpf(571) / 210, 3)}")

# Monte Carlo over the box 0 <= x <= 1, 0 <= y <= 1, 0 <= z <= 3.
generator = np.random.default_rng(20261109)
sample_count = 4000000
sample_x = generator.uniform(0.0, 1.0, sample_count)
sample_y = generator.uniform(0.0, 1.0, sample_count)
sample_z = generator.uniform(0.0, 3.0, sample_count)
inside = (sample_y**2 <= sample_x) & (sample_z <= 1.0 + sample_x + sample_y)
accepted = int(np.count_nonzero(inside))
box_volume = 3.0
volume_estimate = box_volume * accepted / sample_count
mass_estimate = 2.0 * volume_estimate
print(f"accepted Monte Carlo points: {accepted}")
print(f"volume estimate: {volume_estimate:.5f}")
print(f"mass estimate: {mass_estimate:.5f}")
for name, values, exact in [
    ("x-bar", sample_x[inside], float(moment_yz / mass)),
    ("y-bar", sample_y[inside], float(moment_xz / mass)),
    ("z-bar", sample_z[inside], float(moment_xy / mass)),
]:
    estimate = float(np.mean(values))
    standard_error = float(np.std(values)) / np.sqrt(accepted)
    print(f"{name} estimate: {estimate:.5f} plus or minus {standard_error:.5f}, exact {exact:.5f}")
