"""Check the geometry of part 1: coordinate conversion, the two surfaces, and the angle range.

Run with ``code/.venv/Scripts/python.exe code/part1_verify.py``.
Every check compares a value from one method with a value from another method.
"""

from __future__ import annotations

import math

import numpy as np

import solid_geometry as geometry

RADIUS = geometry.REFERENCE_RADIUS


def check_coordinate_round_trip() -> None:
    """Check that the conversion from (r, theta) to (x, y) and back keeps both values."""
    generator = np.random.default_rng(11)
    radial = generator.uniform(0.0, RADIUS, 5000)
    angle = generator.uniform(-math.pi, math.pi, 5000)
    x_values = radial * np.cos(angle)
    y_values = radial * np.sin(angle)
    radial_back = np.hypot(x_values, y_values)
    angle_back = np.arctan2(y_values, x_values)
    radial_error = float(np.max(np.abs(radial_back - radial)))
    angle_error = float(np.max(np.abs(np.angle(np.exp(1j * (angle_back - angle))))))
    geometry.report_check(
        "coordinate_round_trip_radial",
        radial_error,
        0.0,
        1.0e-12,
        "forward map r(cos, sin) against inverse map hypot",
    )
    geometry.report_check(
        "coordinate_round_trip_angle",
        angle_error,
        0.0,
        1.0e-12,
        "forward angle against arctan2 of the same point",
    )


def check_cylinder_predicates() -> None:
    """Check that the polar form and the Cartesian form of the cylinder agree."""
    generator = np.random.default_rng(12)
    x_values = generator.uniform(-1.5 * RADIUS, 1.5 * RADIUS, 60000)
    y_values = generator.uniform(-1.5 * RADIUS, 1.5 * RADIUS, 60000)
    radial = np.hypot(x_values, y_values)
    angle = np.arctan2(y_values, x_values)
    polar_mask = geometry.cylinder_membership_polar(radial, angle, RADIUS)
    cartesian_mask = geometry.cylinder_membership_cartesian(x_values, y_values, RADIUS)
    disagreements = int(np.count_nonzero(polar_mask != cartesian_mask))
    geometry.report_check(
        "cylinder_predicates_agree",
        float(disagreements),
        0.0,
        0.0 + 1.0e-9,
        "60000 samples: polar r <= a cos(theta) against (x - a/2)^2 + y^2 <= (a/2)^2",
    )
    mismatched_radius = geometry.cylinder_membership_polar(radial, angle, 1.25 * RADIUS)
    control_gap = int(np.count_nonzero(mismatched_radius != cartesian_mask))
    geometry.report_falsification(
        "cylinder_predicates_control",
        float(control_gap),
        0.0,
        500.0,
        "the same comparison with a mismatched radius must disagree on many samples",
    )
    inside_count = int(np.count_nonzero(cartesian_mask))
    print(
        f"FACT cylinder_samples_inside={inside_count} of 60000 "
        f"fraction={inside_count / 60000:.6f} expected_fraction={math.pi * (RADIUS / 2) ** 2 / 9.0:.6f}"
    )


def check_angle_range() -> None:
    """Check the two ends of the angle range and one angle outside the range."""
    at_right_end = RADIUS * math.cos(math.pi / 2.0)
    at_left_end = RADIUS * math.cos(-math.pi / 2.0)
    geometry.report_check(
        "angle_range_right_end_radius",
        at_right_end,
        0.0,
        1.0e-15,
        "a cos(pi/2) against the exact value zero",
    )
    geometry.report_check(
        "angle_range_left_end_radius",
        at_left_end,
        0.0,
        1.0e-15,
        "a cos(-pi/2) against the exact value zero",
    )
    outside_value = RADIUS * math.cos(3.0 * math.pi / 4.0)
    geometry.report_check(
        "angle_outside_range_is_negative",
        outside_value,
        -math.sqrt(2.0) / 2.0,
        1.0e-15,
        "a cos(3 pi/4) against minus root two over two",
    )
    print(f"FACT maximum_admissible_radius={RADIUS * math.cos(0.0):.12f} at theta=0")
    print(f"FACT radius_at_pi_over_2={at_right_end:.3e} so the base is one point at the origin")
    assert outside_value < 0.0, "the angle outside the range must give a negative radius"


