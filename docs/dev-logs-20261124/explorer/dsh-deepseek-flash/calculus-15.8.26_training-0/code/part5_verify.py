"""Check the volume of part 5 by three methods that do not use the closed form.

Run with ``code/.venv/Scripts/python.exe code/part5_verify.py``.
"""

from __future__ import annotations

import math

import numpy as np

import solid_geometry as geometry

RADIUS = geometry.REFERENCE_RADIUS


def check_horizontal_slices() -> None:
    """Check the slice integral of the lens area against the closed form."""
    slice_value = geometry.volume_by_horizontal_slices(RADIUS)
    geometry.report_check(
        "horizontal_slices_match_closed_form",
        slice_value,
        geometry.exact_volume(RADIUS),
        1.0e-7,
        "integral over z of the lens area against (2/3) pi a^3 - (8/9) a^3",
    )
    print(f"FACT slice_volume={slice_value:.12f}")
    print(
        f"FACT slice_area_at_z_0={geometry.lens_area(RADIUS, RADIUS / 2.0, RADIUS / 2.0):.12f} "
        f"at_z_0.5={geometry.lens_area(math.sqrt(RADIUS**2 - 0.25), RADIUS / 2.0, RADIUS / 2.0):.12f} "
        f"at_z_0.9={geometry.lens_area(math.sqrt(RADIUS**2 - 0.81), RADIUS / 2.0, RADIUS / 2.0):.12f}"
    )


def check_cylinder_axis_polar() -> None:
    """Check the volume from polar coordinates about the cylinder axis."""
    polar_value = geometry.volume_by_cylinder_axis_polar(RADIUS)
    geometry.report_check(
        "cylinder_axis_polar_matches_closed_form",
        polar_value,
        geometry.exact_volume(RADIUS),
        1.0e-7,
        "double integral about the cylinder axis against the closed form",
    )
    print(f"FACT polar_volume={polar_value:.12f}")


def check_monte_carlo() -> None:
    """Check the Monte Carlo estimate against the closed form within four errors."""
    estimate, standard_error = geometry.volume_by_monte_carlo(RADIUS)
    geometry.report_check(
        "monte_carlo_agreement",
        estimate,
        geometry.exact_volume(RADIUS),
        4.0 * standard_error,
        "rejection sampling with 4 million samples against the closed form at four standard errors",
    )
    ratio = abs(estimate - geometry.exact_volume(RADIUS)) / standard_error
    print(
        f"FACT monte_carlo_estimate={estimate:.12f} standard_error={standard_error:.12f} "
        f"difference_in_errors={ratio:.6f}"
    )


def check_scaling() -> None:
    """Check that the volume grows with the cube of the radius."""
    radii = (1.0, 2.0, 3.0)
    values = {radius_value: geometry.volume_by_horizontal_slices(radius_value) for radius_value in radii}
    for radius_value in (1.0, 2.0, 3.0):
        geometry.report_check(
            f"slice_volume_at_a_{radius_value:.0f}",
            values[radius_value],
            geometry.exact_volume(radius_value),
            1.0e-6,
            f"slice integral at a = {radius_value:.0f} against the closed form",
        )
    geometry.report_check(
        "scaling_ratio_at_two",
        values[2.0] / values[1.0],
        8.0,
        1.0e-6,
        "V(2a)/V(a) against the cube ratio eight",
    )
    geometry.report_check(
        "scaling_ratio_at_three",
        values[3.0] / values[1.0],
        27.0,
        1.0e-6,
        "V(3a)/V(a) against the cube ratio twenty seven",
    )
    print(f"FACT scaled_volumes a=1:{values[1.0]:.9f} a=2:{values[2.0]:.9f} a=3:{values[3.0]:.9f}")


def check_lens_area() -> None:
    """Check the lens formula at an interior height against a grid count."""
    height_value = 0.5
    large = math.sqrt(RADIUS**2 - height_value**2)
    grid = np.linspace(-1.0, 1.0, 2400)
    x_grid, y_grid = np.meshgrid(grid, grid)
    large_mask = x_grid**2 + y_grid**2 <= large**2
    small_mask = (x_grid - RADIUS / 2.0) ** 2 + y_grid**2 <= (RADIUS / 2.0) ** 2
    grid_area = float(np.count_nonzero(large_mask & small_mask)) * (grid[1] - grid[0]) ** 2
    geometry.report_check(
        "lens_area_at_z_0.5",
        geometry.lens_area(large, RADIUS / 2.0, RADIUS / 2.0),
        grid_area,
        3.0e-3,
        "lens formula against a 2400 by 2400 grid count at z = 0.5",
    )
    print(f"FACT lens_area_grid_at_z_0.5={grid_area:.12f}")


def main() -> None:
    """Run every check of part 5 and print the summary."""
    check_horizontal_slices()
    check_cylinder_axis_polar()
    check_monte_carlo()
    check_scaling()
    check_lens_area()
    geometry.summarize("part5")


if __name__ == "__main__":
    main()
