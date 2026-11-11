"""Exercise 15.7.18: verify setup and evaluate ∭_E z dV.
E bounded by cylinder y^2+z^2=9 and planes x=0, y=3x, z=0, first octant.
For (y,z) in the quarter disk y^2+z^2<=9, y>=0, z>=0, x runs 0..y/3.
"""
import sympy as sp

x, y, z, r, th = sp.symbols('x y z r theta', real=True, nonnegative=True)

# Inner integral over x first (rectangular order dz dy dx style):
# V_integrand = ∫_{x=0}^{y/3} z dx = z*(y/3)
inner_x = sp.integrate(z, (x, 0, y/3))
# over z: 0..sqrt(9-y^2)
mid = sp.integrate(inner_x, (z, 0, sp.sqrt(9 - y**2)))
full = sp.integrate(mid, (y, 0, 3))
print("iterated (dz dy dx) exact:", sp.simplify(full), "=", float(full))

# Independent check: polar in the yz-plane.
# y = r cos(th), z = r sin(th), dy dz = r dr dth, D: 0<=r<=3, 0<=th<=pi/2
polar = sp.integrate(sp.integrate(
    (r*sp.sin(th)) * (r*sp.cos(th)/3) * r, (r, 0, 3)), (th, 0, sp.pi/2))
print("polar in yz-plane exact:", sp.simplify(polar), "=", float(polar))

assert sp.simplify(full - polar) == 0
print("OK: both methods agree; value =", float(full))
