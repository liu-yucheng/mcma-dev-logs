"""Monte Carlo in the cylinder r <= sqrt(5/2), 0 <= z <= 5 estimates the enclosed volume at 25*pi/4."""
import numpy as np
import sympy as sp

r = sp.symbols("r", positive=True)
V = sp.simplify(2*sp.pi*sp.integrate((5 - 2*r**2)*r, (r, 0, sp.sqrt(sp.Rational(5, 2)))))
Rf = float(sp.sqrt(sp.Rational(5, 2)))
rng = np.random.default_rng(11)
N = 4_000_000
rr = Rf*np.sqrt(rng.uniform(0.0, 1.0, N))
zz = rng.uniform(0.0, 5.0, N)
frac = float(np.mean((zz >= rr**2) & (zz <= 5.0 - rr**2)))
Vnum = np.pi*Rf**2*5.0*frac
print("V_exact =", V, "=", round(float(V), 4))
print("V_mc =", round(Vnum, 4), " N =", N, " tolerance =", 5e-2)
assert abs(Vnum - float(V)) <= 5e-2, "Monte Carlo mismatch"
print("PASS 1.3")
