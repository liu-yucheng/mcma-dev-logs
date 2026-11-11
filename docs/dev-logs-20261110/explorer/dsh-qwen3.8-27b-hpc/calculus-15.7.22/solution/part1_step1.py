"""Exercise 15.7.22: volume enclosed by cylinder x^2+z^2=4 and planes y=-1, y+z=4.
For (x,z) in disk x^2+z^2<=4: y from -1 to 4-z. Volume = int (5 - z) dA = 20*pi.
"""
import sympy as sp
import numpy as np

x, y, z, r, th = sp.symbols('x y z r theta', real=True)

# polar in the xz-plane: x = r cos th, z = r sin th, dA = r dr dth
V = sp.integrate(sp.integrate((5 - r*sp.sin(th)) * r, (r, 0, 2)), (th, 0, 2*sp.pi))
print("volume exact:", sp.simplify(V), "=", float(V))

# Independent check: rectangular iterated order (y inner)
V2 = sp.integrate(sp.integrate(sp.integrate(1, (y, -1, 4 - z)),
                               (x, -sp.sqrt(4 - z**2), sp.sqrt(4 - z**2))), (z, -2, 2))
print("volume rectangular:", sp.simplify(V2), "=", float(V2))
assert sp.simplify(V - V2) == 0

# Numeric cross-check
thg, rg = np.meshgrid(np.linspace(0, 2*np.pi, 1500), np.linspace(0, 2, 1500))
Vnum = np.sum((5 - rg*np.sin(thg)) * rg) * (2*np.pi/1500) * (2/1500)
print("numeric:", Vnum, " exact 20*pi =", 20*np.pi)
print("OK")
