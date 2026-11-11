"""Part (a) of problem 15.7.55: identify the maximizing region.

We maximize F(E) = int_E g dV with g(x,y,z) = 1 - x^2 - 2 y^2 - 3 z^2.
g >= 0 exactly on the ellipsoid E0 = {x^2 + 2 y^2 + 3 z^2 <= 1} and
g < 0 outside it. Adding any point where g > 0 raises F(E), removing
any point where g < 0 raises F(E); the maximum is attained at
E = E0. Verified here:
 1. sign of g at sample points (inside vs outside E0);
 2. Volume(E0) by the semi-axis formula AND by the affine change of
    variables (x, y, z) = (u, v/sqrt(2), w/sqrt(3)) (Jacobian 1/sqrt(6))
    mapping E0 to the unit ball, whose volume is computed exactly in
    spherical coordinates;
 3. Monte-Carlo estimate.
"""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
g = 1 - x**2 - 2*y**2 - 3*z**2

# 1) sign checks. A point (p) is inside E0 iff p^T diag(1,2,3) p <= 1.
samples = {
    "(0,0,0)":            (0, 0, 0),
    "(1/3, 1/3, 1/3)":    (sp.Rational(1, 3),)*3,
    "(1/2, 0, 0)":        (sp.Rational(1, 2), 0, 0),
    "(0, 1/2, 1/3)":      (0, sp.Rational(1, 2), sp.Rational(1, 3)),
    "(2,0,0)":            (2, 0, 0),
    "(0,1,0)":            (0, 1, 0),
    "(0,0,1)":            (0, 0, 1),
    "(1, 1, 1)":          (1, 1, 1),
}
for name, (px, py, pz) in samples.items():
    q = px**2 + 2*py**2 + 3*pz**2
    inside = (q <= 1)
    gv = g.subs({x: px, y: py, z: pz})
    print(f"g{name} = {gv}  (quad form {q}, inside: {inside})")
    assert (gv > 0) == inside, f"sign mismatch at {name}"

# 2) volume by semi-axis formula: a = 1, b = 1/sqrt(2), c = 1/sqrt(3)
a, b, c = 1, 1/sp.sqrt(2), 1/sp.sqrt(3)
V_formula = sp.simplify(4 * sp.pi * a * b * c / 3)
print("Volume (formula)  =", V_formula, "=", sp.N(V_formula, 12))

# volume via affine change of variables to the unit ball
u, v, w = sp.symbols("u v w", real=True)
J = sp.simplify(1 / (sp.sqrt(2) * sp.sqrt(3)))   # = 1/sqrt(6)
x_of, y_of, z_of = u, v / sp.sqrt(2), w / sp.sqrt(3)
lhs = sp.simplify(x_of**2 + 2*y_of**2 + 3*z_of**2)
print("x^2 + 2y^2 + 3z^2 in (u,v,w) =", lhs)
assert lhs == u**2 + v**2 + w**2

rho, phi, theta = sp.symbols("rho phi theta", nonnegative=True)
V_ball = sp.integrate(sp.integrate(sp.integrate(
    rho**2 * sp.sin(phi), (rho, 0, 1)), (phi, 0, sp.pi)), (theta, 0, 2*sp.pi))
V_change = sp.simplify(J * V_ball)
print("Volume (change of variables) =", V_change, "=", sp.N(V_change, 12))
assert sp.simplify(V_formula - V_change) == 0

# 3) Monte-Carlo volume check (independent numeric)
rng = np.random.default_rng(42)
N = 4_000_000
A, B, C = 1.0, 1.0/np.sqrt(2), 1.0/np.sqrt(3)
X = rng.uniform(-A, A, N); Y = rng.uniform(-B, B, N); Z = rng.uniform(-C, C, N)
inside = (X**2 + 2*Y**2 + 3*Z**2) <= 1
V_mc = float(inside.mean()) * (2*A) * (2*B) * (2*C)
print(f"Volume (Monte Carlo) = {V_mc:.6f}  (exact {float(sp.N(V_formula, 12)):.6f})")
assert abs(V_mc - float(sp.N(V_formula, 12))) < 5e-4

print("OK: maximizing region is E0 = {x^2 + 2 y^2 + 3 z^2 <= 1}")
print("OK: Volume(E0) =", V_formula)
