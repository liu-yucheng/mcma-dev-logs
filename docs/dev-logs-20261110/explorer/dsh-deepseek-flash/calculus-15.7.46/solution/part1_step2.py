"""Derive the z-axis moment of inertia of a solid cone in SymPy.

The cone is sqrt(x^2 + y^2) <= z <= h with constant density k.  In cylindrical
coordinates the moment is I_z = k * integral of r^2 * r over the cone, so the volume
element supplies one factor of r and the integrand becomes k * r^3.

Run:  python part1_step2.py
"""

from __future__ import annotations

import sympy as sp

r, z, theta = sp.symbols("r z theta", positive=True)
h, k = sp.symbols("h k", positive=True)

height_of_shell = h - r
inner = sp.integrate(k * r**3, (z, r, h))
print(f"integral over z, from r to h: {sp.simplify(inner)}")

radial = sp.integrate(sp.simplify(inner), (r, 0, h))
print(f"integral over r, from 0 to h: {sp.simplify(radial)}")

moment = sp.integrate(radial, (theta, 0, 2 * sp.pi))
moment = sp.simplify(moment)
print(f"integral over theta, from 0 to 2*pi: {moment}")

mass = sp.integrate(sp.integrate(sp.integrate(k * r, (z, r, h)), (r, 0, h)), (theta, 0, 2 * sp.pi))
mass = sp.simplify(mass)
print(f"mass of the cone: {mass}")

ratio = sp.simplify(moment / mass)
print(f"I_z / m = {ratio}")

assert sp.simplify(moment - sp.pi * k * h**5 / 10) == 0
assert sp.simplify(ratio - 3 * h**2 / 10) == 0
print("assertions passed")
