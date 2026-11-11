"""Evaluate all six orders of integration for two test integrands.

Each order must return the same number for the same integrand. The script uses
f = 1, which gives the volume, and f = y**2 * z**2, which depends on the two
variables that the two disk slicings treat differently.
"""

from sympy import integrate, pi, simplify, sqrt, symbols

x, y, z = symbols("x y z", real=True)

# Each order is a tuple of (variable, lower limit, upper limit) entries. The
# first entry is the innermost integral, the last entry is the outermost.
orders = {
    "dz dy dx": ((z, -sqrt(9 - y**2), sqrt(9 - y**2)), (y, -3, 3), (x, -2, 2)),
    "dz dx dy": ((z, -sqrt(9 - y**2), sqrt(9 - y**2)), (x, -2, 2), (y, -3, 3)),
    "dy dz dx": ((y, -sqrt(9 - z**2), sqrt(9 - z**2)), (z, -3, 3), (x, -2, 2)),
    "dy dx dz": ((y, -sqrt(9 - z**2), sqrt(9 - z**2)), (x, -2, 2), (z, -3, 3)),
    "dx dy dz": ((x, -2, 2), (y, -sqrt(9 - z**2), sqrt(9 - z**2)), (z, -3, 3)),
    "dx dz dy": ((x, -2, 2), (z, -sqrt(9 - y**2), sqrt(9 - y**2)), (y, -3, 3)),
}


def evaluate(order, integrand):
    """Integrate the integrand in the given innermost-to-outermost order."""
    value = integrand
    for variable, lower, upper in order:
        value = integrate(value, (variable, lower, upper))
    return simplify(value)


print("test integrand f = 1, expected volume 36*pi")
values = {}
for name, order in orders.items():
    value = evaluate(order, 1)
    values[name] = value
    print(f"  {name}: {value} = {float(value.evalf(12)):.9f}")
assert all(value == 36 * pi for value in values.values())
print("all six orders give 36*pi")

print("test integrand f = y^2 * z^2, expected value 243*pi/2")
second_values = {}
for name, order in orders.items():
    value = evaluate(order, y**2 * z**2)
    second_values[name] = value
    print(f"  {name}: {value} = {float(value.evalf(12)):.9f}")
assert all(value == 243 * pi / 2 for value in second_values.values())
print("all six orders give 243*pi/2")

# Show the three stages of the first order, for the written report.
inner = integrate(1, (z, -sqrt(9 - y**2), sqrt(9 - y**2)))
middle = integrate(inner, (y, -3, 3))
outer = integrate(middle, (x, -2, 2))
print(f"stages of dz dy dx with f = 1: {inner} -> {middle} -> {outer}")
