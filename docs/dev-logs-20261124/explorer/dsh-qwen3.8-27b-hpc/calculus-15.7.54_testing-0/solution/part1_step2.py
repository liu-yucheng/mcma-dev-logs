"""Step 1.2: the integral of f equals 4*pi/3."""
import numpy as np
import sympy as sp

r = sp.symbols("r", positive=True)
N4 = sp.simplify(sp.integrate(r**3*(1 - r**2)**2, (r, 0, 1))*2*sp.pi)
print("N exact =", N4, "=", float(N4))

h = 0.01
xs = np.arange(-1.005, 1.005, h); ys = np.arange(-1.005, 1.005, h)
X, Y = np.meshgrid(xs, ys)
disk = X*X + Y*Y <= 1.0 + 1e-9
f = X*X + Y*Y
Ng = h*h*0.5*float(np.sum(f[disk]**2))
print("grid N:", round(Ng, 4))
assert abs(Ng - float(N4)) < 0.05
print("PASS 1.2")