def check_vertical_extent() -> None:
    """Check that the vertical extent of the ball meets the sphere and stops there."""
    generator = np.random.default_rng(13)
    radial = generator.uniform(0.0, RADIUS, 400)
    angle = generator.uniform(-math.pi / 2.0, math.pi / 2.0, 400)
    radial = np.minimum(radial, RADIUS * np.cos(angle))
    top = np.sqrt(np.maximum(RADIUS**2 - radial**2, 0.0))
    residual = radial**2 + top**2 - RADIUS**2
    geometry.report_check(
        "vertical_extent_on_sphere",
        float(np.max(np.abs(residual))),
        0.0,
        1.0e-12,
        "r^2 + z_top^2 against a^2 at 400 base points",
    )
    inside_at_top = geometry.sphere_membership(
        radial * np.cos(angle), radial * np.sin(angle), top - 1.0e-3, RADIUS
    )
    outside_above_top = geometry.sphere_membership(
        radial * np.cos(angle), radial * np.sin(angle), top + 1.0e-3, RADIUS
    )
    geometry.report_check(
        "vertical_extent_inside_below_top",
        float(np.count_nonzero(inside_at_top)),
        float(radial.size),
        0.0 + 1.0e-9,
        "membership 0.001 below the top against the count of all samples",
    )
    geometry.report_check(
        "vertical_extent_outside_above_top",
        float(np.count_nonzero(outside_above_top)),
        0.0,
        1.0e-9,
        "membership 0.001 above the top against the count zero",
    )
    print(
        f"FACT first_base_point r={radial[0]:.6f} theta={angle[0]:.6f} "
        f"top={top[0]:.6f} bottom={-top[0]:.6f}"
    )


def check_surface_directions() -> None:
    """Check the slope of the upper surface and of the lower surface at three radii."""
    step = 1.0e-6
    for radius_value in (0.3, 0.6, 0.9):
        upper_slope = (
            geometry.upper_height(radius_value + step, RADIUS)
            - geometry.upper_height(radius_value - step, RADIUS)
        ) / (2.0 * step)
        exact_upper = -radius_value / math.sqrt(RADIUS**2 - radius_value**2)
        lower_slope = (
            -geometry.upper_height(radius_value + step, RADIUS)
            + geometry.upper_height(radius_value - step, RADIUS)
        ) / (2.0 * step)
        exact_lower = radius_value / math.sqrt(RADIUS**2 - radius_value**2)
        geometry.report_check(
            f"upper_surface_slope_at_r_{radius_value:.1f}",
            upper_slope,
            exact_upper,
            1.0e-6,
            "central difference of sqrt(a^2 - r^2) against minus r over sqrt(a^2 - r^2)",
        )
        geometry.report_check(
            f"lower_surface_slope_at_r_{radius_value:.1f}",
            lower_slope,
            exact_lower,
            1.0e-6,
            "central difference of minus sqrt(a^2 - r^2) against plus r over sqrt(a^2 - r^2)",
        )
        assert upper_slope < 0.0 < lower_slope, "the two surfaces must fall and rise in opposite ways"
    print("FACT upper surface decreases with r; lower surface increases with r")


def check_base_area() -> None:
    """Check the area of the footprint by a grid quadrature and by the lens formula."""
    grid = np.linspace(-0.6, RADIUS + 0.1, 1400)
    x_grid, y_grid = np.meshgrid(grid, grid)
    mask = geometry.cylinder_membership_cartesian(x_grid, y_grid, RADIUS)
    cell_area = (grid[1] - grid[0]) ** 2
    grid_area = float(np.count_nonzero(mask)) * cell_area
    geometry.report_check(
        "base_area_grid",
        grid_area,
        math.pi * (RADIUS / 2.0) ** 2,
        2.0e-3,
        "1400 by 1400 midpoint grid against the exact disk area pi (a/2)^2",
    )
    mask_small = geometry.cylinder_membership_cartesian(x_grid, y_grid, RADIUS)
    mask_large = x_grid**2 + y_grid**2 <= RADIUS**2
    intersection_grid = float(np.count_nonzero(mask_small & mask_large)) * cell_area
    geometry.report_check(
        "base_area_lens_formula",
        geometry.lens_area(RADIUS, RADIUS / 2.0, RADIUS / 2.0),
        intersection_grid,
        2.0e-3,
        "lens formula against the grid count of the same two disks",
    )
    print(
        f"FACT footprint_area={math.pi * (RADIUS / 2.0) ** 2:.12f} "
        f"diameter={RADIUS:.6f} center=({RADIUS / 2.0:.6f},0)"
    )


def check_tangency() -> None:
    """Check that the cylinder touches the z axis and does not cross it."""
    center_distance = math.hypot(RADIUS / 2.0, 0.0)
    geometry.report_check(
        "tangency_center_distance",
        center_distance,
        RADIUS / 2.0,
        1.0e-15,
        "hypot of the center against the value a/2",
    )
    geometry.report_check(
        "tangency_clearance",
        abs(center_distance - RADIUS / 2.0),
        0.0,
        1.0e-15,
        "distance from the center to the nearest rim point against zero",
    )
    print("FACT the cylinder is tangent to the z axis at the origin and lies in x >= 0")


def main() -> None:
    """Run every check of part 1 and print the summary."""
    check_coordinate_round_trip()
    check_cylinder_predicates()
    check_angle_range()
    check_vertical_extent()
    check_surface_directions()
    check_base_area()
    check_tangency()
    geometry.summarize("part1")


if __name__ == "__main__":
    main()
