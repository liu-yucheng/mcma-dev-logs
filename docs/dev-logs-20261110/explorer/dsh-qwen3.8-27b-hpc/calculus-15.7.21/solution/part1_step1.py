"""Exercise 15.7.21: volume enclosed by cylinder y = x^2 and planes z = 0, y + z = 1.
Region: -1 <= x <= 1, x^2 <= y <= 1, 0 <= z <= 1 - y.
"""
import sympy as sp
import numpy as np

x, y, z = sp.symbols('x y z', real=True)

inner = sp.integrate(1, (z, 0, 1 - y))
mid = sp.integrate(inner, (y, x**2, 1))
V = sp.integrate(mid, (x, -1, 1))
print("inner (z):", inner)
print("mid  (y):", sp.simplify(mid))
print("volume exact:", sp.simplify(V), "=", float(V))

# Independent check, order z -> x -> y swapped: for z in [0,1], y in [0,1-z], x^2 <= y
V2 = sp.integrate(sp.integrate(sp.integrate(1, (x, -sp.sqrt(y), sp.sqrt(y))), (y, 0, 1 - z)), (z, 0, 1))
V2 = sp.simplify(V2)
print("volume alternate order:", V2, "=", float(V2))
assert sp.simplify(V - V2) == 0

# Numeric check on the (x,y) footprint
N = 400
xs = np.linspace(-1, 1, N)
ys = np.linspace(0, 1, N)
XX, YY = np.meshgrid(xs, ys, indexing="ij")
inside = (XX**2 <= YY)
Vnum = np.sum(np.where(inside, 1 - YY, 0.0)) * (2/N) * (1/N)
print("numeric:", Vnum, " exact:", float(V))
print("OK")
