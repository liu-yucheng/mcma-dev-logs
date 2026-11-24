"""Verify the cylindrical and spherical descriptions of Part 3.

Each check compares two computations: a one-dimensional integral with the closed form of its
antiderivative, a product of three numerical factors of the spherical Jacobian with the closed
form ``18*pi``, and a Monte Carlo estimate of the cap volume with its standard error.
"""

import math

import numpy as np

from silo_geometry import (
    CAP_RADIUS,
    CYLINDER_HEIGHT,
    CYLINDER_RADIUS,
    body_holds,
    cap_point,
    cap_volume,
    inner_cylinder_integral,
    total_volume,
)
from verification_report import CheckLog

RANDOM_SEED = 20261123
"""Seed of every random sample of this part."""

MONTE_CARLO_COUNT = 1_000_000
"""Number of sampled points of the Monte Carlo estimate of the cap volume."""

TOLERANCE = 1.0e-6
"""Tolerance of a one-dimensional integral, in the unit of the exercise.

The integrand ``r * sqrt(9 - r**2)`` has an infinite second derivative at ``r = 3``, so the
composite Simpson rule of 200001 points carries an error of about 3.5e-8.
"""


def simpson(function, lower: float, upper: float, count: int = 200001) -> float:
    """Return the integral of a function of one variable by the composite Simpson rule."""
    if count % 2 == 0:
        count += 1
    step = (upper - lower) / (count - 1)
    total = 0.0
    for index in range(count):
        value = lower + index * step
        weight = 1.0 if index in (0, count - 1) else (4.0 if index % 2 == 1 else 2.0)
        total += weight * function(value)
    return total * step / 3.0


def radial_integrand(radius: float) -> float:
    """Return the height of the ceiling times the radius of the cylindrical element."""
    return radius * (CYLINDER_HEIGHT + math.sqrt(max(0.0, CAP_RADIUS**2 - radius * radius)))


def cap_volume_monte_carlo() -> tuple[float, float]:
    """Return the Monte Carlo volume of the cap and its standard error.

    The sample box covers the cap: x and y from -3 to 3, z from 10 to 13.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.uniform(-CAP_RADIUS, CAP_RADIUS, MONTE_CARLO_COUNT)
    y_values = generator.uniform(-CAP_RADIUS, CAP_RADIUS, MONTE_CARLO_COUNT)
    z_values = generator.uniform(CYLINDER_HEIGHT, CYLINDER_HEIGHT + CAP_RADIUS, MONTE_CARLO_COUNT)
    inside = (
        x_values * x_values + y_values * y_values + (z_values - CYLINDER_HEIGHT) ** 2
        <= CAP_RADIUS**2
    )
    box_volume = (2.0 * CAP_RADIUS) ** 2 * CAP_RADIUS
    fraction = float(np.mean(inside))
    standard_error = box_volume * math.sqrt(fraction * (1.0 - fraction) / MONTE_CARLO_COUNT)
    return box_volume * fraction, standard_error


def spherical_map_errors() -> int:
    """Return the number of sampled spherical points of the cap that leave the body."""
    generator = np.random.default_rng(RANDOM_SEED)
    failures = 0
    for radius, inclination, azimuth in zip(
        generator.uniform(0.0, CAP_RADIUS, 3000),
        generator.uniform(0.0, 0.5 * math.pi, 3000),
        generator.uniform(0.0, 2.0 * math.pi, 3000),
    ):
        point = (
            float(radius) * math.sin(float(inclination)) * math.cos(float(azimuth)),
            float(radius) * math.sin(float(inclination)) * math.sin(float(azimuth)),
            CYLINDER_HEIGHT + float(radius) * math.cos(float(inclination)),
        )
        if not body_holds(*point):
            failures += 1
    return failures


def minus_branch_inside_count() -> int:
    """Return the number of points of the lower branch of the sphere that lie in the body."""
    count = 0
    for radius in np.linspace(0.05, CAP_RADIUS, 40):
        height = CYLINDER_HEIGHT - math.sqrt(max(0.0, CAP_RADIUS**2 - radius * radius))
        if body_holds(float(radius), 0.0, height):
            count += 1
    return count


def main() -> None:
    """Run every check of Part 3 and write the summary table."""
    log = CheckLog("part3")

    radial_numeric = simpson(radial_integrand, 0.0, CYLINDER_RADIUS)
    radial_exact = inner_cylinder_integral()
    log.record(
        "C1 radial integral: Simpson of $r(10+\\sqrt{9-r^{2}})$ against $45+9$",
        radial_numeric,
        radial_exact,
        abs(radial_numeric - radial_exact),
        abs(radial_numeric - radial_exact) < TOLERANCE,
    )

    cylindrical_volume = 2.0 * math.pi * radial_exact
    log.record(
        "C2 cylindrical volume: $2\\pi$ times the radial integral against $108\\pi$",
        cylindrical_volume,
        total_volume(),
        abs(cylindrical_volume - total_volume()),
        abs(cylindrical_volume - total_volume()) < 1.0e-9,
    )

    theta_factor = simpson(lambda value: 1.0, 0.0, 2.0 * math.pi, 2001)
    phi_factor = simpson(math.sin, 0.0, 0.5 * math.pi, 2001)
    rho_factor = simpson(lambda value: value * value, 0.0, CAP_RADIUS, 2001)
    spherical_numeric = theta_factor * phi_factor * rho_factor
    log.record(
        "C3 spherical volume: product of three numerical Jacobian factors against $18\\pi$",
        spherical_numeric,
        cap_volume(),
        abs(spherical_numeric - cap_volume()),
        abs(spherical_numeric - cap_volume()) < 1.0e-6,
    )

    naive_ball = 2.0 / 3.0 * math.pi * (CYLINDER_HEIGHT + CAP_RADIUS) ** 3
    log.record(
        "C4 one ball of radius 13 about the origin against the true volume, "
        "the two values must differ",
        naive_ball,
        total_volume(),
        abs(naive_ball - total_volume()),
        abs(naive_ball - total_volume()) > 100.0,
    )

    cap_monte_carlo, cap_error = cap_volume_monte_carlo()
    cap_difference = abs(cap_monte_carlo - cap_volume())
    log.record(
        "C5 cap volume: Monte Carlo estimate against $18\\pi$",
        cap_monte_carlo,
        cap_volume(),
        cap_difference,
        cap_difference <= 3.0 * cap_error,
    )

    failures = spherical_map_errors()
    log.record(
        "C6 spherical map: 3000 cap points against the membership test",
        float(failures),
        0.0,
        float(failures),
        failures == 0,
    )

    minus_count = minus_branch_inside_count()
    log.record(
        "C7 lower branch $z=10-\\sqrt{9-r^{2}}$: 40 points against the membership test",
        float(minus_count),
        40.0,
        float(40 - minus_count),
        minus_count == 40,
    )

    print(f"theta factor {theta_factor:.9f}, phi factor {phi_factor:.9f}, "
          f"rho factor {rho_factor:.9f}", flush=True)
    print(f"cap Monte Carlo standard error {cap_error:.6f}, "
          f"three standard errors {3.0 * cap_error:.6f}", flush=True)
    print(f"naive ball volume {naive_ball:.6f} against true volume {total_volume():.6f}, "
          f"ratio {naive_ball / total_volume():.6f}", flush=True)
    print(f"apex of the cap {cap_point(0.0, 0.0)}", flush=True)
    log.require_all_passed()
    log.write()


if __name__ == "__main__":
    main()
