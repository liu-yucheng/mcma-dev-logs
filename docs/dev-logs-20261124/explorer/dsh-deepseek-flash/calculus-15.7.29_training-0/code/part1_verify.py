"""Verification of Part 1: read the solid from the two given equations.

Each check compares a value from one method with a value from a different method:
the inequality chain against the substitution image, a root of the surface equation against
a quadrature of the same root, and a grid search for the largest height against a direct
evaluation at the apex. The script prints every compared pair.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exact_integrals import moment_of_unit_disk
from solid_geometry import (
    APEX_HEIGHT,
    inside_projection,
    inside_solid,
    inside_solid_by_substitution,
    upper_height,
)

# Random seed of every sampled check in this script.
RANDOM_SEED = 20261122

# Count of random points of the membership check.
MEMBERSHIP_SAMPLE_COUNT = 200_000

# Count of random directions of the ray check that tests the closure of the solid.
RAY_COUNT = 400

# Relative tolerance of a compared pair of a continuous quantity.
RELATIVE_TOLERANCE = 1.0e-9

# Absolute tolerance of a compared pair of a continuous quantity.
ABSOLUTE_TOLERANCE = 1.0e-9


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


def check_membership_agreement() -> None:
    """Compare the inequality chain with the substitution image on random points.

    The first predicate uses the expression 4 - x**2 - 4*z**2. The second predicate uses
    the scaled radius r = sqrt((x/2)**2 + z**2) and the height 4*(1 - r**2). A point of the
    solid must receive the same answer from both predicates.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    x = generator.uniform(-2.2, 2.2, MEMBERSHIP_SAMPLE_COUNT)
    y = generator.uniform(-0.3, 4.3, MEMBERSHIP_SAMPLE_COUNT)
    z = generator.uniform(-1.2, 1.2, MEMBERSHIP_SAMPLE_COUNT)
    chain_answer = inside_solid(x, y, z)
    substitution_answer = inside_solid_by_substitution(x, y, z)
    disagreement_count = int(np.count_nonzero(chain_answer != substitution_answer))
    print("--- Section: the inequality chain against the substitution image ---")
    print(f"sample count = {MEMBERSHIP_SAMPLE_COUNT}")
    print(f"points inside the solid by the chain = {int(np.count_nonzero(chain_answer))}")
    print(f"points inside the solid by the substitution = {int(np.count_nonzero(substitution_answer))}")
    print(f"disagreement count = {disagreement_count}")
    assert disagreement_count == 0, "the two encodings of the solid disagree"
    inside_count = int(np.count_nonzero(chain_answer))
    assert inside_count > 1000, "the box holds too few interior points for a useful check"


def check_trace_area() -> None:
    """Compare three values of the area of the base ellipse x**2 + 4*z**2 <= 4.

    Method one measures the semi-axes as roots of the surface equation and multiplies them
    by pi. Method two integrates the half width in z over x. Method three counts random
    points. The exact value c*pi from exact arithmetic is the fourth value.
    """
    print("--- Section: the area of the trace on the plane y = 0 ---")
    semi_axis_x = brentq(lambda value: APEX_HEIGHT - value**2, 0.5, 3.0)
    semi_axis_z = brentq(lambda value: APEX_HEIGHT - 4.0 * value**2, 0.2, 2.0)
    area_from_axes = math.pi * semi_axis_x * semi_axis_z
    area_from_quadrature, quadrature_error = quad(
        lambda value: 2.0 * math.sqrt(max(APEX_HEIGHT - value**2, 0.0)) / 2.0,
        -semi_axis_x,
        semi_axis_x,
    )
    generator = np.random.default_rng(RANDOM_SEED + 1)
    area_of_box = 4.4 * 2.2
    sample_count = 400_000
    sample_x = generator.uniform(-2.2, 2.2, sample_count)
    sample_z = generator.uniform(-1.1, 1.1, sample_count)
    hits = inside_projection(sample_x, sample_z)
    hit_fraction = float(np.count_nonzero(hits)) / sample_count
    area_from_sampling = hit_fraction * area_of_box
    standard_error = area_of_box * math.sqrt(hit_fraction * (1.0 - hit_fraction) / sample_count)
    # The substitution x = 2*u and z = w multiplies the plane element by 2, so the area of
    # the base ellipse is 2 times the area of the unit disk.
    area_exact = 2.0 * float(moment_of_unit_disk(0, 0)) * math.pi

    print(f"semi-axis in x from a root = {semi_axis_x:.12f}")
    print(f"semi-axis in z from a root = {semi_axis_z:.12f}")
    difference_axes = report("area from the semi-axes", area_from_axes, area_exact)
    difference_quadrature = report(
        "area from the quadrature", area_from_quadrature, area_from_axes
    )
    print(f"quadrature error estimate = {quadrature_error:.3e}")
    print(f"area from sampling = {area_from_sampling:.12f}  "
          f"standard error = {standard_error:.6f}")
    difference_sampling = abs(area_from_sampling - area_exact)
    print(f"difference of the sampling value from the exact value = {difference_sampling:.3e}  "
          f"in units of the standard error = {difference_sampling / standard_error:.3f}")
    assert abs(semi_axis_x - 2.0) < 1.0e-9
    assert abs(semi_axis_z - 1.0) < 1.0e-9
    assert difference_axes < RELATIVE_TOLERANCE
    assert difference_quadrature < 1.0e-9
    assert difference_sampling <= 3.0 * standard_error, "the sampled area is outside three standard errors"


