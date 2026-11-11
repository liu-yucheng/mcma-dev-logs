"""Problem 15.9.45: volume enclosed by the bumpy sphere
rho = 1 + (1/5) sin(6 theta) sin(5 phi),  m = 6, n = 5.

Because rho(theta, phi) >= 1 - 1/5 > 0 the surface is star-shaped with
respect to the origin, so the enclosed volume is exactly
V = (1/3) Int_0^{2 pi} Int_0^pi rho(theta, phi)^3 sin(phi) dphi dtheta.

sympy's naive evaluation of the whole double integral is unreliable here,
so the cube is expanded into four terms and each term is integrated
separately (still symbolically, with sympy).  Every surviving integral is
also checked numerically (mpmath), and the total volume is checked by a
high-precision mpmath double integral and by a fine uniform-grid sum.
"""

import sympy as sp

th, ph = sp.symbols("theta phi", real=True)
eps = sp.Rational(1, 5)
s6 = sp.sin(6 * th)
s5 = sp.sin(5 * ph)

expr = sp.expand(sp.Rational(1, 3) * (1 + eps * s6 * s5) ** 3 * sp.sin(ph))
terms = sp.Add.make_args(expr)
print("number of terms after expansion:", len(terms))

V_terms = []
for t in terms:
    val = sp.integrate(sp.integrate(t, (th, 0, 2 * sp.pi)), (ph, 0, sp.pi))
    val = sp.simplify(val)
    print("term:", t, "  ->  ", val)
    V_terms.append(val)

V = sp.simplify(sum(V_terms))
print("V exact =", V, "  numeric =", sp.N(V, 12))
V_expected = 136 * sp.pi / 99
print("claim 136*pi/99 =", sp.N(V_expected, 12))
assert sp.simplify(V - V_expected) == 0, "term-by-term value mismatch"

# The two nontrivial factor integrals, symbolically and numerically.
I_theta = sp.integrate(sp.sin(6 * th) ** 2, (th, 0, 2 * sp.pi))
I_phi = sp.integrate(sp.sin(ph) * sp.sin(5 * ph) ** 2, (ph, 0, sp.pi))
print("Int sin^2(6t) dt over [0,2pi]  =", I_theta)
print("Int sin(phi) sin^2(5 phi) dphi over [0,pi] =", I_phi)
assert I_theta == sp.pi and I_phi == 100 * sp.Rational(1, 99)
# cross-check of the term-2 product: (1/25)*I_theta*I_phi = 4*pi/99
print("term-2 check:", sp.simplify(sp.Rational(1, 25) * I_theta * I_phi))

# Independent high-precision numeric check, full 2-D integral, no expansion.
import mpmath as mp
mp.mp.dps = 30
f = lambda t, p: (1 + mp.mpf("0.2") * mp.sin(6 * t) * mp.sin(5 * p)) ** 3 * mp.sin(p) / 3
V_num = mp.quad(lambda p: mp.quad(lambda t: f(t, p), [0, 2 * mp.pi]), [0, mp.pi])
print("mpmath double quad:", V_num)
print("136*pi/99          :", mp.mpf(136) * mp.pi / 99)
assert abs(V_num - mp.mpf(136) * mp.pi / 99) < mp.mpf("1e-12"), "numeric mismatch"

# Second independent check: fine uniform grid sum (crude but independent).
import numpy as np
Nt, Np = 2400, 1600
tt = (np.arange(Nt) + 0.5) / Nt * 2 * np.pi
pp = (np.arange(Np) + 0.5) / Np * np.pi
rho = 1 + 0.2 * np.sin(6 * tt)[:, None] * np.sin(5 * pp)[None, :]
grid = (rho ** 3 * np.sin(pp)[None, :]).sum() * (2 * np.pi / Nt) * (np.pi / Np) / 3
print("fine-grid sum:", grid)
assert abs(grid - float(sp.N(V_expected, 15))) < 2e-4, "grid sum mismatch"
print("OK: V = 136*pi/99 exactly, verified three independent ways")
