"""Step 1.1: the volume of the paraboloid cap is pi/2."""
import numpy as np
import sympy as sp

r = sp.symbols("r", positive=True)
V = sp.simplify(sp.integrate(r*(1 - r**2), (r, 0, 1))*2*sp.pi)
print("V exact =", V, "=", float(V))

h = 0.01
xs = np.arange(-1.005, 1.005, h); ys = np.arange(-1.005, 1.005, h)
X, Y = np.meshgrid(xs, ys)
disk = X*X + Y*Y <= 1.0 + 1e-9
Vg = h*h*float(np.sum(1 - (X[disk]**2 + Y[disk]**2)))
print("grid volume:", round(Vg, 4))
assert abs(Vg - float(V)) < 0.03
print("PASS 1.1")
