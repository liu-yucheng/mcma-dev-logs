"""Check every numerical claim of Part 1 of the tutorial of Problem 15.7.55.

Part 1 identifies the region on which the integrand is positive. The script compares the
semi-axes, the cross-section areas, and the volume of the ellipsoid $P$, each from two routes.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

CODE_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIRECTORY))

import figure_anchors as anchors
import support

OUTPUT_PATH = CODE_DIRECTORY / "outputs" / "part1_results.json"
SECTION_HEIGHTS = (0.0, 0.2, 0.4)
SAMPLE_COUNT = 400000


def main() -> None:
    """Run the checks of Part 1, print each comparison, and write the result file."""
    ledger = support.CheckLedger("part1")
    first, second, third = support.ellipsoid_semi_axes()

    for axis, formula in (("x", first), ("y", second), ("z", third)):
        root = support.axis_intercept_by_root_finding(axis)
        ledger.add(f"semi_axis_{axis}_by_root_finding", root, formula, 1.0e-9)
        residual = support.boundary_residual(tuple(
            formula if name == axis else 0.0 for name in ("x", "y", "z")))
        ledger.add(f"boundary_residual_on_axis_{axis}", residual, 0.0, 1.0e-12)

    rows: list[dict[str, float]] = []
    for height in SECTION_HEIGHTS:
        semi_x, semi_y = support.cross_section_semi_axes(height)
        area_formula = support.cross_section_area_formula(height)
        area_quadrature = support.cross_section_area_quadrature(height)
        area_sample = support.cross_section_area_numeric_limit(height)
        ledger.add(f"section_area_{height:.1f}_formula_against_quadrature",
                   area_quadrature, area_formula, 1.0e-9 * max(1.0, area_formula))
        ledger.add(f"section_area_{height:.1f}_formula_against_sample",
                   area_sample, area_formula, 2.0e-2 * max(1.0, area_formula))
        root_x = support.half_extent_by_root_finding(height, "x")
        root_y = support.half_extent_by_root_finding(height, "y")
        ledger.add(f"section_{height:.1f}_half_width_x_against_formula", root_x, semi_x, 1.0e-9)
        ledger.add(f"section_{height:.1f}_half_width_y_against_formula", root_y, semi_y, 1.0e-9)
        rows.append({
            "height": height,
            "semi_x": semi_x,
            "semi_y": semi_y,
            "area_formula": area_formula,
            "area_quadrature": area_quadrature,
            "area_sample": area_sample,
        })

    volume_closed = support.ellipsoid_volume_closed_form()
    volume_sections = support.integrate_cross_section_areas()
    ledger.add("volume_closed_form_against_sections", volume_sections, volume_closed, 1.0e-9)
    ledger.add("volume_against_unit_field", support.integrate_cartesian(
        lambda first_coordinate, second_coordinate, third_coordinate: 1.0),
        volume_closed, 1.0e-9)

    generator = np.random.default_rng(20261123)
    x = generator.uniform(-1.0, 1.0, SAMPLE_COUNT)
    y = generator.uniform(-1.0, 1.0, SAMPLE_COUNT)
    z = generator.uniform(-1.0, 1.0, SAMPLE_COUNT)
    inside = support.quadratic_form_array(x, y, z) <= 1.0
    fraction = float(np.mean(inside))
    volume_sample = 8.0 * fraction
    volume_error = 8.0 * math.sqrt(fraction * (1.0 - fraction) / SAMPLE_COUNT)
    ledger.add("volume_against_sample", volume_sample, volume_closed,
               support.MONTE_CARLO_STANDARD_ERROR_FACTOR * volume_error)

    point = anchors.section_quarter_point()
    ledger.add("section_quarter_point_residual", support.boundary_residual(point), 0.0, 1.0e-12)
    ledger.add("surface_label_point_residual",
               support.boundary_residual((*anchors.SURFACE_LABEL_POINT,
                                          anchors.surface_label_height())), 0.0, 1.0e-12)

    print(f"the semi-axes of P are {first!r}, {second!r}, and {third!r}")
    print(f"the volume of P is {volume_closed!r} from the closed form and"
          f" {volume_sections!r} from the sections")
    print(f"the sampled volume is {volume_sample!r} with error {volume_error!r}")
    print(f"the drawn section has semi-axes {anchors.section_semi_axes()!r}")

    support.write_results(OUTPUT_PATH, {
        "semi_axis_x": first,
        "semi_axis_y": second,
        "semi_axis_z": third,
        "ellipsoid_volume": volume_closed,
        "volume_from_sections": volume_sections,
        "volume_sample": volume_sample,
        "volume_sample_error": volume_error,
        "section_rows": rows,
        "section_quarter_point": list(point),
        "checks": ledger.summary(),
    })
    print(f"wrote {OUTPUT_PATH} with {ledger.summary()['count']} checks")


if __name__ == "__main__":
    main()
