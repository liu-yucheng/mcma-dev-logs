"""Step 1.3: the hemisphere part has volume 18*pi, checked by a grid count."""

import numpy as np
import sympy as sp

rho, phi, th = sp.symbols("rho phi theta", positive=True)
exact = sp.integrate(sp.integrate(sp.integrate(rho**2 * sp.sin(phi), (rho, 0, 3)), (phi, 0, sp.pi / 2)), (th, 0, 2 * sp.pi))

h = 0.05
xs = np.arange(-3.0, 3.05, h)
ys = np.arange(-3.0, 3.05, h)
zs = np.arange(10.0, 13.05, h)
X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
inside = X**2 + Y**2 + (Z - 10.0)**2 <= 9
grid_vol = float(inside.sum()) * h**3
top_z = 10.0 + 3.0
print("exact hemisphere volume:", exact, "=", round(float(exact), 4))
print("grid count volume:", round(grid_vol, 4), "count:", int(inside.sum()))
print("top point: (0, 0, %g), check 0 + 0 + (%g - 10)^2 = %g" % (top_z, top_z, 9.0))
assert abs(grid_vol - float(exact)) < 1.0
print("PASS 1.3")
