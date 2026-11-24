"""Step 1.3: the exact maximum value is 2*sqrt(6)*pi/5."""
import numpy as np
import sympy as sp

Iz = sp.simplify(4*sp.pi/(5*sp.sqrt(6)))
Iz2 = sp.radsimp(Iz)
print("I exact =", Iz2, "=", round(float(Iz), 4))

rng = np.random.default_rng(5)
N = 300000
X = rng.uniform(-1, 1, N); Y = rng.uniform(-1, 1, N); Z = rng.uniform(-1, 1, N)
q = X**2 + 2*Y**2 + 3*Z**2
k = q < 1.0
a, b, c = 1.0, 1.0/np.sqrt(2), 1.0/np.sqrt(3)
Vell = 4.0/3.0*np.pi*a*b*c
G = 1 - q
est = Vell*float(np.mean(G[k]))/max(float(k.mean()), 1e-12)
print("Monte Carlo ellipsoid integral:", round(est, 4))
assert abs(est - float(Iz)) < 0.08
print("PASS 1.3")
