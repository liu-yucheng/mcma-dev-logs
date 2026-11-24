"""E is the dome x^2 + 4z^2 <= 4, 0 <= y <= 4 - x^2 - 4z^2; its volume is 4*pi."""
import numpy as np
import sympy as sp

u, v = sp.symbols("u v", real=True)
for y0 in (0, 1, 4):
    a = 2*sp.sqrt(1 - y0/4)
    b = sp.sqrt(1 - y0/4)
    corners = [f"({float(a):.6f},0)", f"({-float(a):.6f},0)", f"(0,{float(b):.6f})", f"(0,{-float(b):.6f})"]
    print(f"section y={y0}: a={float(a):.6f} b={float(b):.6f} corners={corners}")
V_ref = 2*sp.integrate(4 - 4*u**2 - 4*v**2, (v, -sp.sqrt(1 - u**2), sp.sqrt(1 - u**2)), (u, -1, 1))
V_ref = sp.simplify(V_ref)
print(f"V_exact = {V_ref} = {float(V_ref):.6f}")
rng = np.random.default_rng(42)
N = 2000000
X, Z, Y = rng.uniform(-2, 2, N), rng.uniform(-1, 1, N), rng.uniform(0, 4, N)
inside = (X**2 + 4*Z**2 <= 4) & (Y <= 4 - X**2 - 4*Z**2)
V_mc = 32.0*inside.mean()
print(f"V_mc = {V_mc:.6f} (N={N}, tol=0.06)")
assert abs(V_mc - float(V_ref)) < 0.06, "Monte Carlo deviates from the exact volume"
print("PASS 1.1")
