"""Check the integral set-up of part 2: the bounds, the Jacobian, and the order.

Run with ``code/.venv/Scripts/python.exe code/part2_verify.py``.
"""

from __future__ import annotations

import math

import numpy as np

import solid_geometry as geometry

RADIUS = geometry.REFERENCE_RADIUS


def check_vertical_length_by_bisection() -> None:
    """Check the vertical length of the ball over a base point by bisection on membership."""
    generator = np.random.default_rng(21)
    angle = generator.uniform(-math.pi / 2.0, math.pi / 2.0, 60)
    radial = generator.uniform(0.0, 1.0, 60) * RADIUS * np.cos(angle)
    worst_error = 0.0
    for index in range(radial.size):
        x_value = radial[index] * math.cos(angle[index])
        y_value = radial[index] * math.sin(angle[index])
        low, high = 0.0, RADIUS
        for _ in range(80):
            middle = 0.5 * (low + high)
            inside = geometry.sphere_membership(
                np.array([x_value]), np.array([y_value]), np.array([middle]), RADIUS
            )[0]
            if inside:
                low = middle
            else:
                high = middle
        measured_top = 0.5 * (low + high)
        closed_top = geometry.upper_height(radial[index], RADIUS)
        worst_error = max(worst_error, abs(measured_top - closed_top))
    geometry.report_check(
        "vertical_length_by_bisection",
        worst_error,
        0.0,
        1.0e-9,
        "80 step bisection on the membership test against sqrt(a^2 - r^2)",
    )
    print(
        f"FACT vertical_length_check r=0.500000 "
        f"length={2.0 * geometry.upper_height(0.5, RADIUS):.12f}"
    )


def check_jacobian_cell() -> None:
    """Check the polar area element against the shoelace area of the same cell."""
    inner, outer = 0.30, 0.85
    start, end = 0.20, 0.95
    exact_area = geometry.polar_cell_area(inner, outer, start, end)
    count = 400
    angles = np.linspace(start, end, count)
    outer_points = list(zip(outer * np.cos(angles), outer * np.sin(angles)))
    inner_points = list(zip(inner * np.cos(angles[::-1]), inner * np.sin(angles[::-1])))
    ring = outer_points + inner_points
    polygon = geometry.polygon_area([point[0] for point in ring], [point[1] for point in ring])
    geometry.report_check(
        "jacobian_cell_area",
        polygon,
        exact_area,
        1.0e-4,
        "shoelace area of the sampled cell against (r2^2 - r1^2)/2 times the angle width",
    )
    grid = np.linspace(-1.0, 1.0, 2200)
    x_grid, y_grid = np.meshgrid(grid, grid)
    radial_grid = np.hypot(x_grid, y_grid)
    angle_grid = np.arctan2(y_grid, x_grid)
    sector_mask = (
        (radial_grid >= inner) & (radial_grid <= outer) & (angle_grid >= start) & (angle_grid <= end)
    )
    grid_area = float(np.count_nonzero(sector_mask)) * (grid[1] - grid[0]) ** 2
    geometry.report_check(
        "jacobian_cell_area_grid",
        grid_area,
        exact_area,
        3.0e-3,
        "2200 by 2200 Cartesian grid count of the sector against the polar sector area",
    )
    print(f"FACT cell_area={exact_area:.12f} so the area element is r dr dtheta")


def check_region_predicates() -> None:
    """Check that the inequality chain and the Cartesian description define one set."""
    generator = np.random.default_rng(22)
    x_values = generator.uniform(-1.4, 1.4, 80000)
    y_values = generator.uniform(-1.4, 1.4, 80000)
    z_values = generator.uniform(-1.4, 1.4, 80000)
    cartesian_mask = geometry.region_membership(x_values, y_values, z_values, RADIUS)
    radial = np.hypot(x_values, y_values)
    angle = np.arctan2(y_values, x_values)
    height = np.sqrt(np.maximum(RADIUS**2 - radial**2, 0.0))
    chain_mask = (
        (angle >= -math.pi / 2.0)
        & (angle <= math.pi / 2.0)
        & (radial >= 0.0)
        & (radial <= RADIUS * np.cos(angle) + 1.0e-15)
        & (np.abs(z_values) <= height + 1.0e-15)
    )
    disagreements = int(np.count_nonzero(chain_mask != cartesian_mask))
    geometry.report_check(
        "region_predicates_agree",
        float(disagreements),
        0.0,
        1.0e-9,
        "80000 samples: the inequality chain against the two Cartesian inequalities",
    )
    broken_mask = (angle >= -math.pi / 3.0) & (angle <= math.pi / 3.0) & (radial <= RADIUS)
    control_gap = int(np.count_nonzero(broken_mask != cartesian_mask))
    geometry.report_falsification(
        "region_predicates_control",
        float(control_gap),
        0.0,
        1000.0,
        "a chain with a shortened angle range must disagree on many samples",
    )
    print(f"FACT region_samples_inside={int(np.count_nonzero(cartesian_mask))} of 80000")


