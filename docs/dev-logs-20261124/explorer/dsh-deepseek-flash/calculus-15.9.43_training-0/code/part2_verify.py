"""Verify the horizontal sections and the volume by slicing of Part 2.

Each check compares two computations: the radius of a section from the ceiling formula against
the radius from a bisection on the membership test, the section area from a formula against the
area of a sampled point set, and the volume from a numerical integral against the exact value of
the antiderivative and against a Monte Carlo estimate.
"""

import math

import numpy as np

from figure_anchors import SLICE_HEIGHTS
from silo_geometry import (
    APEX_HEIGHT,
    CAP_RADIUS,
    CYLINDER_HEIGHT,
    CYLINDER_RADIUS,
    body_holds,
    cap_volume,
    cylinder_volume,
    section_area,
    section_radius_from_formula,
    section_radius_from_membership,
    slice_area_integral,
    total_volume,
)
from verification_report import CheckLog

MONTE_CARLO_COUNT = 2_000_000
"""Number of sampled points of the Monte Carlo estimate of the volume."""

RANDOM_SEED = 20261123
"""Seed of the Monte Carlo sample."""

AREA_TOLERANCE = 1.0e-9
"""Tolerance of the section radius, in the unit of length of the exercise."""

VOLUME_TOLERANCE = 1.0e-6
"""Tolerance of the numerical volume, in cubic units."""


def sampled_section_area(height: float, angle_count: int = 720) -> float:
    """Return the area of a section from the vertices found along the rays of the section.

    The routine reads the membership test only.  Along each ray it bisects the largest radius
    that belongs to the body, and then it takes the shoelace area of the polygon of the vertices.
    """
    vertices = []
    for angle_index in range(angle_count):
        angle = 2.0 * math.pi * angle_index / angle_count
        cosine = math.cos(angle)
        sine = math.sin(angle)
        low = 0.0
        high = CYLINDER_RADIUS
        for _ in range(80):
            middle = 0.5 * (low + high)
            if body_holds(middle * cosine, middle * sine, height):
                low = middle
            else:
                high = middle
        vertices.append((low * cosine, low * sine))
    x_values = np.array([point[0] for point in vertices])
    y_values = np.array([point[1] for point in vertices])
    return float(0.5 * abs(np.sum(x_values * np.roll(y_values, -1)
                                  - np.roll(x_values, -1) * y_values)))


def monte_carlo_volume() -> tuple[float, float]:
    """Return the Monte Carlo volume of the body and its standard error."""
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.uniform(-CYLINDER_RADIUS, CYLINDER_RADIUS, MONTE_CARLO_COUNT)
    y_values = generator.uniform(-CYLINDER_RADIUS, CYLINDER_RADIUS, MONTE_CARLO_COUNT)
    z_values = generator.uniform(0.0, APEX_HEIGHT, MONTE_CARLO_COUNT)
    squared_radius = x_values * x_values + y_values * y_values
    ceiling = CYLINDER_HEIGHT + np.sqrt(np.maximum(0.0, CAP_RADIUS**2 - squared_radius))
    inside = (squared_radius <= CYLINDER_RADIUS**2) & (z_values <= ceiling)
    box_volume = (2.0 * CYLINDER_RADIUS) ** 2 * APEX_HEIGHT
    fraction = float(np.mean(inside))
    standard_error = box_volume * math.sqrt(fraction * (1.0 - fraction) / MONTE_CARLO_COUNT)
    return box_volume * fraction, standard_error


