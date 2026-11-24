"""Verify the integral of the height and the centroid of Part 5.

Each check compares two computations: the closed form of a volume moment with the integral of
``z`` times the section area, and the exact centroid height with a Monte Carlo estimate that
carries its own standard error.
"""

import math

import numpy as np

from silo_geometry import (
    APEX_HEIGHT,
    CAP_RADIUS,
    CYLINDER_HEIGHT,
    CYLINDER_RADIUS,
    cap_moment_about_base,
    cap_volume,
    centroid_height,
    section_area,
    total_volume,
    volume_moment_about_base,
)
from verification_report import CheckLog

MONTE_CARLO_COUNT = 4_000_000
"""Number of sampled points of the Monte Carlo estimate of the centroid."""

RANDOM_SEED = 20261123
"""Seed of the Monte Carlo sample."""

TOLERANCE = 1.0e-5
"""Tolerance of a numerical volume moment, in cubic units times a length."""


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


def centroid_monte_carlo() -> dict[str, tuple[float, float]]:
    """Return the Monte Carlo mean coordinate and its standard error of each axis.

    The routine samples the box of the body, keeps the points of the body, and takes the mean of
    the three coordinates of the kept points.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.uniform(-CYLINDER_RADIUS, CYLINDER_RADIUS, MONTE_CARLO_COUNT)
    y_values = generator.uniform(-CYLINDER_RADIUS, CYLINDER_RADIUS, MONTE_CARLO_COUNT)
    z_values = generator.uniform(0.0, APEX_HEIGHT, MONTE_CARLO_COUNT)
    squared_radius = x_values * x_values + y_values * y_values
    ceiling = CYLINDER_HEIGHT + np.sqrt(np.maximum(0.0, CAP_RADIUS**2 - squared_radius))
    inside = (squared_radius <= CYLINDER_RADIUS**2) & (z_values <= ceiling)
    result = {}
    for name, values in (("x", x_values), ("y", y_values), ("z", z_values)):
        kept = values[inside]
        result[name] = (
            float(np.mean(kept)),
            float(np.std(kept, ddof=1) / math.sqrt(kept.size)),
        )
    return result


def main() -> None:
    """Run every check of Part 5 and write the summary table."""
    log = CheckLog("part5")

    cylinder_numeric = simpson(lambda value: value * math.pi * CYLINDER_RADIUS**2,
                               0.0, CYLINDER_HEIGHT)
    cylinder_exact = math.pi * CYLINDER_RADIUS**2 * CYLINDER_HEIGHT**2 / 2.0
    log.record(
        "C1 cylinder moment: Simpson of $z\\cdot 9\\pi$ against $450\\pi$",
        cylinder_numeric,
        cylinder_exact,
        abs(cylinder_numeric - cylinder_exact),
        abs(cylinder_numeric - cylinder_exact) < TOLERANCE,
    )

    cap_numeric = simpson(lambda value: value * section_area(value), CYLINDER_HEIGHT, APEX_HEIGHT)
    cap_exact = cap_moment_about_base()
    log.record(
        "C2 cap moment: Simpson of $z\\,A(z)$ over $10\\le z\\le 13$ against "
        "$180\\pi+\\frac{81\\pi}{4}$",
        cap_numeric,
        cap_exact,
        abs(cap_numeric - cap_exact),
        abs(cap_numeric - cap_exact) < TOLERANCE,
    )

    whole_numeric = cylinder_numeric + cap_numeric
    whole_exact = volume_moment_about_base()
    log.record(
        "C3 whole moment: two integrals against $\\frac{2601\\pi}{4}$",
        whole_numeric,
        whole_exact,
        abs(whole_numeric - whole_exact),
        abs(whole_numeric - whole_exact) < TOLERANCE,
    )

    centroid_numeric = whole_numeric / total_volume()
    log.record(
        "C4 centroid height: moment over volume against $\\frac{289}{48}$",
        centroid_numeric,
        centroid_height(),
        abs(centroid_numeric - centroid_height()),
        abs(centroid_numeric - centroid_height()) < 1.0e-9,
    )

    estimates = centroid_monte_carlo()
    monte_carlo, standard_error = estimates["z"]
    difference = abs(monte_carlo - centroid_height())
    log.record(
        "C5 centroid height: Monte Carlo estimate against the exact value",
        monte_carlo,
        centroid_height(),
        difference,
        difference <= 3.0 * standard_error,
    )

    for name in ("x", "y"):
        mean_value, mean_error = estimates[name]
        log.record(
            f"C{6 if name == 'x' else 7} mean {name}: Monte Carlo mean against 0",
            mean_value,
            0.0,
            abs(mean_value),
            abs(mean_value) <= 3.0 * mean_error,
        )

    print(f"cap moment parts: {CYLINDER_HEIGHT * cap_volume():.9f} and "
          f"{cap_exact - CYLINDER_HEIGHT * cap_volume():.9f}", flush=True)
    print(f"centroid height {centroid_height():.12f}, 289/48 "
          f"{289.0 / 48.0:.12f}", flush=True)
    print(f"Monte Carlo standard error {standard_error:.6f}, three standard errors "
          f"{3.0 * standard_error:.6f}, difference {difference:.6f}", flush=True)
    print(f"mean x {estimates['x'][0]:.6f} plus or minus {estimates['x'][1]:.6f}, "
          f"mean y {estimates['y'][0]:.6f} plus or minus {estimates['y'][1]:.6f}", flush=True)
    log.require_all_passed()
    log.write()


if __name__ == "__main__":
    main()