def check_largest_height() -> None:
    """Compare the largest height from a grid search with the height at the apex.

    The grid search looks for the maximum of 4 - x**2 - 4*z**2 over the projection. The
    reference value is the height at the point (0, 0), which the surface equation evaluates
    directly. The count of grid points that reach the maximum must be one.
    """
    print("--- Section: the largest height of the solid ---")
    axis_x = np.linspace(-2.0, 2.0, 1601)
    axis_z = np.linspace(-1.0, 1.0, 801)
    grid_x, grid_z = np.meshgrid(axis_x, axis_z)
    grid_height = upper_height(grid_x, grid_z)
    grid_maximum = float(np.max(grid_height))
    height_at_apex = float(upper_height(0.0, 0.0))
    difference = report("largest height", grid_maximum, height_at_apex)
    near_maximum = grid_height >= height_at_apex - 1.0e-9
    print(f"grid points that reach the largest height = {int(np.count_nonzero(near_maximum))}")
    print(f"height at the apex = {height_at_apex:.12f}")
    assert difference < 1.0e-6
    assert int(np.count_nonzero(near_maximum)) == 1
    assert abs(height_at_apex - 4.0) < 1.0e-12


def check_closure_by_rays() -> None:
    """Check that the two given surfaces close the solid and that no third wall exists.

    The check starts at an interior point and follows a random direction until the point
    leaves the solid. At the exit point, at least one of the two surface equations must
    hold. A third wall would give an exit point on neither surface.
    """
    print("--- Section: the two surfaces close the solid ---")
    generator = np.random.default_rng(RANDOM_SEED + 2)
    start = np.array([0.0, 2.0, 0.0])
    direction = generator.normal(size=(RAY_COUNT, 3))
    direction /= np.linalg.norm(direction, axis=1, keepdims=True)
    smallest_residual = np.empty(RAY_COUNT)
    exit_on_base = 0
    exit_on_roof = 0
    for index in range(RAY_COUNT):
        step = direction[index]
        low = 0.0
        high = 0.1
        while inside_solid(*(start + high * step)) and high < 40.0:
            high *= 2.0
        for _ in range(80):
            middle = 0.5 * (low + high)
            if inside_solid(*(start + middle * step)):
                low = middle
            else:
                high = middle
        point = start + low * step
        residual_base = abs(point[1])
        residual_roof = abs(point[1] - float(upper_height(point[0], point[2])))
        smallest_residual[index] = min(residual_base, residual_roof)
        if residual_base <= residual_roof:
            exit_on_base += 1
        else:
            exit_on_roof += 1
    print(f"ray count = {RAY_COUNT}")
    print(f"exit points on the plane y = 0 = {exit_on_base}")
    print(f"exit points on the paraboloid = {exit_on_roof}")
    print(f"largest of the smallest residuals = {float(np.max(smallest_residual)):.3e}")
    assert float(np.max(smallest_residual)) < 1.0e-9, "a ray leaves the solid through a third wall"
    assert exit_on_base > 0 and exit_on_roof > 0, "one surface receives no ray"


def main() -> None:
    """Run every check of Part 1 and print the compared values."""
    check_membership_agreement()
    check_trace_area()
    check_largest_height()
    check_closure_by_rays()
    print("Part 1: every compared pair agrees within the stated tolerance.")


if __name__ == "__main__":
    main()
