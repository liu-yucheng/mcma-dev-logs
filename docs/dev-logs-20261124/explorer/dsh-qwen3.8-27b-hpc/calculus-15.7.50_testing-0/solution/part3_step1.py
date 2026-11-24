"""Step 3.1: the moment of inertia about the z-axis is 2430*pi/7."""
import numpy as np
import sympy as sp

r, th = sp.symbols("r theta", positive=True)
i1 = sp.integrate(sp.integrate(r**5, (r, 0, 3)), (th, 0, sp.pi/6))
i2 = sp.integrate(sp.integrate(r**5, (r, 0, 3*sp.sin(th))), (th, sp.pi/6, sp.pi/2))
Iz = sp.simplify(i1 + i2)
print("I_z exact =", Iz, "=", round(float(Iz), 3))

rng = np.random.default_rng(5)
N = 400000
x = rng.random(N)*3.0; y = rng.random(N)*3.0; z = rng.random(N)*3.0
k = (x <= 3.0) & (y >= 0.0) & (x*x + y*y <= 9.0) & (z >= 0.0)
Vg = 27.0
w = x[k]**2 + y[k]**2
iz = float(k.sum())/N*Vg*float(np.mean(w*w))/max(float(k.mean()), 1e-12)
print("Monte Carlo I_z:", round(iz, 2))
assert abs(iz - float(Iz)) < 2.5
print("PASS 3.1")
