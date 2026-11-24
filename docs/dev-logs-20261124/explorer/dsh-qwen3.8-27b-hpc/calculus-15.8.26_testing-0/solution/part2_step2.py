"""Step 2.2: the section boundary at three heights is min(a cos theta, sqrt(a^2 - z^2))."""

import numpy as np
import sympy as sp

a = 1.0
print("corners at theta endpoints (a = 1):")
for tv in [-np.pi / 2, 0.0, np.pi / 2]:
    print(f"  theta = {tv:+.4f}: r_cyl = {a * np.cos(tv):.4f}")
fine = np.linspace(-np.pi / 2, np.pi / 2, 20001)
worst = 0.0
rng = np.random.default_rng(23)
for z in [0.0, 0.5, -0.5]:
    cap = float(np.sqrt(a**2 - z**2))
    rb = np.minimum(a * np.cos(np.linspace(-np.pi / 2, np.pi / 2, 7)), cap)
    print(f"z = {z:+.1f}: cap = {cap:.4f} r(theta) = {np.round(rb, 4).tolist()}")
    area = float(np.trapezoid(np.minimum(a * np.cos(fine), cap) ** 2 / 2.0, fine))
    m = 2_000_000
    tt = rng.uniform(-np.pi / 2, np.pi / 2, m)
    rr = rng.uniform(0.0, a, m)
    hit = (rr <= a * np.cos(tt)) & (rr**2 + z**2 <= a**2)
    num = float(np.pi * a * np.mean(rr * hit))
    worst = max(worst, abs(num - area))
exact0 = float(sp.pi / 4)
trap0 = float(np.trapezoid((a * np.cos(fine)) ** 2 / 2.0, fine))
assert abs(trap0 - exact0) < 1e-6
assert worst < 5e-3
print("max section area error:", round(worst, 5))
print("PASS 2.2")
