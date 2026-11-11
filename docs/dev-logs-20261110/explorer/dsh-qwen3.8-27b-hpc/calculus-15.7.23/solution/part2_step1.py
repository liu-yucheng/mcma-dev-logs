"""Exercise 15.7.23(b): use a CAS (sympy) to find the exact value of the integral in (a)."""
import sympy as sp

x, y, z = sp.symbols('x y z', real=True)

# (a):  V = int_0^1 int_y^1 int_0^{sqrt(1-y^2)} dz dx dy
V = sp.integrate(sp.integrate(sp.integrate(1, (z, 0, sp.sqrt(1 - y**2))), (x, y, 1)), (y, 0, 1))
V = sp.simplify(V)
print("exact volume (CAS):", V, "=", float(V))
print("  (pi/4 - 1/3) =", float(sp.pi/4 - sp.Rational(1, 3)))

# Step-by-step, as a human would do by hand:
# inner: z -> sqrt(1-y^2);  x: y..1 -> factor (1-y)
mid = (1 - y) * sp.sqrt(1 - y**2)
outer = sp.integrate(mid, (y, 0, 1))
print("hand-style antiderivative path gives:", sp.simplify(outer))

# Independent check with the order z, y, x (x outer):
# for x in [0,1]: y in [0, x], z in [0, sqrt(1-y^2)]
V2 = sp.integrate(sp.integrate(sp.integrate(1, (z, 0, sp.sqrt(1 - y**2))), (y, 0, x)), (x, 0, 1))
V2 = sp.simplify(V2)
print("alternate order (CAS):", V2, "=", float(V2))
assert sp.simplify(V - V2) == 0
assert sp.simplify(V - (sp.pi/4 - sp.Rational(1, 3))) == 0
print("OK: both orders agree: pi/4 - 1/3")
