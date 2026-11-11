import sympy as sp
import numpy as np

x, y, z = sp.symbols('x y z', real=True)

# Given order: 0<=x<=1, 0<=z<=1-x, 0<=y<=2-2z  ->  dy dz dx
I_given = sp.integrate(sp.integrate(sp.integrate(1, (y, 0, 2 - 2*z)),
                                    (z, 0, 1 - x)), (x, 0, 1))
print("given order (dy dz dx):", I_given)

# Alternative order 1: dx dz dy  (x: 0..1-z, z: 0..1, y: 0..2, with z<=1-y/2? no:
#   for fixed (y,z) in D_yz = {0<=z<=1, 0<=y<=2-2z}: x runs 0..1-z)
alt1 = sp.integrate(sp.integrate(sp.integrate(1, (x, 0, 1 - z)),
                                 (z, 0, 1 - y/2)), (y, 0, 2))
print("order dx dz dy (y outer):", alt1)

# Alternative order 2: dy dx dz  (z: 0..1, x: 0..1-z, y: 0..2-2z)
alt2 = sp.integrate(sp.integrate(sp.integrate(1, (y, 0, 2 - 2*z)),
                                 (x, 0, 1 - z)), (z, 0, 1))
print("order dy dx dz:", alt2)

# Monte Carlo sanity check in box x in [0,1], z in [0,1], y in [0,2]
rng = np.random.default_rng(42)
N = 4_000_000
xs = rng.random(N); zs = rng.random(N); ys = 2.0*rng.random(N)
mask = (xs + zs <= 1) & (ys <= 2 - 2*zs)
box = 1.0*1.0*2.0
print("Monte Carlo volume:", float(mask.mean())*box)
assert I_given == sp.Rational(2,3) and alt1 == sp.Rational(2,3) and alt2 == sp.Rational(2,3)
print("OK: all orders agree with 2/3 =", float(sp.Rational(2,3)))
