"""Estimate the moment of inertia of a solid cone by quadrature and by sampling.

The solid is the cone sqrt(x^2 + y^2) <= z <= h with constant density k.  The z-axis
moment is I_z = k * integral of (x^2 + y^2) over the cone.  Method 1 integrates the
reduced one-dimensional form in cylindrical coordinates with mpmath.  Method 2 samples
points uniformly in the cylinder 0 <= r <= h, 0 <= z <= h and keeps the points that lie
under the cone surface.

Run:  python part1_step1.py
"""

from __future__ import annotations

import numpy as np
from mpmath import mp, quad

H = 1.0
K = 1.0


def moment_by_quadrature(h: float, k: float) -> float:
    """Integrate the shell form 2*pi*k*r^3*(h - r) over 0 <= r <= h."""
    mp.dps = 20
    integrand = lambda r: 2.0 * mp.pi * k * r**3 * (h - r)
    return float(quad(integrand, [0.0, h]))


def moment_by_sampling(h: float, k: float, count: int, seed: int) -> tuple[float, float]:
    """Sample the bounding cylinder and average r^2 over the points inside the cone.

    Args:
        h: Height of the cone; the base radius equals h.
        k: Constant density.
        count: Number of uniform samples in the cylinder.
        seed: Seed of the random generator.

    Returns:
        The estimate of I_z and its standard error.
    """
    rng = np.random.default_rng(seed)
    radius = h * np.sqrt(rng.random(count))
    angle = 2.0 * np.pi * rng.random(count)
    height = h * rng.random(count)
    inside = height >= radius
    values = np.where(inside, k * radius**2, 0.0)
    cylinder_volume = np.pi * h**3
    estimate = cylinder_volume * values.mean()
    error = cylinder_volume * values.std(ddof=1) / np.sqrt(values.size)
    return float(estimate), float(error)


def main() -> None:
    exact = np.pi * K * H**5 / 10.0
    print(f"cone height h = {H}, density k = {K}")
    print(f"quadrature I_z = {moment_by_quadrature(H, K):.15f}")
    print(f"closed form I_z = {exact:.15f}")
    estimate, error = moment_by_sampling(H, K, count=4_000_000, seed=20261109)
    print(f"sampling I_z = {estimate:.6f} with standard error {error:.6f}")
    print(f"deviation = {(estimate - exact) / error:+.2f} standard errors")
    print(f"acceptance fraction (cone volume / cylinder volume) = {1.0 / 3.0:.6f}")
    print(f"base radius equals h = {H}")


if __name__ == "__main__":
    main()
