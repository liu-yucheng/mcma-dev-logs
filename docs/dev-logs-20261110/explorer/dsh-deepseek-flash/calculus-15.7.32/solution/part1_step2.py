"""Evaluate the six iterated integrals over E with symbolic algebra.

Every ordering uses its own bounds. The script evaluates all six with f = 1 and
again with f = x*y*z. Equal results confirm that the six descriptions cover the
same solid.
"""

from sympy import Rational, integrate, simplify, symbols

x, y, z = symbols("x y z", real=True)


def order_dz_dy_dx(f):
    """Integrate f with z innermost, then y, then x."""
    inner = integrate(f, (z, 0, (x + y - 2) / 2))
    middle = integrate(inner, (y, 2 - x, 2))
    return simplify(integrate(middle, (x, 0, 2)))


def order_dz_dx_dy(f):
    """Integrate f with z innermost, then x, then y."""
    inner = integrate(f, (z, 0, (x + y - 2) / 2))
    middle = integrate(inner, (x, 2 - y, 2))
    return simplify(integrate(middle, (y, 0, 2)))


def order_dy_dz_dx(f):
    """Integrate f with y innermost, then z, then x."""
    inner = integrate(f, (y, 2 + 2 * z - x, 2))
    middle = integrate(inner, (z, 0, x / 2))
    return simplify(integrate(middle, (x, 0, 2)))


def order_dy_dx_dz(f):
    """Integrate f with y innermost, then x, then z."""
    inner = integrate(f, (y, 2 + 2 * z - x, 2))
    middle = integrate(inner, (x, 2 * z, 2))
    return simplify(integrate(middle, (z, 0, 1)))


def order_dx_dz_dy(f):
    """Integrate f with x innermost, then z, then y."""
    inner = integrate(f, (x, 2 + 2 * z - y, 2))
    middle = integrate(inner, (z, 0, y / 2))
    return simplify(integrate(middle, (y, 0, 2)))


def order_dx_dy_dz(f):
    """Integrate f with x innermost, then y, then z."""
    inner = integrate(f, (x, 2 + 2 * z - y, 2))
    middle = integrate(inner, (y, 2 * z, 2))
    return simplify(integrate(middle, (z, 0, 1)))


orders = [
    ("dz dy dx", order_dz_dy_dx),
    ("dz dx dy", order_dz_dx_dy),
    ("dy dz dx", order_dy_dz_dx),
    ("dy dx dz", order_dy_dx_dz),
    ("dx dz dy", order_dx_dz_dy),
    ("dx dy dz", order_dx_dy_dz),
]

print("check with f = 1, so every value is the volume of E")
unit_values = []
for label, order in orders:
    value = order(Rational(1))
    unit_values.append(value)
    print(f"  order {label}: {value}")
assert all(value == Rational(2, 3) for value in unit_values)
print("all six values equal 2/3")

print("check with f = x*y*z, a nonconstant integrand")
product_values = []
for label, order in orders:
    value = order(x * y * z)
    product_values.append(value)
    print(f"  order {label}: {value}")
assert all(value == product_values[0] for value in product_values)
print(f"all six values agree, and the common value is {product_values[0]}")

# The inner z-integral of x*y*z is easy to write in closed form.
inner_z = integrate(x * y * z, (z, 0, (x + y - 2) / 2))
print(f"inner z-integral of x*y*z: {simplify(inner_z)}")
