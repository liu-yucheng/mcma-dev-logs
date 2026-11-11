"""Check the cone moment at a second size and density with mpmath.

The closed form I_z = pi * k * h^5 / 10 scales with h^5 and k.  This script tests that
scaling at h = 2 and k = 3 and compares the result with the mass form (3/10) * m * h^2.

Run:  python part1_step3.py
"""

from __future__ import annotations

from mpmath import mp, mpf, pi, quad

mp.dps = 25
H = mpf(2)
K = mpf(3)


def moment(h: mpf, k: mpf) -> mpf:
    """Return the z-axis moment of inertia by one-dimensional quadrature."""
    return quad(lambda r: 2 * pi * k * r**3 * (h - r), [0, h])


def mass(h: mpf, k: mpf) -> mpf:
    """Return the mass of the cone, one third of the enclosing cylinder."""
    return pi * k * h**3 / 3


closed = pi * K * H**5 / 10
print(f"h = {H}, k = {K}")
print(f"quadrature I_z = {moment(H, K)}")
print(f"closed form I_z = {closed}")
print(f"mass m = {mass(H, K)}")
print(f"(3/10) * m * h^2 = {3 * mass(H, K) * H**2 / 10}")
print(f"relative difference = {abs(moment(H, K) - closed) / closed}")
