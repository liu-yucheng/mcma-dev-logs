"""Check Part 1: the body, the star-shaped property, and the form of the volume integral.

Each row of the log pairs a value that one method computes with a value that a second method
computes.  The numeric grid of angles and the exact constants of :mod:`bumpy_sphere` are separate
routes to the same quantity, so a row fails when either route is wrong.
"""

import math
import sys
from fractions import Fraction

import numpy as np
import scipy.integrate

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

import bumpy_sphere
from verification_report import CheckLog

ANGLE_SAMPLE_COUNT = 2001
"""Number of sample points along each angle for the grid checks."""

RAY_SAMPLE_COUNT = 4096
"""Number of directions used by the one-crossing check."""

RADIAL_STEP_COUNT = 4000
"""Number of radial steps along one direction."""


def grid_minimum_and_maximum() -> tuple[float, float]:
    """Return the smallest and the largest radius on a dense grid of angles.

    Returns:
        The two extreme radii of the grid.
    """
    theta = np.linspace(0.0, 2.0 * math.pi, ANGLE_SAMPLE_COUNT)
    phi = np.linspace(0.0, math.pi, ANGLE_SAMPLE_COUNT)
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    values = bumpy_sphere.radius_array(theta_grid, phi_grid)
    return float(values.min()), float(values.max())


def extreme_pole_deviation() -> tuple[float, float]:
    """Return the largest departure of the two poles from the unit sphere.

    Returns:
        The largest deviation at ``varphi = 0`` and the largest deviation at ``varphi = pi``.
    """
    theta = np.linspace(0.0, 2.0 * math.pi, ANGLE_SAMPLE_COUNT)
    radius_zero = bumpy_sphere.radius_array(theta, np.zeros_like(theta))
    radius_pi = bumpy_sphere.radius_array(theta, np.full_like(theta, math.pi))
    return float(np.abs(radius_zero - 1.0).max()), float(np.abs(radius_pi - 1.0).max())


def extreme_seam_deviation() -> float:
    """Return the largest difference of the radius across the seam ``theta = 0`` and ``2 pi``.

    Returns:
        The largest difference of the two edges of the drawn surface.
    """
    phi = np.linspace(0.0, math.pi, ANGLE_SAMPLE_COUNT)
    left = bumpy_sphere.radius_array(np.zeros_like(phi), phi)
    right = bumpy_sphere.radius_array(np.full_like(phi, 2.0 * math.pi), phi)
    return float(np.abs(left - right).max())


def crossing_counts() -> tuple[int, int]:
    """Return the smallest and the largest number of boundary crossings along a ray.

    A ray leaves the origin along one random direction.  The radial distance of the body along
    that ray changes sign of ``r - radius`` exactly once when the body is star-shaped about the
    origin.

    Returns:
        The smallest and the largest count over all sampled directions.
    """
    generator = np.random.default_rng(20261123)
    directions = generator.normal(size=(RAY_SAMPLE_COUNT, 3))
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    steps = np.linspace(1.0e-6, 2.0 * float(bumpy_sphere.BOX_HALF_WIDTH), RADIAL_STEP_COUNT)
    counts = []
    for direction in directions[:256]:
        polar = math.acos(max(-1.0, min(1.0, float(direction[2]))))
        azimuthal = math.fmod(math.atan2(float(direction[1]), float(direction[0])) + 2.0 * math.pi,
                              2.0 * math.pi)
        surface = bumpy_sphere.radius(azimuthal, polar)
        excess = steps - surface
        crossings = int(np.count_nonzero(np.diff(np.sign(excess)) != 0))
        counts.append(crossings)
    return int(min(counts)), int(max(counts))


def cartesian_residual() -> float:
    """Return the largest error of the Cartesian conversion of the surface points.

    Returns:
        The largest absolute difference between the length of a converted point and its radius.
    """
    theta = np.linspace(0.0, 2.0 * math.pi, 401)
    phi = np.linspace(0.0, math.pi, 401)
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    rho = bumpy_sphere.radius_array(theta_grid, phi_grid)
    x, y, z = bumpy_sphere.to_cartesian(theta_grid, phi_grid, rho)
    return float(np.abs(np.sqrt(x * x + y * y + z * z) - rho).max())


def unit_ball_by_quadrature() -> float:
    """Return the volume of the unit ball through the spherical integrand.

    Returns:
        The quadrature value of one third of the integral of ``sin(varphi)`` over the rectangle.
    """
    value, _error = scipy.integrate.dblquad(
        lambda phi, _theta: math.sin(phi) / 3.0,
        0.0, 2.0 * math.pi, lambda _theta: 0.0, lambda _theta: math.pi,
        epsabs=1.0e-13, epsrel=1.0e-13,
    )
    return float(value)


def main() -> None:
    """Run the checks of Part 1 and write the summary of the part."""
    log = CheckLog("part1")
    log_name = "closed body: smallest radius against 4/5"

    smallest, largest = grid_minimum_and_maximum()
    log.record(log_name, smallest, float(bumpy_sphere.RADIUS_MINIMUM),
               abs(smallest - float(bumpy_sphere.RADIUS_MINIMUM)), abs(
                   smallest - float(bumpy_sphere.RADIUS_MINIMUM)) < 1.0e-6)
    log.record("closed body: largest radius against 6/5", largest,
               float(bumpy_sphere.RADIUS_MAXIMUM), abs(largest - float(bumpy_sphere.RADIUS_MAXIMUM)),
               abs(largest - float(bumpy_sphere.RADIUS_MAXIMUM)) < 1.0e-6)

    for label, theta_value, phi_value in (("north", 0.7, 0.0), ("south", 0.7, math.pi)):
        scalar_radius = bumpy_sphere.radius(theta_value, phi_value)
        array_radius = float(bumpy_sphere.radius_array(
            np.array([theta_value]), np.array([phi_value]))[0])
        log.record(
            f"pole at varphi = {'0' if phi_value == 0.0 else 'pi'}: scalar radius against "
            "vectorised radius",
            scalar_radius, array_radius, abs(scalar_radius - array_radius),
            abs(scalar_radius - array_radius) < 1.0e-15 and abs(scalar_radius - 1.0) < 1.0e-15,
        )

    seam = extreme_seam_deviation()
    log.record("seam at theta = 0 and 2 pi: radius difference against 0", seam, 0.0, seam,
               seam < 1.0e-15)

    fewest, most = crossing_counts()
    log.record("crossings of a ray with the surface: range", float(most), float(fewest),
               float(most - fewest), fewest == 1 and most == 1)

    residual = cartesian_residual()
    log.record("Cartesian length against the radius of the same point", residual, 0.0, residual,
               residual < 1.0e-12)

    ball = unit_ball_by_quadrature()
    exact_ball = float(Fraction(4, 3)) * math.pi
    log.record("unit ball volume: quadrature against 4 pi / 3", ball, exact_ball,
               abs(ball - exact_ball), abs(ball - exact_ball) < 1.0e-12)

    log.require_all_passed()
    log.write()
    print(f"smallest radius {smallest:.12g}, largest radius {largest:.12g}", flush=True)
    print(f"pole radius and vectorised radius agree, seam deviation {seam:.3e}", flush=True)
    print(f"crossing counts range from {fewest} to {most} over 256 directions", flush=True)


if __name__ == "__main__":
    main()