def check_base_radius_by_bisection() -> None:
    """Check the largest admissible r at three angles by bisection on the disk inequality."""
    for angle_value in (0.0, math.pi / 4.0, math.pi / 3.0):
        low, high = 0.0, RADIUS
        for _ in range(80):
            middle = 0.5 * (low + high)
            x_value = middle * math.cos(angle_value)
            y_value = middle * math.sin(angle_value)
            inside = geometry.cylinder_membership_cartesian(
                np.array([x_value]), np.array([y_value]), RADIUS
            )[0]
            if inside:
                low = middle
            else:
                high = middle
        measured = 0.5 * (low + high)
        geometry.report_check(
            f"base_radius_at_theta_{angle_value:.4f}",
            measured,
            RADIUS * math.cos(angle_value),
            1.0e-8,
            "80 step bisection on the disk inequality against a cos(theta)",
        )


def check_single_interval() -> None:
    """Check that one vertical line meets the solid in one closed segment."""
    generator = np.random.default_rng(23)
    angle = generator.uniform(-math.pi / 2.0, math.pi / 2.0, 40)
    radial = generator.uniform(0.0, 1.0, 40) * RADIUS * np.cos(angle)
    heights = np.linspace(-RADIUS, RADIUS, 4001)
    run_counts = []
    for index in range(radial.size):
        x_value = radial[index] * math.cos(angle[index])
        y_value = radial[index] * math.sin(angle[index])
        mask = geometry.sphere_membership(
            np.full(heights.size, x_value), np.full(heights.size, y_value), heights, RADIUS
        )
        transitions = int(np.count_nonzero(mask[1:] & ~mask[:-1]))
        run_counts.append(transitions)
    geometry.report_check(
        "single_vertical_segment",
        float(np.mean(run_counts)),
        1.0,
        1.0e-12,
        "count of inside runs along 40 vertical lines against the value one",
    )
    print(f"FACT run_count_min={min(run_counts)} run_count_max={max(run_counts)}")


def check_missing_jacobian() -> None:
    """Show that the integral without the factor r gives a measurably wrong value."""
    from scipy import integrate

    without_jacobian, _ = integrate.dblquad(
        lambda r, theta: 2.0 * math.sqrt(max(RADIUS**2 - r**2, 0.0)),
        -math.pi / 2.0,
        math.pi / 2.0,
        0.0,
        lambda theta: RADIUS * math.cos(theta),
        epsabs=1.0e-10,
        epsrel=1.0e-10,
    )
    accepted = geometry.exact_volume(RADIUS)
    print(
        f"FACT volume_without_jacobian={without_jacobian:.12f} "
        f"volume_with_jacobian={accepted:.12f}"
    )
    geometry.report_falsification(
        "missing_jacobian_control",
        without_jacobian,
        accepted,
        0.1,
        "the double integral of 2 sqrt(a^2 - r^2) without the factor r against the volume",
    )


def check_triple_integral() -> None:
    """Check the full triple integral against the closed form."""
    numeric_value = geometry.volume_by_triple_quadrature(RADIUS)
    geometry.report_check(
        "triple_integral_matches_closed_form",
        numeric_value,
        geometry.exact_volume(RADIUS),
        1.0e-8,
        "adaptive triple quadrature of the constant integrand r against (2/3) pi a^3 - (8/9) a^3",
    )
    print(f"FACT triple_integral_value={numeric_value:.12f}")
    print(
        f"FACT bound_order theta_outer_r_middle_z_inner: "
        f"theta in [-pi/2, pi/2], r in [0, {RADIUS:.1f} cos(theta)], z in [-h, h]"
    )


def main() -> None:
    """Run every check of part 2 and print the summary."""
    check_vertical_length_by_bisection()
    check_jacobian_cell()
    check_region_predicates()
    check_base_radius_by_bisection()
    check_single_interval()
    check_missing_jacobian()
    check_triple_integral()
    geometry.summarize("part2")


if __name__ == "__main__":
    main()
