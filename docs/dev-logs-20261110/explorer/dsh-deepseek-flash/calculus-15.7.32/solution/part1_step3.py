"""Evaluate the six iterated integrals numerically.

Fixed Gauss-Legendre quadrature integrates every polynomial exactly, so each
ordering returns the volume or the test integral to machine precision. One
ordering is also evaluated with mpmath tanh-sinh quadrature as a check on the
quadrature rule.
"""

import numpy as np
from mpmath import mp, mpf, quad

mp.dps = 16
GAUSS_POINTS = 60


def gauss_nodes(low, high):
    """Return Gauss-Legendre nodes and weights for interval bounds of any shape."""
    low = np.asarray(low, dtype=float)
    high = np.asarray(high, dtype=float)
    nodes, weights = np.polynomial.legendre.leggauss(GAUSS_POINTS)
    half_width = 0.5 * (high - low)
    midpoint = 0.5 * (high + low)
    node_grid = midpoint[..., None] + half_width[..., None] * nodes
    weight_grid = half_width[..., None] * weights
    return node_grid, weight_grid


def unit(x, y, z):
    """Return 1 at every point."""
    return np.ones_like(x + y + z)


def product(x, y, z):
    """Return the test integrand x*y*z."""
    return x * y * z


def order_dz_dy_dx(f):
    """Integrate f with z innermost, then y, then x."""
    x_nodes, x_weights = gauss_nodes(0.0, 2.0)
    y_nodes, y_weights = gauss_nodes(2.0 - x_nodes, 2.0)
    z_nodes, z_weights = gauss_nodes(0.0, (x_nodes[:, None] + y_nodes - 2.0) / 2.0)
    values = f(x_nodes[:, None, None], y_nodes[:, :, None], z_nodes)
    return np.einsum("ijk,i,ij,ijk->", values, x_weights, y_weights, z_weights)


def order_dz_dx_dy(f):
    """Integrate f with z innermost, then x, then y."""
    y_nodes, y_weights = gauss_nodes(0.0, 2.0)
    x_nodes, x_weights = gauss_nodes(2.0 - y_nodes, 2.0)
    z_nodes, z_weights = gauss_nodes(0.0, (x_nodes + y_nodes[:, None] - 2.0) / 2.0)
    values = f(x_nodes[:, :, None], y_nodes[:, None, None], z_nodes)
    return np.einsum("ijk,i,ij,ijk->", values, y_weights, x_weights, z_weights)


def order_dy_dz_dx(f):
    """Integrate f with y innermost, then z, then x."""
    x_nodes, x_weights = gauss_nodes(0.0, 2.0)
    z_nodes, z_weights = gauss_nodes(0.0, x_nodes / 2.0)
    y_nodes, y_weights = gauss_nodes(2.0 + 2.0 * z_nodes - x_nodes[:, None], 2.0)
    values = f(x_nodes[:, None, None], y_nodes, z_nodes[:, :, None])
    return np.einsum("ijk,i,ij,ijk->", values, x_weights, z_weights, y_weights)


def order_dy_dx_dz(f):
    """Integrate f with y innermost, then x, then z."""
    z_nodes, z_weights = gauss_nodes(0.0, 1.0)
    x_nodes, x_weights = gauss_nodes(2.0 * z_nodes, 2.0)
    y_nodes, y_weights = gauss_nodes(2.0 + 2.0 * z_nodes[:, None] - x_nodes, 2.0)
    values = f(x_nodes[:, :, None], y_nodes, z_nodes[:, None, None])
    return np.einsum("ijk,i,ij,ijk->", values, z_weights, x_weights, y_weights)


def order_dx_dz_dy(f):
    """Integrate f with x innermost, then z, then y."""
    y_nodes, y_weights = gauss_nodes(0.0, 2.0)
    z_nodes, z_weights = gauss_nodes(0.0, y_nodes / 2.0)
    x_nodes, x_weights = gauss_nodes(2.0 + 2.0 * z_nodes - y_nodes[:, None], 2.0)
    values = f(x_nodes, y_nodes[:, None, None], z_nodes[:, :, None])
    return np.einsum("ijk,i,ij,ijk->", values, y_weights, z_weights, x_weights)


def order_dx_dy_dz(f):
    """Integrate f with x innermost, then y, then z."""
    z_nodes, z_weights = gauss_nodes(0.0, 1.0)
    y_nodes, y_weights = gauss_nodes(2.0 * z_nodes, 2.0)
    x_nodes, x_weights = gauss_nodes(2.0 + 2.0 * z_nodes[:, None] - y_nodes, 2.0)
    values = f(x_nodes, y_nodes[:, :, None], z_nodes[:, None, None])
    return np.einsum("ijk,i,ij,ijk->", values, z_weights, y_weights, x_weights)


orders = [
    ("dz dy dx", order_dz_dy_dx),
    ("dz dx dy", order_dz_dx_dy),
    ("dy dz dx", order_dy_dz_dx),
    ("dy dx dz", order_dy_dx_dz),
    ("dx dz dy", order_dx_dz_dy),
    ("dx dy dz", order_dx_dy_dz),
]

print(f"Gauss-Legendre quadrature with {GAUSS_POINTS} points per variable")
print("f = 1, so every value is the volume of E")
volume_values = []
for label, order in orders:
    value = order(unit)
    volume_values.append(value)
    print(f"  order {label}: {value:.15f}")
print(f"largest spread: {max(volume_values) - min(volume_values):.3e}")
print(f"2/3: {2.0 / 3.0:.15f}")

print("f = x*y*z, a nonconstant integrand")
product_values = []
for label, order in orders:
    value = order(product)
    product_values.append(value)
    print(f"  order {label}: {value:.15f}")
print(f"largest spread: {max(product_values) - min(product_values):.3e}")
print(f"19/45: {19.0 / 45.0:.15f}")

# Independent check of one ordering with tanh-sinh quadrature.
inner = lambda x, y: quad(lambda z: mpf(1), [0, (x + y - 2) / 2], maxdegree=4)
middle = lambda x: quad(lambda y: inner(x, y), [2 - x, 2], maxdegree=5)
mpmath_volume = quad(middle, [0, 2], maxdegree=5)
print(f"mpmath volume for the order dz dy dx: {mp.nstr(mpmath_volume, 16)}")
