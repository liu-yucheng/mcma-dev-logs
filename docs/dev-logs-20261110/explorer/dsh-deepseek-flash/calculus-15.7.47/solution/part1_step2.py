"""Check the setup integrals by uniform sampling of the enclosing box.

The box is -1 <= x <= 1, 0 <= y <= 1, 0 <= z <= 1.  A sample point belongs to the solid
when y >= x^2 and z <= 1 - y.  The box volume is 2, so each mean is multiplied by 2.

Run:  python part1_step2.py
"""

from __future__ import annotations

import numpy as np

COUNT = 4_000_000
SEED = 20261109


def main() -> None:
    rng = np.random.default_rng(SEED)
    x = rng.uniform(-1.0, 1.0, COUNT)
    y = rng.uniform(0.0, 1.0, COUNT)
    z = rng.uniform(0.0, 1.0, COUNT)
    inside = (y >= x * x) & (z <= 1.0 - y)
    density = np.sqrt(x * x + y * y)
    box_volume = 2.0

    mass = box_volume * np.mean(np.where(inside, density, 0.0))
    moment_xz = box_volume * np.mean(np.where(inside, y * density, 0.0))
    moment_xy = box_volume * np.mean(np.where(inside, z * density, 0.0))
    inertia = box_volume * np.mean(np.where(inside, (x * x + y * y) * density, 0.0))

    print(f"accepted fraction = {inside.mean():.6f}")
    print(f"mass     m    = {mass:.6f}")
    print(f"moment   M_xz = {moment_xz:.6f}")
    print(f"moment   M_xy = {moment_xy:.6f}")
    print(f"inertia  I_z  = {inertia:.6f}")
    print(f"y bar         = {moment_xz / mass:.6f}")
    print(f"z bar         = {moment_xy / mass:.6f}")
    print(f"volume by sampling = {box_volume * inside.mean():.6f}")
    print(f"exact volume = 8/15 = {8.0 / 15.0:.6f}")


if __name__ == "__main__":
    main()
