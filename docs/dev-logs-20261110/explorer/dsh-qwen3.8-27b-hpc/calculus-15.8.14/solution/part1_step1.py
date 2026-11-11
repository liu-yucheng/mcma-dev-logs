"""Problem 15.8.14: describe the solid between the paraboloids
z = x^2 + y^2 (opens up, vertex at origin) and z = 5 - x^2 - y^2
(opens down, vertex at (0,0,5)), in cylindrical coordinates.

Intersection: r^2 = 5 - r^2  =>  r^2 = 5/2  =>  r = sqrt(5/2), z = 5/2.
So E = { (r, theta, z): 0 <= theta <= 2 pi, 0 <= r <= sqrt(5/2),
          r^2 <= z <= 5 - r^2 }.
Verify the bounds symbolically.
"""
import sympy as sp

r, theta = sp.symbols("r theta", nonnegative=True)
z_lo = r**2
z_hi = 5 - r**2
# solve intersection
sol = sp.solve(sp.Eq(z_lo, z_hi), r)
print("intersection radii:", sol)
r_star = sp.sqrt(sp.Rational(5, 2))
print("r* =", r_star, "=", sp.N(r_star, 12))
z_star = sp.simplify(z_lo.subs(r, r_star))
print("z* =", z_star, "=", sp.N(z_star, 12))
assert sp.simplify(z_star - sp.Rational(5, 2)) == 0

# sanity: for 0 < r < r* we have z_lo < z_hi
test = sp.simplify((z_hi - z_lo).subs(r, sp.Rational(1, 2)))
print("z_hi - z_lo at r = 1/2:", test, "(positive:", test > 0, ")")

# cylindrical description of the volume (also used by the figure)
V = sp.integrate(sp.integrate(sp.integrate(r, (sp.Symbol("z"), z_lo, z_hi)),
                              (r, 0, r_star)), (theta, 0, 2*sp.pi))
print("Volume of the solid =", sp.simplify(V), "=", sp.N(sp.simplify(V), 12))
