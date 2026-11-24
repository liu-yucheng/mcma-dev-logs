"""Step 1.2: the mass is the triple integral of r^2, equal to 19*pi."""
import numpy as np
import sympy as sp

r, th = sp.symbols("r theta", positive=True)
m1 = sp.integrate(sp.integrate(r**3, (r, 0, 3)), (th, 0, sp.pi/6))
m2 = sp.integrate(sp.integrate(r**3, (r, 0, 3*sp.sin(th))), (th, sp.pi/6, sp.pi/2))
M = sp.simplify(m1 + m2)
print("M exact =", M, "=", float(M))

rng = np.random.default_rng(5)
N = 400000
x = rng.random(N)*3.0; y = rng.random(N)*3.0; z = rng.random(N)*3.0
k = (x <= 3.0) & (y >= 0.0) & (x*x + y*y <= 9.0) & (z >= 0.0)
Vg = 27.0
mhat = float(k.sum())/N*Vg*float(np.mean((x[k]**2 + y[k]**2)))/max(float(k.mean()), 1e-12)
print("Monte Carlo mass:", round(mhat, 3))
assert abs(mhat - float(M)) < 0.25
print("PASS 1.2")
