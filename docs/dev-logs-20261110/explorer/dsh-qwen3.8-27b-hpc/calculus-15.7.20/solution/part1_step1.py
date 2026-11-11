"""Exercise 15.7.20: volume between paraboloids y = x^2+z^2 and y = 8-x^2-z^2.
With r^2 = x^2+z^2: y from r^2 to 8-r^2; intersection at r = 2.
"""
import sympy as sp
import numpy as np

r, th, y = sp.symbols('r theta y', real=True, nonnegative=True)

# Intersection: r^2 = 8 - r^2  ->  r = 2 (y = 4)
rstar = [v for v in sp.solve(sp.Eq(r**2, 8 - r**2), r) if v >= 0]
print("intersection radius:", rstar)

# Volume = double integral over the disk (r<=2) of (upper - lower) dA
V = sp.integrate(sp.integrate((8 - r**2 - r**2) * r, (r, 0, 2)), (th, 0, 2*sp.pi))
print("volume exact:", sp.simplify(V), "=", float(V))

# Independent check: full triple integral, y inner, polar in xz-plane
V2 = sp.integrate(sp.integrate(sp.integrate(1, (y, r**2, 8 - r**2)) * r, (r, 0, 2)), (th, 0, 2*sp.pi))
print("volume via triple integral:", sp.simplify(V2), "=", float(V2))
assert sp.simplify(V - V2) == 0

# Numeric cross-check (2D Riemann sum of height * r dr dth)
thg, rg = np.meshgrid(np.linspace(0, 2*np.pi, 1500), np.linspace(0, 2, 1500))
Vnum = np.sum((8 - 2*rg**2) * rg) * (2*np.pi/1500) * (2/1500)
print("numeric Riemann sum:", Vnum, " exact 16*pi =", 16*np.pi)
print("OK")
