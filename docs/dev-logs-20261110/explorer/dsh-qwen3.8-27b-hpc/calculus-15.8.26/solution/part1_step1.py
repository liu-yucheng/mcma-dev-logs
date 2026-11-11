"""Volume of the solid cut out of the sphere of radius a by the cylinder
r = a*cos(theta)  (problem 15.8.26, part (a)).

Cylindrical coordinates: x = r*cos(theta), y = r*sin(theta), dV = r dz dr dtheta.
  Sphere:   r^2 + z^2 <= a^2  ->  -sqrt(a^2 - r^2) <= z <= sqrt(a^2 - r^2)
  Cylinder: r = a*cos(theta);  r >= 0 forces cos(theta) >= 0, so
            -pi/2 <= theta <= pi/2 and 0 <= r <= a*cos(theta).
The integrand is even in theta, so  V = 2 * Int[0, pi/2] Int[0, a cos(th)].

The inner r-integral is evaluated with the substitution r = a*sin(u):
dr = a*cos(u) du, sqrt(a^2 - r^2) = a*cos(u) for u in [0, pi/2], and the
upper limit r = a*cos(th) corresponds to u = pi/2 - th.
"""

import sympy as sp

a = sp.symbols("a", positive=True)
th = sp.symbols("theta", positive=True)
u = sp.symbols("u", nonnegative=True)

# after the z-integration and the substitution r = a*sin(u):
#   Int_{0}^{a cos(th)} 2*sqrt(a^2 - r^2) * r dr
#     = Int_{0}^{pi/2 - th} 2*a^3*sin(u)*cos(u)^2 du
g = sp.integrate(2 * a**3 * sp.sin(u) * sp.cos(u)**2, (u, 0, sp.pi / 2 - th))
g = sp.simplify(sp.trigsimp(g))
print("g(th) =", g)
claim = 2 * a**3 / 3 * (1 - sp.sin(th)**3)
assert sp.simplify(g - claim) == 0, "inner r-integral mismatch"
print("g(th) = (2/3)a^3 (1 - sin^3 th)  confirmed")

half = sp.integrate(g, (th, 0, sp.pi / 2))
V = sp.simplify(2 * half)
print("V(a) exact   =", V)
print("V(a) factored =", sp.factor(V))
print("V(a) numeric  =", sp.N(V, 12))
print("V(1) numeric  =", sp.N(V.subs(a, 1), 12))
print("V(2) numeric  =", sp.N(V.subs(a, 2), 12))

# Check 1: direct high-precision mpmath quad over the original iterated
# limits (a = 1).  The integrand has a square-root cusp at r -> a, so the
# attainable accuracy is ~1e-8, not 30 digits.
import mpmath as mp
mp.mp.dps = 30


def V_direct(aa):
    inner = lambda t: mp.quad(
        lambda rr: mp.quad(lambda zz: rr,
                           [-mp.sqrt(aa**2 - rr**2), mp.sqrt(aa**2 - rr**2)]),
        [0, aa * mp.cos(t)])
    return mp.quad(inner, [-mp.pi / 2, mp.pi / 2])


num_direct = V_direct(1)
print("direct mpmath (a=1)  =", num_direct)
assert abs(float(num_direct) - float(sp.N(V.subs(a, 1), 25))) < 1e-8

# Check 2: mpmath at 30 digits on the smooth integrand obtained from the
# same substitution (r = a*sin(u)); this one converges to full precision.
def V_sub(aa):
    inner = lambda t: mp.quad(lambda uu: 2 * aa**3 * mp.sin(uu) * mp.cos(uu)**2,
                              [0, mp.pi / 2 - t])
    return mp.quad(inner, [0, mp.pi / 2]) * 2


num_sub = V_sub(1)
print("substituted mpmath   =", num_sub)
assert abs(float(num_sub) - float(sp.N(V.subs(a, 1), 25))) < 1e-14

# Check 3: independent plain numpy trapz rule (a = 1), with the region
# r <= cos(t) masked out.
import numpy as np
Nt, Nr = 20000, 800
t = (np.arange(Nt) + 0.5) / Nt * (np.pi / 2)     # midpoint, theta in [0, pi/2]
R = (np.arange(Nr) + 0.5) / Nr                   # midpoint in [0, 1]
# mapped grid r = R*cos(theta):  dr = cos(theta) dR  (Jacobian!).
r = R[:, None] * np.cos(t)[None, :]              # (Nr, Nt)
integrand = 2 * np.sqrt(np.clip(1.0 - r**2, 0, None)) * r * np.cos(t)[None, :]
# midpoint weights: 1/Nr in R over [0,1], pi/(2 Nt) in theta over [0, pi/2].
trap = 2 * (np.pi / 2) * integrand.sum() / (Nr * Nt)   # factor 2: even theta
print("numpy midpoint sum   =", trap)
assert abs(trap - float(sp.N(V.subs(a, 1), 20))) < 5e-4
print("OK: V = (2/9)*(3*pi - 4)*a^3, verified three independent ways")
