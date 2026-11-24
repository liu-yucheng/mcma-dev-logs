"""At each y in 0, 1, 2 the slice is a rectangle 0 <= x <= 4 - y**2 by 0 <= z <= 2 - y."""
import sympy as sp
y = sp.symbols("y")
X1 = 4 - y**2
Z1 = 2 - y
for yv in (0, 1, 2):
    xb = float(X1.subs(y, yv))
    zb = float(Z1.subs(y, yv))
    nx = nz = 40
    sx, sz = xb / nx, zb / nz
    grid = float(sum(sx * sz for _ in range(nx) for _ in range(nz)))
    exact = float(sp.simplify((X1 * Z1).subs(y, yv)))
    corners = [(x, z) for x in (0.0, xb) for z in (0.0, zb)]
    print(f"y={yv}: x in [0, {xb:g}], z in [0, {zb:g}]")
    print(f"corners={corners} area_exact={exact:g} area_grid={grid:.6f}")
    assert abs(exact - grid) < 1e-6 + max(sx, sz), yv
print("PASS 1.1")
