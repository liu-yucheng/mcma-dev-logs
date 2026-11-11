"""Check the results of Exercise 15.7.50 with quadrature and random sampling.

The solid is E = {(x, y, z) : 0 <= y <= 3, 0 <= x <= y/3, 0 <= z <= sqrt(9 - y**2)}
with density rho = x**2 + y**2. Quadrature and Monte Carlo sampling are independent
of the symbolic derivation in part1_step1.py.
"""

import mpmath as mp
import numpy as np


mp.mp.dps = 16


def integrate_over_solid(function):
    """Return the triple integral of function(x, y, z) over E by nested quadrature."""
    over_x = lambda y_value, z_value: mp.quad(lambda x_value: function(x_value, y_value, z_value),
                                              [0, y_value / 3])
    over_z = lambda y_value: mp.quad(lambda z_value: over_x(y_value, z_value),
                                     [0, mp.sqrt(9 - y_value**2)])
    return mp.quad(over_z, [0, 3])


density = lambda x_value, y_value, z_value: x_value**2 + y_value**2
mass = integrate_over_solid(density)
moment_yz = integrate_over_solid(lambda x_value, y_value, z_value: x_value * density(x_value, y_value, z_value))
moment_xz = integrate_over_solid(lambda x_value, y_value, z_value: y_value * density(x_value, y_value, z_value))
moment_xy = integrate_over_solid(lambda x_value, y_value, z_value: z_value * density(x_value, y_value, z_value))
inertia = integrate_over_solid(lambda x_value, y_value, z_value: (x_value**2 + y_value**2)
                               * density(x_value, y_value, z_value))

exact_mass = mp.mpf(56) / 5
exact_moment_yz = 171 * mp.pi / 128
exact_moment_xz = 63 * mp.pi / 8
exact_moment_xy = mp.mpf(21) / 2
exact_inertia = mp.mpf(10464) / 175

print("nested quadrature against the exact values:")
for label, computed, exact in [
    ("mass M", mass, exact_mass),
    ("M_yz", moment_yz, exact_moment_yz),
    ("M_xz", moment_xz, exact_moment_xz),
    ("M_xy", moment_xy, exact_moment_xy),
    ("I_z", inertia, exact_inertia),
]:
    print(f"  {label:8s} quadrature {mp.nstr(computed, 12):>16s}"
          f"   exact {mp.nstr(exact, 12):>16s}   gap {mp.nstr(computed - exact, 3):>10s}")

print()
print("center of mass from the quadrature:")
print(f"  x bar = {mp.nstr(moment_yz / mass, 10)}")
print(f"  y bar = {mp.nstr(moment_xz / mass, 10)}")
print(f"  z bar = {mp.nstr(moment_xy / mass, 10)}")

print()
random_generator = np.random.default_rng(20261110)
sample_count = 4000000
sample_x = random_generator.uniform(0.0, 1.0, sample_count)
sample_y = random_generator.uniform(0.0, 3.0, sample_count)
sample_z = random_generator.uniform(0.0, 3.0, sample_count)
box_volume = 9.0
inside = (sample_x <= sample_y / 3.0) & (sample_y**2 + sample_z**2 <= 9.0)
weight = (sample_x**2 + sample_y**2) * inside
estimate = box_volume * float(np.mean(weight))
standard_error = box_volume * float(np.std(weight)) / np.sqrt(sample_count)
print(f"Monte Carlo estimate of the mass: {estimate:.5f}")
print(f"exact value 56/5:                 {float(exact_mass):.5f}")
print(f"estimated standard error:         {standard_error:.5f}")
print(f"deviation in standard errors:     {(estimate - float(exact_mass)) / standard_error:+.2f}")

inertia_weight = (sample_x**2 + sample_y**2) * weight
inertia_estimate = box_volume * float(np.mean(inertia_weight))
inertia_error = box_volume * float(np.std(inertia_weight)) / np.sqrt(sample_count)
print(f"Monte Carlo estimate of I_z:      {inertia_estimate:.5f}")
print(f"exact value 10464/175:            {float(exact_inertia):.5f}")
print(f"deviation in standard errors:     {(inertia_estimate - float(exact_inertia)) / inertia_error:+.2f}")
