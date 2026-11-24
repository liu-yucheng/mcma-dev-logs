"""Step 1.1: the volume of E is 9*pi/2 in cylindrical coordinates."""
import numpy as np
import sympy as sp

r, th = sp.symbols("r theta", positive=True)
I1 = sp.integrate(sp.integrate(r, (r, 0, 3)), (th, 0, sp.pi/6))
I2 = sp.integrate(sp.integrate(r, (r, 0, 3*sp.sin(th))), (th, sp.pi/6, sp.pi/2))
V = sp.simplify(I1 + I2)
print("V exact =", V, "=", float(V))

h = 0.01
xs = np.arange(-0.005, 3.005, h); ys = np.arange(-0.005, 3.005, h)
X, Y = np.meshgrid(xs, ys)
m = (X <= 3.0 + 1e-9) & (Y >= -1e-9) & (X*X + Y*Y <= 9.0 + 1e-9)
print("grid volume:", round(float(m.sum())*h*h, 4))
assert abs(float(m.sum())*h*h - float(V)) < 0.05
print("PASS 1.1")
