"""Check the description of the solid cone E and the shape of its horizontal slices.

The script compares two descriptions of the same solid: the Cartesian test
``x**2 + y**2 <= z**2 and z <= h`` and the cylindrical test ``r <= z <= h``.
It also measures the volume, the base radius, the apex height, and the radius
of a slice at three heights. Each measured value comes from a method that is
independent of the formula that it is compared with.
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

BOX_HALF_WIDTH = 1.0
"""The half width of the sampling box in x and in y, in units of h."""

BOX_HEIGHT = 1.0
"""The height of the sampling box in z, in units of h."""


def cartesian_membership(x: np.ndarray, y: np.ndarray, z: np.ndarray, height: float) -> np.ndarray:
    """Return True where the Cartesian inequalities of the statement hold.

    Args:
        x: The x coordinates of the points.
        y: The y coordinates of the points.
        z: The z coordinates of the points.
        height: The height h of the cone.

    Returns:
        A Boolean array with the same shape as the input arrays.
    """
    inside = (x * x + y * y) <= z * z
    return inside & (z >= 0.0) & (z <= height)


def cylindrical_membership(radius: np.ndarray, z: np.ndarray, height: float) -> np.ndarray:
    """Return True where the cylindrical description of the solid holds.

    Args:
        radius: The distance r from the z axis.
        z: The z coordinates of the points.
        height: The height h of the cone.

    Returns:
        A Boolean array with the same shape as the input arrays.
    """
    return (radius <= z) & (z <= height) & (radius >= 0.0)


def sample_box(count: int, height: float, generator: np.random.Generator) -> tuple[np.ndarray, ...]:
    """Return uniformly random points of the sampling box around the cone.

    Args:
        count: The number of points.
        height: The height h of the cone.
        generator: The random number generator.

    Returns:
        The arrays x, y, and z of the sampled points.
    """
    x = generator.uniform(-BOX_HALF_WIDTH * height, BOX_HALF_WIDTH * height, count)
    y = generator.uniform(-BOX_HALF_WIDTH * height, BOX_HALF_WIDTH * height, count)
    z = generator.uniform(0.0, BOX_HEIGHT * height, count)
    return x, y, z


def monte_carlo_volume(count: int, height: float, generator: np.random.Generator) -> tuple[float, float]:
    """Return the Monte Carlo volume of the cone and its standard error.

    Args:
        count: The number of sampled points.
        height: The height h of the cone.
        generator: The random number generator.

    Returns:
        The estimated volume and the standard error of the estimate.
    """
    x, y, z = sample_box(count, height, generator)
    inside = cartesian_membership(x, y, z, height)
    box_volume = (2.0 * BOX_HALF_WIDTH * height) ** 2 * BOX_HEIGHT * height
    fraction = float(np.count_nonzero(inside)) / count
    estimate = box_volume * fraction
    standard_error = box_volume * float(np.sqrt(fraction * (1.0 - fraction) / count))
    return estimate, standard_error


def radial_boundary(height_of_slice: float, height: float) -> float:
    """Return the radius of the slice at one height by bisection on the membership test.

    Args:
        height_of_slice: The value z0 of the slice.
        height: The height h of the cone.

    Returns:
        The radius where the membership test changes from True to False.
    """
    low = 0.0
    high = 2.0 * height
    for _ in range(200):
        middle = 0.5 * (low + high)
        if cylindrical_membership(np.array(middle), np.array(height_of_slice), height):
            low = middle
        else:
            high = middle
    return low


def apex_height(height: float) -> float:
    """Return the lowest z of the solid on the z axis by bisection.

    Args:
        height: The height h of the cone.

    Returns:
        The lowest z at which the point (0, 0, z) belongs to the solid.
    """
    low = -0.5 * height
    high = 0.5 * height
    for _ in range(200):
        middle = 0.5 * (low + high)
        if cylindrical_membership(np.array(0.0), np.array(middle), height):
            high = middle
        else:
            low = middle
    return high


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
    """Run the checks of Part 1 and print each computed value beside its expected value."""
    generator = np.random.default_rng(RANDOM_SEED)
    count = 2_000_000

    x, y, z = sample_box(count, HEIGHT, generator)
    agreement = int(
        np.count_nonzero(
            cartesian_membership(x, y, z, HEIGHT)
            == cylindrical_membership(np.hypot(x, y), z, HEIGHT)
        )
    )
    print(f"points where the two descriptions agree: computed = {agreement}, expected = {count}")
    assert agreement == count, "the Cartesian and the cylindrical descriptions disagree"

    volume_mc, error_mc = monte_carlo_volume(count, HEIGHT, generator)
    volume_quad, _ = integrate.quad(lambda value: np.pi * value * value, 0.0, HEIGHT)
    print(f"volume: Monte Carlo = {volume_mc:.6f} +- {error_mc:.6f}, quad = {volume_quad:.6f}, "
          f"formula pi*h**3/3 = {np.pi * HEIGHT ** 3 / 3.0:.6f}")
    assert abs(volume_mc - volume_quad) <= 4.0 * error_mc, "the Monte Carlo volume is off"

    base_radius = radial_boundary(HEIGHT, HEIGHT)
    print(f"base radius: bisection = {base_radius:.8f}, expected = {HEIGHT:.8f}")
    assert abs(base_radius - HEIGHT) <= 1.0e-6, "the base radius is not h"

    print(f"apex height: bisection = {apex_height(HEIGHT):.8f}, expected = 0.0")
    assert abs(apex_height(HEIGHT)) <= 1.0e-6, "the apex is not at z = 0"

    slice_heights = (0.25 * HEIGHT, 0.50 * HEIGHT, 0.75 * HEIGHT)
    point_count = 400_000
    radius_sample = HEIGHT * np.sqrt(generator.uniform(0.0, 1.0, point_count))
    angle_sample = generator.uniform(0.0, 2.0 * np.pi, point_count)
    for height_of_slice in slice_heights:
        radius = radial_boundary(height_of_slice, HEIGHT)
        area_quad = np.pi * height_of_slice ** 2
        fraction = float(np.count_nonzero(radius_sample <= height_of_slice)) / point_count
        area_mc = np.pi * HEIGHT ** 2 * fraction
        error_mc = np.pi * HEIGHT ** 2 * float(np.sqrt(fraction * (1.0 - fraction) / point_count))
        print(f"slice z = {height_of_slice:.2f}: radius computed = {radius:.8f}, "
              f"expected = {height_of_slice:.8f}; area quad = {area_quad:.6f}, "
              f"area from inside fraction = {area_mc:.6f} +- {error_mc:.6f}")
        assert abs(radius - height_of_slice) <= 1.0e-6, "the slice radius is not z"
        assert abs(area_mc - area_quad) <= 4.0 * error_mc, "the slice area is off"


if __name__ == "__main__":
    main()
