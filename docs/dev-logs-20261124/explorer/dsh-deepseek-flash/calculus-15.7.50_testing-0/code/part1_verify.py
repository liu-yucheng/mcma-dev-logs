"""Verify the geometry of the solid E of Problem 25.

The script derives every bound from the four surfaces, then checks the volume, the projection on the
plane x = 0, the section at a fixed y, and the shape of that section at three heights. Each check
compares a value from one method with a value from a different method.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors
import verification_support as support

OUTPUT_PATH = Path(__file__).resolve().parent / "outputs" / "part1_results.json"


def cumulative_volume(y_upper: float) -> float:
    """Return the volume of the part of E with y in the interval from 0 to y_upper."""
    section = lambda y: integrate.quad(  # noqa: E731
        lambda z: support.x_upper(y), 0.0, support.cylinder_height(y),
        epsabs=support.QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=support.QUADRATURE_RELATIVE_TOLERANCE)[0]
    return integrate.quad(
        section, 0.0, y_upper,
        epsabs=support.QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=support.QUADRATURE_RELATIVE_TOLERANCE)[0]


def section_area_by_difference(y: float, step: float = 1.0e-4) -> float:
    """Return the section area at y as a central difference of the cumulative volume."""
    return (cumulative_volume(y + step) - cumulative_volume(y - step)) / (2.0 * step)


def projection_area_by_quadrature() -> float:
    """Return the area of the projection of E on the plane x = 0."""
    return integrate.quad(
        support.cylinder_height, 0.0, support.BOX_Y_UPPER,
        epsabs=support.QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=support.QUADRATURE_RELATIVE_TOLERANCE)[0]


def projection_area_by_simpson(point_count: int) -> float:
    """Return the projection area on the plane x = 0 by Simpson in the variable y = 3 sin t."""
    grid = np.linspace(0.0, math.pi / 2.0, point_count)
    values = 9.0 * np.cos(grid) ** 2
    return float(integrate.simpson(values, x=grid))


def projection_area_by_monte_carlo(sample_count: int, seed: int) -> tuple[float, float]:
    """Return the projection area on the plane x = 0 from uniform samples in the yz box."""
    generator = np.random.default_rng(seed)
    y = generator.uniform(0.0, support.BOX_Y_UPPER, sample_count)
    z = generator.uniform(0.0, support.BOX_Z_UPPER, sample_count)
    inside = y * y + z * z <= 9.0
    box_area = support.BOX_Y_UPPER * support.BOX_Z_UPPER
    estimate = box_area * float(np.mean(inside))
    error = box_area * float(np.std(inside.astype(float), ddof=1)) / math.sqrt(sample_count)
    return estimate, error


def main() -> None:
    """Run every check of Part 1 and write the JSON result file."""
    print("PART 1: the solid E from the four surfaces")
    print(f"inequalities: 0 <= y <= 3, 0 <= z <= sqrt(9 - y^2), 0 <= x <= y / 3")
    ledger = support.CheckLedger("part1")
    samples = figure_anchors.MONTE_CARLO_SAMPLE_COUNT
    seed = figure_anchors.MONTE_CARLO_SEED

    volume_primary = support.integrate_dx_dz_dy(lambda x, y, z: 1.0)
    volume_alternate = support.integrate_dz_dy_dx(lambda x, y, z: 1.0)
    volume_monte_carlo, volume_error = support.monte_carlo(lambda x, y, z: 1.0, samples, seed)
    print(f"volume by dx dz dy = {volume_primary:.12f}")
    print(f"volume by dz dy dx = {volume_alternate:.12f}")
    print(f"volume by Monte Carlo = {volume_monte_carlo:.12f} +- {volume_error:.12f}")
    ledger.add("volume: two integration orders",
               volume_primary, volume_alternate, 1.0e-9)
    ledger.add("volume: quadrature against Monte Carlo",
               volume_primary, volume_monte_carlo,
               support.MONTE_CARLO_STANDARD_ERROR_FACTOR * volume_error)

    projection_quadrature = projection_area_by_quadrature()
    projection_closed_form = 9.0 * math.pi / 4.0
    projection_monte_carlo, projection_error = projection_area_by_monte_carlo(samples, seed + 1)
    print(f"projection area on x = 0 by quadrature = {projection_quadrature:.12f}")
    print(f"projection area on x = 0 by (9 pi / 4) = {projection_closed_form:.12f}")
    print(f"projection area on x = 0 by Monte Carlo = {projection_monte_carlo:.12f}"
          f" +- {projection_error:.12f}")
    projection_simpson = projection_area_by_simpson(2401)
    print(f"projection area on x = 0 by Simpson on a grid = {projection_simpson:.12f}")
    ledger.add("projection on x = 0: quadrature against Simpson on a grid",
               projection_quadrature, projection_simpson, 1.0e-9)
    ledger.add("projection on x = 0: closed form against Monte Carlo",
               projection_closed_form, projection_monte_carlo,
               support.MONTE_CARLO_STANDARD_ERROR_FACTOR * projection_error)

    y = figure_anchors.SECTION_Y
    width = support.x_upper(y)
    height = support.cylinder_height(y)
    area_product = width * height
    area_difference = section_area_by_difference(y)
    print(f"section at y = {y}: width = {width:.12f}, height = {height:.12f}")
    print(f"section area by width times height = {area_product:.12f}")
    print(f"section area by the difference of the cumulative volume = {area_difference:.12f}")
    ledger.add("section area at y = 1.5: product against the volume difference",
               area_product, area_difference, 1.0e-6)

    print("corners of the section at three values of y")
    shape_rows = []
    for y_value in (0.0, y, 3.0):
        corners = support.section_corners(y_value)
        kept = support.distinct_corners(y_value)
        shape_by_count = support.section_shape_from_distinct_corners(y_value)
        shape_by_edges = support.section_shape_from_edge_lengths(y_value)
        print(f"  y = {y_value:.1f}: four written corners")
        for corner in corners:
            print(f"    ({corner[0]:.6f}, {corner[1]:.6f}, {corner[2]:.6f})")
        print(f"    distinct corners = {len(kept)}")
        print(f"    shape from the distinct corner count = {shape_by_count}")
        print(f"    shape from the edge lengths = {shape_by_edges}")
        ledger.add_text(f"section shape at y = {y_value:.1f}",
                        shape_by_count, shape_by_edges)
        shape_rows.append({
            "y": f"{y_value:.1f}",
            "width": f"{support.x_upper(y_value):.6f}",
            "height": f"{support.cylinder_height(y_value):.6f}",
            "distinct_corners": str(len(kept)),
            "shape": shape_by_count,
            "area": f"{support.x_upper(y_value) * support.cylinder_height(y_value):.6f}",
        })

    anchors = []
    for surface, (point, offset) in figure_anchors.SURFACE_LABEL_ANCHORS.items():
        residual = figure_anchors.label_residual(surface, point)
        inside = (
            point[0] >= 0.0
            and 3.0 * point[0] <= point[1] + support.GEOMETRY_TOLERANCE
            and point[1] * point[1] + point[2] * point[2] <= 9.0 + support.GEOMETRY_TOLERANCE
        )
        print(f"label anchor {surface}: ({point[0]:.4f}, {point[1]:.4f}, {point[2]:.4f})"
              f" residual = {residual:.3e}")
        ledger.add(f"label anchor {surface} satisfies its surface", residual, 0.0, 1.0e-12)
        anchors.append({
            "surface": surface,
            "point": [f"{value:.4f}" for value in point],
            "offset": [f"{value:.4f}" for value in offset],
            "residual": f"{residual:.3e}",
            "inside": str(inside),
        })

    results = {
        "volume": f"{volume_primary:.6f}",
        "volume_alternate": f"{volume_alternate:.6f}",
        "volume_relative_difference": f"{abs(volume_primary - volume_alternate) / abs(volume_primary):.2e}",
        "volume_relative_difference_latex": support.scientific_latex(
            abs(volume_primary - volume_alternate) / abs(volume_primary)),
        "volume_relative_difference_denominator": f"{int(round(1.0 / (abs(volume_primary - volume_alternate) / abs(volume_primary)))):.0f}",
        "volume_monte_carlo": f"{volume_monte_carlo:.6f}",
        "volume_monte_carlo_error": f"{volume_error:.6f}",
        "projection_area": f"{projection_quadrature:.6f}",
        "projection_area_closed_form": f"{projection_closed_form:.6f}",
        "section_y": f"{y:.6f}",
        "section_width": f"{width:.6f}",
        "section_height": f"{height:.6f}",
        "section_area": f"{area_product:.6f}",
        "section_area_difference": f"{area_difference:.6f}",
        "shape_rows": shape_rows,
        "anchors": anchors,
        "checks": ledger.summary(),
    }
    support.write_results(OUTPUT_PATH, results)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
