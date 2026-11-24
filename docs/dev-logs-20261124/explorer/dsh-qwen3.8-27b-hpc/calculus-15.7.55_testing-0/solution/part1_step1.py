"""Step 1.1: the integrand is positive exactly inside the ellipsoid."""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z")
g = 1 - x**2 - 2*y**2 - 3*z**2
print("zero set: x^2 + 2*y^2 + 3*z^2 = 1")
print("semi-axes:", 1, round(float(1/sp.sqrt(2)), 4), round(float(1/sp.sqrt(3)), 4))
print("max of g at origin:", g.subs({x: 0, y: 0, z: 0}))

N = 200000
rng = np.random.default_rng(5)
X = rng.uniform(-1, 1, N); Y = rng.uniform(-1, 1, N); Z = rng.uniform(-1, 1, N)
G = 1 - X**2 - 2*Y**2 - 3*Z**2
print("positive fraction of the box:", round(float((G > 0).mean()), 4))
print("max of g on the sample:", round(float(G.max()), 4))
assert abs(float(G.max()) - 1.0) < 1e-9
print("PASS 1.1")
