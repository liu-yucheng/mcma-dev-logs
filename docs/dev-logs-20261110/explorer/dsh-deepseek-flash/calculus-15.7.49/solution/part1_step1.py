"""Derive the mass, the center of mass, and the z-axis inertia for Exercise 15.7.49.

The solid is E = {(x, y, z) : 0 <= y <= 1, 0 <= x <= s, 0 <= z <= y} with
s = sqrt(1 - y**2) and density rho = 1 + x + y + z. The script integrates in the
order z, x, y; the radial integrals use y = sin(t) with the Jacobian dy = cos(t) dt.
"""

from sympy import Poly, Rational, cos, expand, integrate, pi, simplify, sin, symbols

x, y, z, t, s = symbols("x y z t s", positive=True)
density = 1 + x + y + z


def radial_integral(expression):
    """Integrate an expression in y and s over 0 <= y <= 1 with y = sin(t), s = cos(t)."""
    substituted = expand(expression.subs({s: cos(t), y: sin(t)}) * cos(t))
    return simplify(integrate(substituted, (t, 0, pi / 2)))


def triple_integral(integrand):
    """Return the triple integral of the integrand over E in the order z, x, y."""
    inner_z = expand(integrate(integrand, (z, 0, y)))
    inner_x = expand(integrate(inner_z, (x, 0, s)))
    return radial_integral(inner_x)


basis_terms = {
    (1, 1): ("y s", y * s),
    (2, 1): ("y^2 s", y**2 * s),
    (3, 1): ("y^3 s", y**3 * s),
    (1, 3): ("y s^3", y * s**3),
    (2, 3): ("y^2 s^3", y**2 * s**3),
    (1, 2): ("y s^2", y * s**2),
    (2, 2): ("y^2 s^2", y**2 * s**2),
    (3, 2): ("y^3 s^2", y**3 * s**2),
    (4, 1): ("y^4 s", y**4 * s),
}
basis_values = {key: (name, radial_integral(term)) for key, (name, term) in basis_terms.items()}

print("elementary radial integrals on 0 <= y <= 1, with s = sqrt(1 - y**2):")
for key in sorted(basis_values, key=lambda item: (item[1], item[0])):
    name, value = basis_values[key]
    print(f"  int {name:9s} dy = {value}")

print()
inner_z = expand(integrate(density, (z, 0, y)))
print(f"mass: the inner integral over z from 0 to y gives {inner_z}")
inner_x = expand(integrate(inner_z, (x, 0, s)))
print(f"mass: the integral over x from 0 to s gives {inner_x}")


def composition(expression, label):
    """Print an x-integrated integrand as coefficients times elementary radial integrals."""
    polynomial = Poly(expand(expression), y, s)
    accumulated = 0
    for (power_y, power_s), coefficient in polynomial.terms():
        name, value = basis_values[(power_y, power_s)]
        accumulated += coefficient * value
        print(f"  {label}: coefficient {str(coefficient):5s} on int {name:9s} dy = {value}")
    print(f"  {label}: total = {simplify(accumulated)}")
    return simplify(accumulated)


mass = composition(inner_x, "mass M")
print()
moment_yz_inner = expand(integrate(x * density, (z, 0, y)))
moment_yz = composition(expand(integrate(moment_yz_inner, (x, 0, s))), "M_yz")
print()
moment_xz_inner = expand(integrate(y * density, (z, 0, y)))
moment_xz = composition(expand(integrate(moment_xz_inner, (x, 0, s))), "M_xz")
print()
moment_xy_inner = expand(integrate(z * density, (z, 0, y)))
moment_xy = composition(expand(integrate(moment_xy_inner, (x, 0, s))), "M_xy")

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
print("inertia about the z-axis as eight monomial integrals:")
monomial_table = [
    ((2, 0, 0), "x^2"),
    ((0, 2, 0), "y^2"),
    ((3, 0, 0), "x^3"),
    ((2, 1, 0), "x^2 y"),
    ((2, 0, 1), "x^2 z"),
    ((1, 2, 0), "x y^2"),
    ((0, 3, 0), "y^3"),
    ((0, 2, 1), "y^2 z"),
]
running_total = 0
for powers, label in monomial_table:
    value = triple_integral(x ** powers[0] * y ** powers[1] * z ** powers[2])
    running_total += value
    print(f"  triple integral of {label:6s} dV = {value}")
inertia = simplify(running_total)
print(f"  I_z = {inertia}  ~ {float(inertia.evalf(12)):.6f}")

assert mass == Rational(11, 24) + 3 * pi / 32
assert moment_yz == Rational(7, 24)
assert moment_xz == pi / 16 + Rational(4, 15)
assert moment_xy == pi / 32 + Rational(13, 90)
assert inertia == Rational(17, 60) + pi / 16
assert inertia == triple_integral((x**2 + y**2) * density)
print()
print("all exact forms agree with the hand derivation")
