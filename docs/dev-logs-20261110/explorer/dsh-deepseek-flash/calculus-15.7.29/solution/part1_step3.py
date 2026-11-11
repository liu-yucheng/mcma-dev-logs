"""Check the six orders numerically with Gauss-Legendre quadrature.

The script integrates the same solid in the six orders that the page prints, first with
f = 1 and then with f = x**2 * z**2.  The first test must give the volume 4*pi and the
second must give pi/3.

Usage:
    python part1_step3.py
"""

import numpy as np
from numpy.polynomial.legendre import leggauss

NODES = 80
TOLERANCE = 1.0e-9
NODES_BASE, WEIGHTS_BASE = leggauss(NODES)
SINES = 0.5 * (1.0 + NODES_BASE)


def rule(low: float, high: float) -> tuple:
    """Return Gauss-Legendre points and weights on one interval.

    The nodes are pushed toward both ends by the substitution x = low + (high - low) *
    (1 - cos(pi * s)) / 2.  This softens the square-root behaviour that appears where a
    limit curve meets the plane y = 0.

    Args:
        low: The lower end of the interval.
        high: The upper end of the interval.

    Returns:
        A tuple of two arrays: the points and the weights.
    """
    shape = 0.5 * (1.0 - np.cos(np.pi * SINES))
    points = low + (high - low) * shape
    scaled = 0.25 * (high - low) * np.pi * np.sin(np.pi * SINES) * WEIGHTS_BASE
    return points, scaled


def dy_dx_dz(f) -> float:
    """Integrate f with y first, then x, then z."""
    total = 0.0
    zs, wz = rule(-1.0, 1.0)
    for z_value, z_weight in zip(zs, wz):
        half_x = 2.0 * np.sqrt(1.0 - z_value**2)
        xs, wx = rule(-half_x, half_x)
        for x_value, x_weight in zip(xs, wx):
            ys, wy = rule(0.0, 4.0 - x_value**2 - 4.0 * z_value**2)
            total += z_weight * x_weight * float(np.sum(wy * f(x_value, ys, z_value)))
    return total


def dy_dz_dx(f) -> float:
    """Integrate f with y first, then z, then x."""
    total = 0.0
    xs, wx = rule(-2.0, 2.0)
    for x_value, x_weight in zip(xs, wx):
        half_z = 0.5 * np.sqrt(4.0 - x_value**2)
        zs, wz = rule(-half_z, half_z)
        for z_value, z_weight in zip(zs, wz):
            ys, wy = rule(0.0, 4.0 - x_value**2 - 4.0 * z_value**2)
            total += x_weight * z_weight * float(np.sum(wy * f(x_value, ys, z_value)))
    return total


def dx_dy_dz(f) -> float:
    """Integrate f with x first, then y, then z."""
    total = 0.0
    zs, wz = rule(-1.0, 1.0)
    for z_value, z_weight in zip(zs, wz):
        ys, wy = rule(0.0, 4.0 - 4.0 * z_value**2)
        for y_value, y_weight in zip(ys, wy):
            half_x = np.sqrt(4.0 - 4.0 * z_value**2 - y_value)
            xs, wx = rule(-half_x, half_x)
            total += z_weight * y_weight * float(np.sum(wx * f(xs, y_value, z_value)))
    return total


def dx_dz_dy(f) -> float:
    """Integrate f with x first, then z, then y."""
    total = 0.0
    ys, wy = rule(0.0, 4.0)
    for y_value, y_weight in zip(ys, wy):
        half_z = 0.5 * np.sqrt(4.0 - y_value)
        zs, wz = rule(-half_z, half_z)
        for z_value, z_weight in zip(zs, wz):
            half_x = np.sqrt(4.0 - y_value - 4.0 * z_value**2)
            xs, wx = rule(-half_x, half_x)
            total += y_weight * z_weight * float(np.sum(wx * f(xs, y_value, z_value)))
    return total


def dz_dy_dx(f) -> float:
    """Integrate f with z first, then y, then x."""
    total = 0.0
    xs, wx = rule(-2.0, 2.0)
    for x_value, x_weight in zip(xs, wx):
        ys, wy = rule(0.0, 4.0 - x_value**2)
        for y_value, y_weight in zip(ys, wy):
            half_z = 0.5 * np.sqrt(4.0 - x_value**2 - y_value)
            zs, wz = rule(-half_z, half_z)
            total += x_weight * y_weight * float(np.sum(wz * f(x_value, y_value, zs)))
    return total


def dz_dx_dy(f) -> float:
    """Integrate f with z first, then x, then y."""
    total = 0.0
    ys, wy = rule(0.0, 4.0)
    for y_value, y_weight in zip(ys, wy):
        half_x = np.sqrt(4.0 - y_value)
        xs, wx = rule(-half_x, half_x)
        for x_value, x_weight in zip(xs, wx):
            half_z = 0.5 * np.sqrt(4.0 - y_value - x_value**2)
            zs, wz = rule(-half_z, half_z)
            total += y_weight * x_weight * float(np.sum(wz * f(x_value, y_value, zs)))
    return total


def constant_one(x, y, z):
    """Return the constant function 1 on the shape of the inner variable."""
    return np.ones_like(y)


def weight_x2_z2(x, y, z):
    """Return x**2 * z**2 on the shape of the inner variable."""
    if isinstance(x, np.ndarray):
        return x**2 * z**2
    if isinstance(y, np.ndarray):
        return np.full(y.shape, x**2 * z**2)
    return np.full(z.shape, x**2 * z**2)


def main() -> None:
    """Print the six values for both test functions and the largest difference."""
    orders = [
        ("dy dx dz", dy_dx_dz),
        ("dy dz dx", dy_dz_dx),
        ("dx dy dz", dx_dy_dz),
        ("dx dz dy", dx_dz_dy),
        ("dz dy dx", dz_dy_dx),
        ("dz dx dy", dz_dx_dy),
    ]
    exact_volume = 4.0 * np.pi
    exact_weight = np.pi / 3.0

    print(f"Gauss-Legendre rule with {NODES} nodes in each direction")
    print()
    print("test 1: f = 1, expected 4*pi = %.15f" % exact_volume)
    worst = 0.0
    for name, function in orders:
        value = function(constant_one)
        worst = max(worst, abs(value - exact_volume))
        print(f"  {name}: {value:.15f}   difference {value - exact_volume:+.2e}")
    print(f"  largest difference: {worst:.2e}, tolerance {TOLERANCE:.0e}")
    print()
    print("test 2: f = x^2*z^2, expected pi/3 = %.15f" % exact_weight)
    worst = 0.0
    for name, function in orders:
        value = function(weight_x2_z2)
        worst = max(worst, abs(value - exact_weight))
        print(f"  {name}: {value:.15f}   difference {value - exact_weight:+.2e}")
    print(f"  largest difference: {worst:.2e}, tolerance {TOLERANCE:.0e}")


if __name__ == "__main__":
    main()
