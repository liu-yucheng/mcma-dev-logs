"""The slice of the wedge at fixed x is 0<=y<=x and 0<=z<=sqrt(1-y^2); endpoints print."""
import sympy as sp
import numpy as np

x, y = sp.symbols("x y", nonnegative=True)
A = sp.simplify(sp.integrate(sp.sqrt(1 - y**2), (y, 0, x)))
assert sp.simplify(A - (x / 2 * sp.sqrt(1 - x**2) + sp.asin(x) / 2)) == 0, "antiderivative"

def corners(xv):
    pts = [(0.0, 0.0)]
    if xv > 0.0:
        pts.append((xv, 0.0))
        if xv < 1.0:
            pts.append((xv, round((1 - xv * xv) ** 0.5, 4)))
    pts.append((0.0, 1.0))
    return pts

for xv in (0.0, 0.5, 1.0):
    print(f"slice at x = {xv}: corners {corners(xv)}")

n = 500
ys = np.linspace(0, 0.5, n + 1)[1:]
zs = np.linspace(0, 1.0, n + 1)[1:]
mask = zs[None, :] <= np.sqrt(1 - ys[:, None] ** 2)
hy, hz = 0.5 / n, 1.0 / n
grid_area = float(mask.sum() * hy * hz)
exact_area = float(A.subs(x, sp.Rational(1, 2)))
print(f"grid area {grid_area:.6f} vs exact slice area {exact_area:.6f}")
assert abs(grid_area - exact_area) < 20 * hz + 1e-9, "grid tolerance"
print("PASS 1.1")
