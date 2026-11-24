"""Check the cylindrical integrand and the cylindrical volume element.

The script checks three facts. First, the distance from a point of the cone
surface to the z axis equals its height z, and the check computes the distance
with a cross product instead of the coordinate formula. Second, the Jacobian
determinant of the map from (r, theta, z) to (x, y, z) equals r, and the check
computes the determinant from finite differences. Third, the volume element
r dz dr dtheta integrates to the volume of the cone, and the check compares that
integral with the volume of the stack of disks.
"""

from __future__ import annotations

import numpy as np
from scipy import integrate
import importlib.metadata
import platform

HEIGHT = 1.0
"""The height h of the cone that the numeric checks use."""

RANDOM_SEED = 20261123
"""The seed of the random number generator, so that a result repeats."""


def cylindrical_map(radius: float, angle: float, height: float) -> np.ndarray:
    """Return the Cartesian coordinates of one cylindrical coordinate triple.

    Args:
        radius: The distance r from the z axis.
        angle: The angle theta in radians.
        height: The z coordinate.

    Returns:
        The vector (x, y, z).
    """
    return np.array([radius * np.cos(angle), radius * np.sin(angle), height])


def numeric_jacobian(radius: float, angle: float, height: float) -> float:
    """Return the determinant of the Jacobian of the cylindrical map by finite differences.

    Args:
        radius: The distance r from the z axis.
        angle: The angle theta in radians.
        height: The z coordinate.

    Returns:
        The determinant of the Jacobian matrix at the point.
    """
    step = 1.0e-6
    base = cylindrical_map(radius, angle, height)
    matrix = np.empty((3, 3))
    matrix[:, 0] = (cylindrical_map(radius + step, angle, height) - base) / step
    matrix[:, 1] = (cylindrical_map(radius, angle + step, height) - base) / step
    matrix[:, 2] = (cylindrical_map(radius, angle, height + step) - base) / step
    return float(np.linalg.det(matrix))


def distance_to_axis(point: np.ndarray) -> float:
    """Return the distance from one point to the z axis by a cross product.

    Args:
        point: The Cartesian coordinates of the point.

    Returns:
        The length of the cross product of the point and the unit vector of the z axis.
    """
    axis = np.array([0.0, 0.0, 1.0])
    return float(np.linalg.norm(np.cross(point, axis)))


def print_environment() -> None:
    """Print the version of each tool and the seed, so that a reported result repeats."""
    package_names = ("numpy", "scipy", "sympy", "matplotlib")
    versions = ", ".join(
        f"{name} {importlib.metadata.version(name)}" for name in package_names
    )
    seed = globals().get("RANDOM_SEED", "not used")
    print(f"Python {platform.python_version()}, {versions}, random seed {seed}")
    print()


def main() -> None:
    print_environment()
    """Run the checks of Part 2 and print each computed value beside its expected value."""
    generator = np.random.default_rng(RANDOM_SEED)

    largest_gap = 0.0
    for _ in range(200):
        height = float(generator.uniform(0.05, 1.0)) * HEIGHT
        angle = float(generator.uniform(0.0, 2.0 * np.pi))
        surface_point = cylindrical_map(height, angle, height)
        gap = abs(distance_to_axis(surface_point) - height)
        largest_gap = max(largest_gap, gap)
    print(f"largest gap between the distance to the axis and z on the cone: "
          f"computed = {largest_gap:.3e}, expected = 0.0 (below 1e-12)")
    assert largest_gap <= 1.0e-12, "a point of the cone surface is not at distance z"

    relative_gap = 0.0
    for _ in range(20):
        radius = float(generator.uniform(0.05, 1.0)) * HEIGHT
        angle = float(generator.uniform(0.0, 2.0 * np.pi))
        height = float(generator.uniform(0.0, 1.0)) * HEIGHT
        determinant = numeric_jacobian(radius, angle, height)
        relative_gap = max(relative_gap, abs(determinant - radius) / radius)
    print(f"largest relative gap between the numeric Jacobian and r: "
          f"computed = {relative_gap:.3e}, expected = 0.0 (below 1e-6)")
    assert relative_gap <= 1.0e-6, "the volume element is not r dr dtheta dz"

    volume_element, _ = integrate.tplquad(
        lambda z_value, radius_value, angle_value: radius_value,
        0.0,
        2.0 * np.pi,
        lambda angle_value: 0.0,
        lambda angle_value: HEIGHT,
        lambda angle_value, radius_value: radius_value,
        lambda angle_value, radius_value: HEIGHT,
    )
    volume_disks, _ = integrate.quad(lambda value: np.pi * value * value, 0.0, HEIGHT)
    print(f"volume from the volume element: computed = {volume_element:.9f}, "
          f"volume from the disk stack = {volume_disks:.9f}, "
          f"formula pi*h**3/3 = {np.pi * HEIGHT ** 3 / 3.0:.9f}")
    assert abs(volume_element - volume_disks) <= 1.0e-8, "the two volume integrals disagree"

    integrand_gap = 0.0
    for _ in range(200):
        radius = float(generator.uniform(0.0, 1.0)) * HEIGHT
        angle = float(generator.uniform(0.0, 2.0 * np.pi))
        point = cylindrical_map(radius, angle, 0.0)
        cartesian_value = point[0] ** 2 + point[1] ** 2
        integrand_gap = max(integrand_gap, abs(cartesian_value - radius ** 2))
    print(f"largest gap between x**2 + y**2 and r**2: computed = {integrand_gap:.3e}, "
          f"expected = 0.0 (below 1e-15)")
    assert integrand_gap <= 1.0e-15, "the integrand x**2 + y**2 is not r**2"


if __name__ == "__main__":
    main()
