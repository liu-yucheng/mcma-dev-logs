"""Verify Part 3: the inequality description, the vertical extent, and one volume cross-check.

Each check compares a value that one method computes with a value that a second
method computes.  Each check prints the computed value and the expected value,
and it stops with an error when the two values differ by more than the stated
tolerance.  The problem of this session asks for a drawing and for no volume.
The volume of this part is a cross-check of the inequality description, and the
page labels it as such.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

RANDOM_SEED = 20261123
SAMPLE_COUNT = 2000000
HEIGHT_TOLERANCE = 1.0e-9
VOLUME_TOLERANCE = 1.0e-9
BOX_HALF_WIDTH = 1.6
BOX_TOP = 5.0


def lower_height(squared_radius: float) -> float:
    """Return the height of the lower surface at one squared radius."""
    return squared_radius


def upper_height(squared_radius: float) -> float:
    """Return the height of the upper surface at one squared radius."""
    return 5.0 - squared_radius


def bar_length(squared_radius: float) -> float:
    """Return the length of the vertical bar of the solid at one squared radius."""
    return upper_height(squared_radius) - lower_height(squared_radius)


# BEGIN CHECK description_matches_forms
def check_description_matches_forms() -> None:
    """Check that the Cartesian form and the polar form name the same set of points.

    The Cartesian form tests the two heights at the point $(x, y)$.  The polar
    form tests the disk once and then the same two heights in the squared
    distance.  A random sample of the box decides the two tests independently,
    and the two tests must return the same answer for every sampled point.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    point_count = 200000
    x_values = generator.uniform(-BOX_HALF_WIDTH, BOX_HALF_WIDTH, point_count)
    y_values = generator.uniform(-BOX_HALF_WIDTH, BOX_HALF_WIDTH, point_count)
    z_values = generator.uniform(-0.5, BOX_TOP + 0.5, point_count)
    squared_radius = x_values**2 + y_values**2
    cartesian_form = (squared_radius <= z_values) & (z_values <= 5.0 - squared_radius)
    polar_form = (
        (squared_radius <= 2.5)
        & (squared_radius <= z_values)
        & (z_values <= 5.0 - squared_radius)
    )
    disagreement_count = int(np.count_nonzero(cartesian_form != polar_form))
    accepted_share = float(np.count_nonzero(cartesian_form)) / float(point_count)
    print("[description_matches_forms] points where the two forms disagree")
    print(f"    computed {disagreement_count}   expected 0   over {point_count} sampled points")
    print("[description_matches_forms] share of the sampled box that the body holds")
    print(f"    computed {accepted_share:.6f}   expected a value between 0 and 1")
    assert disagreement_count == 0, f"the two forms disagree at {disagreement_count} points"
    assert 0.0 < accepted_share < 1.0, "the sampled box holds no point of the body or every point of it"
# END CHECK description_matches_forms


# BEGIN CHECK vertical_extent
def check_vertical_extent() -> None:
    """Check the vertical extent of the solid against the optima of the two surfaces."""
    rim_squared_radius = float(brentq(bar_length, 0.0, 3.0, xtol=1.0e-15))
    algebraic_rim = 2.5
    print("[vertical_extent] squared radius at which the bar length falls to 0, root against 5/2")
    print(f"    computed {rim_squared_radius:.12f}   expected {algebraic_rim:.12f}")
    print(f"    difference {abs(rim_squared_radius - algebraic_rim):.3e}   tolerance 1.0e-10")
    assert abs(rim_squared_radius - algebraic_rim) < 1.0e-10

    search_options = {"xatol": 1.0e-14}
    lower_minimum = minimize_scalar(
        lower_height, bounds=(0.0, rim_squared_radius), method="bounded", options=search_options
    )
    upper_minimum = minimize_scalar(
        lambda value: -upper_height(value),
        bounds=(0.0, rim_squared_radius),
        method="bounded",
        options=search_options,
    )
    bottom = float(lower_minimum.fun)
    top = float(-upper_minimum.fun)
    print("[vertical_extent] lowest height of the solid, bounded search against 0")
    print(f"    computed {bottom:.12f}   expected 0.000000000000   tolerance {HEIGHT_TOLERANCE:.1e}")
    print("[vertical_extent] highest height of the solid, bounded search against 5")
    print(f"    computed {top:.12f}   expected 5.000000000000   tolerance {HEIGHT_TOLERANCE:.1e}")
    assert abs(bottom) < HEIGHT_TOLERANCE
    assert abs(top - 5.0) < HEIGHT_TOLERANCE

    radius_grid = np.linspace(0.0, rim_squared_radius, 5001)
    bar_values = 5.0 - 2.0 * radius_grid
    sampled_bottom = float(np.min(radius_grid))
    sampled_top = float(np.max(5.0 - radius_grid))
    print("[vertical_extent] same extent read from a 5001 point sample of the two surfaces")
    print(f"    computed {sampled_bottom:.12f} and {sampled_top:.12f}   expected 0 and 5")
    assert abs(sampled_bottom - bottom) < HEIGHT_TOLERANCE
    assert abs(sampled_top - top) < HEIGHT_TOLERANCE
    print(f"[vertical_extent] the vertical bar at the middle of the projection has the length {float(bar_length(0.0)):.6f}")
    assert abs(float(bar_length(0.0)) - 5.0) < HEIGHT_TOLERANCE
    assert float(np.min(bar_values)) > -1.0e-15
