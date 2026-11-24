"""Step 1.2: the cylinder part has volume 90*pi, checked by a grid count."""

import numpy as np
import sympy as sp

r, z, th = sp.symbols("r z theta", positive=True)
exact = sp.integrate(sp.integrate(sp.integrate(r, (z, 0, 10)), (r, 0, 3)), (th, 0, 2 * sp.pi))

h = 0.05
xs = np.arange(-3.0, 3.0 + h, h)
ys = np.arange(-3.0, 3.0 + h, h)
zs = np.arange(0.0, 10.0 + h, h)
X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
inside = (X**2 + Y**2 <= 9) & (Z < 10.0)
grid_vol = float(inside.sum()) * h**3
for zz in (2.0, 5.0, 8.0):
    k = int(round(zz / h))
    rad = np.hypot(X[:, :, k], Y[:, :, k])
    mask = inside[:, :, k]
    print("z = %g: boundary radius = %.4f, count = %d" % (zz, float(rad[mask].max()), int(mask.sum())))
print("exact cylinder volume:", exact, "=", round(float(exact), 4))
print("grid count volume:", round(grid_vol, 4), "count:", int(inside.sum()))
assert abs(grid_vol - float(exact)) < 1.0
print("PASS 1.2")
