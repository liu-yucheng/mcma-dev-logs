"""Part 1, Step 1 - Geometry of E and verification of all six iterated forms.

E is bounded by x = 2, y = 2, z = 0 and the slanted plane x + y - 2z = 2.
E is the side x + y - 2z >= 2 of the slanted plane (the origin side has
x + y - 2z < 2 and also z >= 0 would force the empty/wrong side; check the
test point (2, 2, 0.5): 4 - 1 = 3 >= 2 and 0 <= 0.5 <= (4-2)/2 = 1, inside).
Vertices: (2,0,0), (0,2,0), (2,2,0), (2,2,1). Volume = |det|/6 = 2/3.
All six orderings of dz dy dx etc. must give the same volume for f = 1.
"""
import numpy as np
import sympy as sp

x, y, z, f = sp.symbols("x y z f", real=True)

# --- Vertex check: pairwise plane intersections -------------------------
verts = {
    "A (x=2, z=0, slant)": (2, 0, 0),
    "B (y=2, z=0, slant)": (0, 2, 0),
    "C (x=2, y=2, z=0)":   (2, 2, 0),
    "D (x=2, y=2, slant)": (2, 2, 1),
}
for name, (px, py, pz) in verts.items():
    assert abs(px + py - 2*pz - 2) < 1e-12 or "slant" not in name, name
    assert 0 <= pz, name
print("vertices ok:", verts)

# --- Exact tetrahedron volume -------------------------------------------
A = np.array([2, 0, 0], float); B = np.array([0, 2, 0], float)
C = np.array([2, 2, 0], float); D = np.array([2, 2, 1], float)
V_tetra = abs(np.linalg.det(np.array([B - A, C - A, D - A]))) / 6
print("tetrahedron volume =", V_tetra)

# --- Six orderings, f = 1, exact with sympy ------------------------------
six = {
    # 1: dz dy dx
    1: sp.integrate(sp.integrate(sp.integrate(1, (z, 0, (x + y - 2) / 2)),
                                 (y, 2 - x, 2)), (x, 0, 2)),
    # 2: dz dx dy
    2: sp.integrate(sp.integrate(sp.integrate(1, (z, 0, (x + y - 2) / 2)),
                                 (x, 2 - y, 2)), (y, 0, 2)),
    # 3: dy dz dx
    3: sp.integrate(sp.integrate(sp.integrate(1, (y, 2 + 2*z - x, 2)),
                                 (z, 0, x / 2)), (x, 0, 2)),
    # 4: dy dx dz
    4: sp.integrate(sp.integrate(sp.integrate(1, (y, 2 + 2*z - x, 2)),
                                 (x, 2*z, 2)), (z, 0, 1)),
    # 5: dx dy dz
    5: sp.integrate(sp.integrate(sp.integrate(1, (x, 2 + 2*z - y, 2)),
                                 (y, 2*z, 2)), (z, 0, 1)),
    # 6: dx dz dy
    6: sp.integrate(sp.integrate(sp.integrate(1, (x, 2 + 2*z - y, 2)),
                                 (z, 0, y / 2)), (y, 0, 2)),
}
ok = True
for k, val in six.items():
    print(f"ordering {k}: vol = {val}")
    if val != sp.Rational(2, 3):
        ok = False
print("all six equal 2/3:", ok)

# --- Cross-check with a generic integrand f = x^2 + y^2 + z^2 -----------
g = x**2 + y**2 + z**2
sixg = {
    1: sp.integrate(sp.integrate(sp.integrate(g, (z, 0, (x + y - 2) / 2)),
                                 (y, 2 - x, 2)), (x, 0, 2)),
    2: sp.integrate(sp.integrate(sp.integrate(g, (z, 0, (x + y - 2) / 2)),
                                 (x, 2 - y, 2)), (y, 0, 2)),
    3: sp.integrate(sp.integrate(sp.integrate(g, (y, 2 + 2*z - x, 2)),
                                 (z, 0, x / 2)), (x, 0, 2)),
    4: sp.integrate(sp.integrate(sp.integrate(g, (y, 2 + 2*z - x, 2)),
                                 (x, 2*z, 2)), (z, 0, 1)),
    5: sp.integrate(sp.integrate(sp.integrate(g, (x, 2 + 2*z - y, 2)),
                                 (y, 2*z, 2)), (z, 0, 1)),
    6: sp.integrate(sp.integrate(sp.integrate(g, (x, 2 + 2*z - y, 2)),
                                 (z, 0, y / 2)), (y, 0, 2)),
}
vals = sorted(sp.simplify(v) for v in sixg.values())
print("f = x^2+y^2+z^2, all six:", vals, "identical:", len(set(vals)) == 1)

# --- Monte Carlo sanity check of the region description ------------------
rng = np.random.default_rng(42)
N = 400_000
xs = rng.uniform(0, 2, N); ys = rng.uniform(0, 2, N); zs = rng.uniform(0, 1, N)
inside = (xs + ys - 2*zs >= 2) & (xs <= 2) & (ys <= 2) & (zs >= 0)
vol_mc = inside.sum() / N * 4.0  # box 2*2*1
print("Monte Carlo volume:", round(vol_mc, 5), "(expect 0.66667)")
