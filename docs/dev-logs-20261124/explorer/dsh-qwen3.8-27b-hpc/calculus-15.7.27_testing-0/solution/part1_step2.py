"""Step 2: the exact volume from the given iterated integral equals 2/3, and the swapped section order agrees."""
import sympy as sp

y, z, x, t = sp.symbols("x y z t")
inner = sp.integrate(sp.Integer(1), (y, 0, 2 - 2 * z))
print("dy step:", inner)
mid = sp.integrate(inner, (z, 0, 1 - x))
print("dz step:", sp.simplify(mid))
V = sp.integrate(mid, (x, 0, 1))
print("exact V =", V)
A = 2 * (1 - t) ** 2  # cross section area at height t (independent order)
Vswap = sp.integrate(A, (t, 0, 1))
print("section V =", Vswap)
assert V == Vswap == sp.Rational(2, 3)
import numpy as np
tt = np.linspace(0, 1, 200001)
trap = float(np.trapz(2 * (1 - tt) ** 2, tt))
print("trapz =", trap)
assert abs(float(V) - trap) < 1e-9
print("PASS 1.2")
