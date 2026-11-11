"""Check the results of Exercise 15.7.49 with quadrature and random sampling.

The solid is E = {(x, y, z) : 0 <= y <= 1, 0 <= x <= sqrt(1 - y**2), 0 <= z <= y}
with density rho = 1 + x + y + z. Quadrature and Monte Carlo sampling are
independent of the symbolic derivation in part1_step1.py.
"""

import mpmath as mp
import numpy as np


mp.mp.dps = 16


def integrate_over_solid(function):
    """Return the triple integral of function(x, y, z) over E by nested quadrature."""
    over_z = lambda x_value, y_value: mp.quad(lambda z_value: function(x_value, y_value, z_value),
                                              [0, y_value])
    over_y = lambda y_value: mp.quad(lambda x_value: over_z(x_value, y_value),
                                     [0, mp.sqrt(1 - y_value**2)])
    return mp.quad(over_y, [0, 1])


density = lambda x_value, y_value, z_value: 1 + x_value + y_value + z_value
mass = integrate_over_solid(density)
moment_yz = integrate_over_solid(lambda x_value, y_value, z_value: x_value * density(x_value, y_value, z_value))
moment_xz = integrate_over_solid(lambda x_value, y_value, z_value: y_value * density(x_value, y_value, z_value))
moment_xy = integrate_over_solid(lambda x_value, y_value, z_value: z_value * density(x_value, y_value, z_value))
inertia = integrate_over_solid(lambda x_value, y_value, z_value: (x_value**2 + y_value**2)
                               * density(x_value, y_value, z_value))

exact_mass = mp.mpf(11) / 24 + 3 * mp.pi / 32
exact_moment_yz = mp.mpf(7) / 24
exact_moment_xz = mp.pi / 16 + mp.mpf(4) / 15
exact_moment_xy = mp.pi / 32 + mp.mpf(13) / 90
exact_inertia = mp.mpf(17) / 60 + mp.pi / 16

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
sample_y = random_generator.uniform(0.0, 1.0, sample_count)
sample_z = random_generator.uniform(0.0, 1.0, sample_count)
inside = (sample_x**2 + sample_y**2 <= 1.0) & (sample_z <= sample_y)
box_volume = 1.0
weight = (1.0 + sample_x + sample_y + sample_z) * inside
estimate = box_volume * float(np.mean(weight))
standard_error = box_volume * float(np.std(weight)) / np.sqrt(sample_count)
print(f"Monte Carlo estimate of the mass: {estimate:.5f}")
print(f"exact value 11/24 + 3*pi/32:      {float(exact_mass):.5f}")
print(f"estimated standard error:         {standard_error:.5f}")
print(f"deviation in standard errors:     {(estimate - float(exact_mass)) / standard_error:+.2f}")

inertia_weight = (sample_x**2 + sample_y**2) * weight
inertia_estimate = box_volume * float(np.mean(inertia_weight))
inertia_error = box_volume * float(np.std(inertia_weight)) / np.sqrt(sample_count)
print(f"Monte Carlo estimate of I_z:      {inertia_estimate:.5f}")
print(f"exact value 17/60 + pi/16:        {float(exact_inertia):.5f}")
print(f"deviation in standard errors:     {(inertia_estimate - float(exact_inertia)) / inertia_error:+.2f}")
