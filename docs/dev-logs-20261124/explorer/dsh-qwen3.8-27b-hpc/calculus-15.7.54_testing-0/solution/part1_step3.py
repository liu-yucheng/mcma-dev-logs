"""Step 1.3: the average value f_ave = (4*pi/3)/(pi/2) = 8/3."""
import numpy as np
import sympy as sp

r = sp.symbols("r", positive=True)
V = sp.Rational(1, 2)*sp.pi
N4 = sp.simplify(sp.integrate(r**3*(1 - r**2)**2, (r, 0, 1))*2*sp.pi)
fave = sp.simplify(N4/V)
print("f_ave exact =", fave, "=", round(float(fave), 4))

rng = np.random.default_rng(5)
N = 200000
u = rng.random(2*N); v = rng.random(2*N)
rr = np.sqrt(u); th = 2*np.pi*v
x = rr*np.cos(th); y = rr*np.sin(th); z = 1 - rr**2
k = (x*x + y*y <= 1.0) & (z >= 0.0)
fav = float(np.mean((x[k]**2 + y[k]**2)*z[k]))
print("Monte Carlo f_ave:", round(fav, 4))
assert abs(fav - float(fave)) < 0.06
print("PASS 1.3")