# END CHECK vertical_extent


# BEGIN CHECK volume_two_methods
def check_volume_two_methods() -> None:
    """Check the volume of the solid by three methods that use different limits."""
    rim = math.sqrt(2.5)
    cylindrical_volume = float(
        quad(lambda radius: 2.0 * math.pi * radius * (5.0 - 2.0 * radius ** 2), 0.0, rim, limit=200)[0]
    )
    middle = 2.5
    slice_volume = float(
        quad(lambda height: math.pi * height, 0.0, middle, limit=200)[0]
        + quad(lambda height: math.pi * (5.0 - height), middle, 5.0, limit=200)[0]
    )
    exact_volume = float(Fraction(5, 2) ** 2) * math.pi
    print("[volume_two_methods] volume from the cylinder sweep against the volume from the two slice ranges")
    print(f"    computed {cylindrical_volume:.12f}   expected {slice_volume:.12f}")
    print(f"    difference {abs(cylindrical_volume - slice_volume):.3e}   tolerance {VOLUME_TOLERANCE:.1e}")
    assert abs(cylindrical_volume - slice_volume) < VOLUME_TOLERANCE

    print("[volume_two_methods] the closed form pi (5/2)^2 against the cylinder sweep")
    print(f"    computed {exact_volume:.12f}   expected {cylindrical_volume:.12f}")
    print(f"    difference {abs(exact_volume - cylindrical_volume):.3e}   tolerance {VOLUME_TOLERANCE:.1e}")
    assert abs(exact_volume - cylindrical_volume) < VOLUME_TOLERANCE

    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.uniform(-BOX_HALF_WIDTH, BOX_HALF_WIDTH, SAMPLE_COUNT)
    y_values = generator.uniform(-BOX_HALF_WIDTH, BOX_HALF_WIDTH, SAMPLE_COUNT)
    z_values = generator.uniform(0.0, BOX_TOP, SAMPLE_COUNT)
    squared_radius = x_values ** 2 + y_values ** 2
    inside = (squared_radius <= z_values) & (z_values <= 5.0 - squared_radius)
    box_volume = (2.0 * BOX_HALF_WIDTH) ** 2 * BOX_TOP
    inside_share = float(np.mean(inside))
    sampled_volume = box_volume * inside_share
    standard_error = box_volume * math.sqrt(inside_share * (1.0 - inside_share) / SAMPLE_COUNT)
    gap_in_errors = abs(sampled_volume - exact_volume) / standard_error
    print("[volume_two_methods] random sampling of the box against the closed form")
    print(f"    computed {sampled_volume:.6f}   expected {exact_volume:.6f}")
    print(f"    standard error {standard_error:.6f}   gap {gap_in_errors:.3f} standard errors   tolerance 3.0")
    assert gap_in_errors < 3.0
# END CHECK volume_two_methods


def main() -> None:
    """Run every check of Part 3."""
    check_description_matches_forms()
    check_vertical_extent()
    check_volume_two_methods()
    print("part3_verify.py: every check of Part 3 passed")


if __name__ == "__main__":
    main()
