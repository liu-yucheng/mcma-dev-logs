import sympy as sp
import numpy as np

x, y, z = sp.symbols('x y z', real=True)

# Given order: 0<=y<=2, 0<=z<=2-y, 0<=x<=4-y^2  ->  dx dz dy
I_given = sp.integrate(sp.integrate(sp.integrate(1, (x, 0, 4 - y**2)), (z, 0, 2 - y)), (y, 0, 2))
print("given order (dx dz dy):", I_given)

# Alternative order 1: dx dy dz  (x: 0..4-y^2, y: 0..2-z, z: 0..2)
alt1 = sp.integrate(sp.integrate(sp.integrate(1, (x, 0, 4 - y**2)), (y, 0, 2 - z)), (z, 0, 2))
print("order dx dy dz:", alt1)

# Alternative order 2: dz dx dy  (z: 0..2-y, x: 0..4-y^2, y: 0..2)
alt2 = sp.integrate(sp.integrate(sp.integrate(1, (z, 0, 2 - y)), (x, 0, 4 - y**2)), (y, 0, 2))
print("order dz dx dy:", alt2)

# Monte Carlo sanity check in box y in [0,2], z in [0,2], x in [0,4]
rng = np.random.default_rng(7)
N = 4_000_000
ys = 2.0*rng.random(N); zs = 2.0*rng.random(N); xs = 4.0*rng.random(N)
mask = (ys + zs <= 2) & (xs <= 4 - ys**2)
box = 2.0*2.0*4.0
print("Monte Carlo volume:", float(mask.mean())*box)
print("20/3 =", sp.Rational(20,3), "=", float(sp.Rational(20,3)))
assert I_given == sp.Rational(20,3) and alt1 == sp.Rational(20,3) and alt2 == sp.Rational(20,3)
print("OK: all orders agree with 20/3")
