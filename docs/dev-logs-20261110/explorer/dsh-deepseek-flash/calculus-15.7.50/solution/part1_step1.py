"""Derive the mass, the center of mass, and the z-axis inertia for Exercise 15.7.50.

The solid is E = {(x, y, z) : 0 <= y <= 3, 0 <= x <= y/3, 0 <= z <= s} with
s = sqrt(9 - y**2) and density rho = x**2 + y**2. The script integrates in the
order x, z, y; the radial integrals use y = 3 sin(t) with dy = 3 cos(t) dt.
"""

from sympy import Poly, Rational, cos, expand, integrate, pi, simplify, sin, symbols

x, y, z, t, s = symbols("x y z t s", positive=True)
density = x**2 + y**2


def radial_integral(expression):
    """Integrate an expression in y and s over 0 <= y <= 3 with y = 3 sin(t), s = 3 cos(t)."""
    substituted = expand(expression.subs({s: 3 * cos(t), y: 3 * sin(t)}) * 3 * cos(t))
    return simplify(integrate(substituted, (t, 0, pi / 2)))


basis_names = {}


def basis_value(power_y, power_s):
    """Return the value of the radial integral of y**power_y * s**power_s on 0 <= y <= 3."""
    key = (power_y, power_s)
    if key not in basis_names:
        basis_names[key] = (f"y^{power_y} s^{power_s}", radial_integral(y**power_y * s**power_s))
    return basis_names[key]


print("radial integrals on 0 <= y <= 3, with s = sqrt(9 - y**2):")
for power_y, power_s in [(3, 1), (4, 1), (5, 1), (3, 0)]:
    name, value = basis_value(power_y, power_s)
    print(f"  int {name:8s} dy = {value}")

print()
print("trigonometric integrals used by the substitution y = 3 sin(t):")
for power in [3, 4, 5]:
    value = simplify(integrate(sin(t) ** power * cos(t) ** 2, (t, 0, pi / 2)))
    print(f"  int sin^{power}(t) cos^2(t) dt = {value}")

print()
inner_x = expand(integrate(density, (x, 0, y / 3)))
print(f"mass: the inner integral over x from 0 to y/3 gives {inner_x}")
inner_z = expand(integrate(inner_x, (z, 0, s)))
print(f"mass: the integral over z from 0 to s gives {inner_z}")


def composition(expression, label):
    """Print, integrate, and return an expression in y and s as radial integrals."""
    polynomial = Poly(expand(expression), y, s)
    accumulated = 0
    for (power_y, power_s), coefficient in polynomial.terms():
        name, value = basis_value(power_y, power_s)
        accumulated += coefficient * value
        print(f"  {label}: coefficient {str(coefficient):6s} on int {name:8s} dy = {value}")
    print(f"  {label}: total = {simplify(accumulated)}")
    return simplify(accumulated)


mass = composition(inner_z, "mass M")
print()
moment_yz = composition(expand(integrate(expand(integrate(x * density, (x, 0, y / 3))), (z, 0, s))), "M_yz")
print()
moment_xz = composition(expand(integrate(expand(integrate(y * density, (x, 0, y / 3))), (z, 0, s))), "M_xz")
print()
moment_xy = composition(expand(integrate(expand(integrate(z * density, (x, 0, y / 3))), (z, 0, s))), "M_xy")

print()
print(f"mass M   = {mass}  ~ {float(mass.evalf(12)):.6f}")
print(f"moment about yz M_yz = {moment_yz}  ~ {float(moment_yz.evalf(12)):.6f}")
print(f"moment about xz M_xz = {moment_xz}  ~ {float(moment_xz.evalf(12)):.6f}")
print(f"moment about xy M_xy = {moment_xy}  ~ {float(moment_xy.evalf(12)):.6f}")
print()
print(f"x bar = M_yz / M = {simplify(moment_yz / mass)}  ~ {float((moment_yz / mass).evalf(12)):.6f}")
print(f"y bar = M_xz / M = {simplify(moment_xz / mass)}  ~ {float((moment_xz / mass).evalf(12)):.6f}")
print(f"z bar = M_xy / M = {simplify(moment_xy / mass)}  ~ {float((moment_xy / mass).evalf(12)):.6f}")

print()
print("the integrand of the inertia about the z-axis:")
squared_distance = expand((x**2 + y**2) ** 2)
print(f"  (x^2 + y^2)^2 = {squared_distance}")
inertia_inner_x = expand(integrate(squared_distance, (x, 0, y / 3)))
print(f"  integral over x from 0 to y/3 gives {inertia_inner_x}")
inertia_inner_z = expand(integrate(inertia_inner_x, (z, 0, s)))
print(f"  integral over z from 0 to s gives {inertia_inner_z}")
inertia = composition(inertia_inner_z, "I_z")

assert mass == Rational(56, 5)
assert moment_yz == 171 * pi / 128
assert moment_xz == 63 * pi / 8
assert moment_xy == Rational(21, 2)
assert inertia == Rational(10464, 175)
print()
print("all exact forms agree with the hand derivation")
