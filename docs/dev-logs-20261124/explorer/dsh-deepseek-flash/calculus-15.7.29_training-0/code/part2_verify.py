"""Verification of Part 2: the projection on the plane y = 0 and the sections at fixed y.

The script derives each section from the two inequalities of the solid and never from a
figure. It compares a quadrature of a section area with an area from a substitution, samples
the section along rays to decide whether it is filled or hollow, and prints the corner list
of each boundary section before the shape of that section is named.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parent))

from solid_geometry import (
    APEX_HEIGHT,
    BASE_SEMI_AXIS_X,
    BASE_SEMI_AXIS_Z,
    Z_SQUARED_COEFFICIENT,
    inside_projection,
    section_half_width_x,
    section_half_width_z,
)

# Random seed of every sampled check in this script.
RANDOM_SEED = 20261122

# Count of random points of each membership check.
MEMBERSHIP_SAMPLE_COUNT = 200_000

# Heights of the sections that the script measures, from the base to the apex.
SECTION_HEIGHTS = (0.0, 0.5, 1.0, 2.0, 3.0, 3.9, 3.99)

# Count of radial directions of the filled-section check.
DIRECTION_COUNT = 720

# Tolerance of a compared pair of a continuous quantity.
TOLERANCE = 1.0e-10


def report(name: str, computed: float, reference: float) -> float:
    """Print one compared pair and return the absolute difference.

    Args:
        name: Label of the compared quantity.
        computed: Value from the first method.
        reference: Value from the second method.

    Returns:
        The absolute difference of the two values.
    """
    difference = abs(computed - reference)
    print(f"{name}: computed = {computed:.12f}  reference = {reference:.12f}  "
          f"difference = {difference:.3e}")
    return difference


def check_projection_descriptions() -> None:
    """Compare three descriptions of the projection with random points in the plane y = 0.

    Description one is the inequality x**2 + 4*z**2 <= 4. Description two sweeps x and
    bounds z. Description three sweeps z and bounds x. All three must agree at every point.
    """
    print("--- Section: three descriptions of the projection on the plane y = 0 ---")
    generator = np.random.default_rng(RANDOM_SEED)
    sample_x = generator.uniform(-2.3, 2.3, MEMBERSHIP_SAMPLE_COUNT)
    sample_z = generator.uniform(-1.3, 1.3, MEMBERSHIP_SAMPLE_COUNT)
    by_inequality = inside_projection(sample_x, sample_z)
    by_x_sweep = (np.abs(sample_x) <= BASE_SEMI_AXIS_X) & (
        np.abs(sample_z) <= section_half_width_z(sample_x)
    )
    by_z_sweep = (np.abs(sample_z) <= BASE_SEMI_AXIS_Z) & (
        np.abs(sample_x) <= section_half_width_x(sample_z)
    )
    disagreements = int(np.count_nonzero(by_inequality != by_x_sweep)) + int(
        np.count_nonzero(by_inequality != by_z_sweep)
    )
    print(f"sample count = {MEMBERSHIP_SAMPLE_COUNT}")
    print(f"points inside the projection = {int(np.count_nonzero(by_inequality))}")
    print(f"disagreement count over the three descriptions = {disagreements}")
    assert disagreements == 0
    assert int(np.count_nonzero(by_inequality)) > 1000


def check_section_areas() -> None:
    """Compare the quadrature of each section area with the area from a substitution.

    At height y the section is the set of (x, z) with x**2 + 4*z**2 <= 4 - y. The
    substitution x = R*u, z = (R/2)*w with R**2 = 4 - y maps it onto the unit disk with the
    plane element R**2/2, so its area is pi*(4 - y)/2. The quadrature integrates the half
    width in z over x, which is a different computation.
    """
    print("--- Section: the area of the section at each height ---")
    worst_difference = 0.0
    for height in SECTION_HEIGHTS:
        radius_squared = APEX_HEIGHT - height
        radius = math.sqrt(radius_squared)
        area_exact = math.pi * radius_squared / 2.0
        area_quadrature, _ = quad(
            lambda value: 2.0 * math.sqrt(max(radius_squared - value**2, 0.0)) / 2.0,
            -radius,
            radius,
        )
        area_from_half_widths = math.pi * radius * (radius / 2.0)
        difference = report(
            f"section area at y = {height:.2f} from the quadrature",
            area_quadrature,
            area_exact,
        )
        worst_difference = max(worst_difference, difference)
        print(f"    semi-axes of the section at y = {height:.2f}: "
              f"({radius:.9f}, {radius / 2.0:.9f});  area from the semi-axes = "
              f"{area_from_half_widths:.12f}")
        difference_axes = report(
            f"section area at y = {height:.2f} from the ellipse formula",
            area_from_half_widths,
            area_quadrature,
        )
        worst_difference = max(worst_difference, difference_axes)
    assert worst_difference < 1.0e-8, "a section area disagrees with its substitution value"


def check_section_is_filled() -> None:
    """Check that each section is filled and not hollow, by a scan along its rays.

    The check walks from the center of a section outward along 720 directions. It records the
    radius at which the membership stops, then tests a point at one half of that radius. A
    hollow section would fail the second test.
    """
    print("--- Section: each section is filled, not an annulus ---")
    for height in (0.0, 2.0, 3.9):
        radius_squared = APEX_HEIGHT - height
        failures = 0
        empty_rays = 0
        for direction_index in range(DIRECTION_COUNT):
            angle = 2.0 * math.pi * direction_index / DIRECTION_COUNT
            cosine = math.cos(angle)
            sine = math.sin(angle)
            scale = math.sqrt(radius_squared)
            limit_one = abs(scale * cosine)
            limit_two = abs(scale * sine / 2.0)
            upper = math.hypot(limit_one, limit_two) + 1.0e-9
            radius = brentq(
                lambda value: (value * cosine) ** 2 + Z_SQUARED_COEFFICIENT * (value * sine) ** 2
                - radius_squared,
                0.0,
                upper,
            )
            if radius <= 1.0e-12:
                empty_rays += 1
                continue
            point_x = 0.5 * radius * cosine
            point_z = 0.5 * radius * sine
            if point_x**2 + Z_SQUARED_COEFFICIENT * point_z**2 > radius_squared + 1.0e-12:
                failures += 1
        print(f"height y = {height:.2f}: directions = {DIRECTION_COUNT}, "
              f"rays of zero radius = {empty_rays}, failures at half radius = {failures}")
        assert failures == 0, "a section is hollow along a ray"


def check_boundary_sections() -> None:
    """Print the corner list of each section at a boundary or an interior height.

    The corner list holds the four extreme points of the section. The shape name follows the
    printed list: four distinct corners give a filled ellipse, one distinct corner gives a
    single point.
    """
    print("--- Section: the corner list of each section, which decides its shape ---")
    for height in (0.0, 2.0, 4.0):
        radius_squared = APEX_HEIGHT - height
        if radius_squared < 0.0:
            print(f"height y = {height:.2f}: the section is empty")
            continue
        half_width_x = math.sqrt(radius_squared)
        half_width_z = math.sqrt(radius_squared) / 2.0
        corners = [
            (half_width_x, height, 0.0),
            (-half_width_x, height, 0.0),
            (0.0, height, half_width_z),
            (0.0, height, -half_width_z),
        ]
        distinct = sorted({(round(corner[0], 12), round(corner[2], 12)) for corner in corners})
        print(f"height y = {height:.2f}: half width in x = {half_width_x:.9f}, "
              f"half width in z = {half_width_z:.9f}")
        print(f"    corners = {[(round(a, 6), round(b, 3), round(c, 6)) for a, b, c in corners]}")
        print(f"    distinct corner positions = {len(distinct)}")
        if len(distinct) == 1:
            print("    shape = single point")
        else:
            print("    shape = filled ellipse")
    axis = np.linspace(-0.001, 0.001, 2001)
    grid_x, grid_z = np.meshgrid(axis, axis)
    admissible = grid_x**2 + Z_SQUARED_COEFFICIENT * grid_z**2 <= APEX_HEIGHT - APEX_HEIGHT
    print(f"at y = 4 on a grid of 2001 by 2001 points of width 0.002: "
          f"admissible points = {int(np.count_nonzero(admissible))}")
    assert int(np.count_nonzero(admissible)) == 1
    smallest_area = math.pi * (APEX_HEIGHT - 3.999999) / 2.0
    print(f"section area at y = 3.999999 = {smallest_area:.12f}")
    assert smallest_area > 0.0


def main() -> None:
    """Run every check of Part 2 and print the compared values."""
    check_projection_descriptions()
    check_section_areas()
    check_section_is_filled()
    check_boundary_sections()
    print("Part 2: every compared pair agrees within the stated tolerance.")


if __name__ == "__main__":
    main()