def main() -> None:
    """Run every check of Part 2 and write the summary table."""
    log = CheckLog("part2")

    panel = (0.0, 2.0, 6.0, 10.0, 10.2, 11.0, 11.5, 12.5, 12.95)
    radius_errors = []
    print("height | radius from formula | radius from membership | area", flush=True)
    for height in panel:
        from_formula = section_radius_from_formula(height)
        from_membership = section_radius_from_membership(height)
        radius_errors.append(abs(from_formula - from_membership))
        print(f"{height:6.2f} | {from_formula:.12f} | {from_membership:.12f} | "
              f"{section_area(height):.12f}", flush=True)
    worst_radius = max(radius_errors)
    log.record(
        "C1 section radius: ceiling formula against bisection on membership, 9 heights",
        worst_radius,
        0.0,
        worst_radius,
        worst_radius < AREA_TOLERANCE,
    )

    area_errors = []
    print("height | formula area | sampled area | difference", flush=True)
    for height in SLICE_HEIGHTS:
        formula_area = section_area(height)
        sampled_area = sampled_section_area(height)
        area_errors.append(abs(formula_area - sampled_area))
        print(f"{height:6.2f} | {formula_area:.9f} | {sampled_area:.9f} | "
              f"{abs(formula_area - sampled_area):.3e}", flush=True)
    worst_area = max(area_errors)
    log.record(
        "C2 section area at three heights: formula against the 720-vertex "
        "shoelace polygon of bisected rays",
        worst_area,
        0.0,
        worst_area,
        worst_area < 2.0e-3,
    )

    below = section_area(CYLINDER_HEIGHT)
    above = section_area(CYLINDER_HEIGHT + 1.0e-9)
    log.record(
        "C3 junction: area just below $z=10$ against area just above",
        below,
        above,
        abs(below - above),
        abs(below - above) < 1.0e-6,
    )

    lower_numeric = slice_area_integral(0.0, CYLINDER_HEIGHT, 200001)
    lower_exact = math.pi * CYLINDER_RADIUS**2 * CYLINDER_HEIGHT
    log.record(
        "C4 cylinder volume: Simpson integral of the section area against $\\pi R^{2}H$",
        lower_numeric,
        lower_exact,
        abs(lower_numeric - lower_exact),
        abs(lower_numeric - lower_exact) < 1.0e-4,
    )

    upper_numeric = slice_area_integral(CYLINDER_HEIGHT, APEX_HEIGHT, 200001)
    upper_exact = cap_volume()
    log.record(
        "C5 cap volume: Simpson integral of the section area against $\\frac{2}{3}\\pi R^{3}$",
        upper_numeric,
        upper_exact,
        abs(upper_numeric - upper_exact),
        abs(upper_numeric - upper_exact) < 1.0e-4,
    )

    whole_numeric = lower_numeric + upper_numeric
    whole_exact = total_volume()
    log.record(
        "C6 whole volume: sum of the two integrals against $90\\pi+18\\pi$",
        whole_numeric,
        whole_exact,
        abs(whole_numeric - whole_exact),
        abs(whole_numeric - whole_exact) < VOLUME_TOLERANCE,
    )

    monte_carlo, standard_error = monte_carlo_volume()
    difference = abs(monte_carlo - whole_exact)
    log.record(
        "C7 whole volume: Monte Carlo estimate against the exact value",
        monte_carlo,
        whole_exact,
        difference,
        difference <= 3.0 * standard_error,
    )

    split_at_junction = cylinder_volume() + cap_volume()
    log.record(
        "C8 whole volume: two exact solids against the numerical whole",
        split_at_junction,
        whole_numeric,
        abs(split_at_junction - whole_numeric),
        abs(split_at_junction - whole_numeric) < VOLUME_TOLERANCE,
    )

    print(f"slice heights of Figure 2: {SLICE_HEIGHTS}", flush=True)
    print(f"Monte Carlo standard error: {standard_error:.6f}", flush=True)
    print(f"three standard errors: {3.0 * standard_error:.6f}, "
          f"difference: {difference:.6f}", flush=True)
    print(f"exact volume: {whole_exact:.9f}, 9*pi: {9.0 * math.pi:.9f}", flush=True)
    log.require_all_passed()
    log.write()


if __name__ == "__main__":
    main()
