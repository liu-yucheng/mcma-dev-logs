"""Verify Part 1: the inequalities of E, the vertices, the three orders, and the sections.

The script checks the region description in four independent ways. It solves for the vertices
from the defining surfaces. It computes the volume with three different orders of integration,
with one numerical quadrature, and with one Monte Carlo sample. It computes the area of the
section at a fixed x with a formula, with the shoelace formula, and with a midpoint grid. It
computes the area of the section at a fixed z with a closed form, with one quadrature, and with a
midpoint grid. The script writes `code/results/part1_results.json`.
"""

from __future__ import annotations

import math

import numpy as np
import sympy

import common_region as region

X, Y, Z = sympy.symbols("x y z")
"""Symbols of the Cartesian coordinates."""


def volume_in_three_orders() -> tuple[sympy.Expr, sympy.Expr, sympy.Expr]:
    """Return the volume of E in the orders dz dy dx, dy dz dx, and dx dz dy."""
    inner_first = sympy.integrate(1, (Z, 0, Y), (Y, 0, sympy.sqrt(1 - X**2)), (X, 0, 1))
    inner_first = sympy.simplify(inner_first)
    inner_second = sympy.integrate(1, (Y, Z, sympy.sqrt(1 - X**2)), (Z, 0, sympy.sqrt(1 - X**2)), (X, 0, 1))
    inner_second = sympy.simplify(inner_second)
    inner_third = sympy.integrate(1, (X, 0, sympy.sqrt(1 - Y**2)), (Z, 0, Y), (Y, 0, 1))
    inner_third = sympy.simplify(inner_third)
    return inner_first, inner_second, inner_third


def vertices_from_surfaces() -> list[tuple[float, float, float]]:
    """Return the vertices of E, solved from each triple of defining surfaces.

    A triple of surfaces meets at a vertex when the meeting point lies in the closure of E.
    The function keeps the points with x >= 0, y >= 0, z >= 0, x^2 + y^2 <= 1, and z <= y.
    """
    surfaces = [
        X**2 + Y**2 - 1,
        Y - Z,
        X,
        Z,
    ]
    found: set[tuple[float, float, float]] = set()
    for first in range(len(surfaces)):
        for second in range(first + 1, len(surfaces)):
            for third in range(second + 1, len(surfaces)):
                solution_set = sympy.solve(
                    [surfaces[first], surfaces[second], surfaces[third]], [X, Y, Z], dict=True
                )
                for solution in solution_set:
                    if not all(value.is_real for value in solution.values()):
                        continue
                    x_value = float(solution[X])
                    y_value = float(solution[Y])
                    z_value = float(solution[Z])
                    inside = (
                        x_value >= -1e-9
                        and y_value >= -1e-9
                        and z_value >= -1e-9
                        and x_value**2 + y_value**2 <= 1 + 1e-9
                        and z_value <= y_value + 1e-9
                    )
                    if inside:
                        found.add((round(x_value, 9), round(y_value, 9), round(z_value, 9)))
    return sorted(found)


def limit_check() -> dict[str, int]:
    """Count the points where an order of integration disagrees with the inequalities.

    The function samples the unit cube. For each order it decides membership from the limits of
    that order alone, and it compares the decision with the four defining inequalities.
    """
    generator = np.random.default_rng(region.RANDOM_SEED + 1)
    sample_count = 400_000
    x_values = generator.random(sample_count)
    y_values = generator.random(sample_count)
    z_values = generator.random(sample_count)
    inside = region.membership_mask(x_values, y_values, z_values)
    outer = np.sqrt(np.maximum(0.0, 1.0 - x_values**2))
    order_first = (
        (x_values >= 0.0)
        & (x_values <= 1.0)
        & (y_values >= 0.0)
        & (y_values <= outer)
        & (z_values >= 0.0)
        & (z_values <= y_values)
    )
    order_second = (
        (x_values >= 0.0)
        & (x_values <= 1.0)
        & (z_values >= 0.0)
        & (z_values <= outer)
        & (y_values >= z_values)
        & (y_values <= outer)
    )
    order_third = (
        (y_values >= 0.0)
        & (y_values <= 1.0)
        & (z_values >= 0.0)
        & (z_values <= y_values)
        & (x_values >= 0.0)
        & (x_values <= np.sqrt(np.maximum(0.0, 1.0 - y_values**2)))
    )
    return {
        "dz_dy_dx": int(np.count_nonzero(order_first != inside)),
        "dy_dz_dx": int(np.count_nonzero(order_second != inside)),
        "dx_dz_dy": int(np.count_nonzero(order_third != inside)),
        "sample_count": sample_count,
    }


def main() -> None:
    """Run every check of Part 1 and write the result record."""
    checks: list[dict[str, object]] = []
    tables: list[dict[str, object]] = []

    exact_first, exact_second, exact_third = volume_in_three_orders()
    print(f"[exact] volume in the order dz dy dx = {exact_first}")
    print(f"[exact] volume in the order dy dz dx = {exact_second}")
    print(f"[exact] volume in the order dx dz dy = {exact_third}")
    checks.append(region.check_close("volume, order dz dy dx against 1/3", float(exact_first), 1.0 / 3.0, 1e-15))
    checks.append(region.check_close("volume, order dy dz dx against order dz dy dx", float(exact_second), float(exact_first), 1e-15))
    checks.append(region.check_close("volume, order dx dz dy against order dz dy dx", float(exact_third), float(exact_first), 1e-15))

    numeric_volume, numeric_error = region.integrate_with_nquad(
        lambda x_value, y_value, z_value: 1.0, order="z_y_x"
    )
    checks.append(region.check_close("volume, one numerical quadrature against 1/3", numeric_volume, 1.0 / 3.0, 1e-10))
    numeric_second, numeric_second_error = region.integrate_with_nquad(
        lambda x_value, y_value, z_value: 1.0, order="y_z_x"
    )
    checks.append(
        region.check_close(
            "volume, quadrature in the order dy dz dx against quadrature in the order dz dy dx",
            numeric_second,
            numeric_volume,
            1e-10,
        )
    )
    numeric_third, numeric_third_error = region.integrate_with_nquad(
        lambda x_value, y_value, z_value: 1.0, order="x_z_y"
    )
    checks.append(
        region.check_close(
            "volume, quadrature in the order dx dz dy against quadrature in the order dz dy dx",
            numeric_third,
            numeric_volume,
            1e-10,
        )
    )

    monte_carlo_volume, monte_carlo_error = region.monte_carlo_integral(
        region.masked_integrand(lambda x_values, y_values, z_values: np.ones_like(x_values))
    )
    four_errors = 4.0 * monte_carlo_error
    print(
        f"[monte-carlo] volume={monte_carlo_volume:.6f} standard_error={monte_carlo_error:.6f} "
        f"four_standard_errors={four_errors:.6f}"
    )
    checks.append(region.check_close("volume, Monte Carlo against 1/3 within four standard errors", monte_carlo_volume, 1.0 / 3.0, four_errors))

    corners = vertices_from_surfaces()
    claimed_corners = [(0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 1.0), (1.0, 0.0, 0.0)]
    print(f"[vertices] solved from the surfaces: {corners}")
    print(f"[vertices] claimed: {claimed_corners}")
    assert corners == claimed_corners, f"the solved vertices {corners} differ from the claimed {claimed_corners}"
    print("[check] the solved vertex list equals the claimed vertex list")

    limits = limit_check()
    print(f"[limits] disagreements of the three orders with the inequalities: {limits}")
    for name, count in limits.items():
        if name == "sample_count":
            continue
        assert count == 0, f"the order {name} disagrees with the inequalities at {count} points"
        print(f"[check] order {name}: 0 disagreements in {limits['sample_count']} samples")

    rows_fixed_x: list[list[str]] = []
    for x_value in (0.0, 0.4, 0.8, 1.0):
        outer = region.outer_radius(x_value)
        vertices = region.triangle_vertices(outer)
        formula_area = outer**2 / 2.0
        shoelace_area = region.polygon_area(vertices)
        grid_area = region.triangle_grid_integral(outer, lambda y_grid, z_grid: np.ones_like(y_grid))
        if len(vertices) == 1:
            shape = "one point"
        else:
            shape = "a triangle"
        checks.append(region.check_close(f"section area at x={x_value:.1f}, shoelace against Y^2/2", shoelace_area, formula_area, 1e-12))
        checks.append(region.check_close(f"section area at x={x_value:.1f}, grid against Y^2/2", grid_area, formula_area, 3e-3))
        print(f"[section] x={x_value:.1f} outer_radius={outer:.6f} vertices={vertices} shape={shape}")
        rows_fixed_x.append(
            [
                region.decimal(x_value, 1),
                region.decimal(outer, 6),
                "; ".join(f"({first:.3f}, {second:.3f})" for first, second in vertices),
                region.decimal(formula_area, 6),
                region.decimal(shoelace_area, 6),
                region.decimal(grid_area, 6),
                shape,
            ]
        )
    tables.append(
        {
            "caption": "The section of E at a fixed x, and its area by three methods",
            "columns": [
                "$x$",
                "$Y=\\sqrt{1-x^{2}}$",
                "vertices $(y,z)$",
                "$Y^{2}/2$",
                "shoelace",
                "midpoint grid",
                "shape",
            ],
            "rows": rows_fixed_x,
        }
    )

    slice_expression = sympy.integrate(sympy.sqrt(1 - Y**2), (Y, Z, 1))
    slice_expression = sympy.simplify(slice_expression)
    print(f"[exact] area of the section at a fixed z = {slice_expression}")
    slice_function = sympy.lambdify(Z, slice_expression, "math")
    rows_fixed_z: list[list[str]] = []
    for z_value in (0.0, 0.5, 0.9, 1.0):
        closed_form = float(slice_function(z_value))
        quad_area = region.slice_area_quad(z_value)
        grid_area = region.slice_grid_area(z_value)
        if closed_form <= 1e-12:
            shape = "one point"
        else:
            shape = "a quarter-disk cut by the line $y=z$"
        checks.append(region.check_close(f"section area at z={z_value:.1f}, quadrature against the closed form", quad_area, closed_form, 1e-10))
        checks.append(region.check_close(f"section area at z={z_value:.1f}, grid against the closed form", grid_area, closed_form, 3e-3))
        rows_fixed_z.append(
            [
                region.decimal(z_value, 1),
                region.decimal(closed_form, 6),
                region.decimal(quad_area, 6),
                region.decimal(grid_area, 6),
                shape,
            ]
        )
    checks.append(region.check_close("section area at z=0 against pi/4", float(slice_function(0.0)), math.pi / 4.0, 1e-12))
    tables.append(
        {
            "caption": "The section of E at a fixed z, and its area by three methods",
            "columns": ["$z$", "closed form", "quadrature", "midpoint grid", "shape"],
            "rows": rows_fixed_z,
        }
    )

    volume_from_sections = sympy.integrate((1 - X**2) / 2, (X, 0, 1))
    volume_from_sections = sympy.simplify(volume_from_sections)
    volume_from_slices = sympy.integrate(slice_expression, (Z, 0, 1))
    volume_from_slices = sympy.simplify(volume_from_slices)
    print(f"[exact] volume from the sections at a fixed x = {volume_from_sections}")
    print(f"[exact] volume from the sections at a fixed z = {volume_from_slices}")
    checks.append(region.check_close("volume from the sections at a fixed x against 1/3", float(volume_from_sections), 1.0 / 3.0, 1e-15))
    checks.append(region.check_close("volume from the sections at a fixed z against 1/3", float(volume_from_slices), 1.0 / 3.0, 1e-15))

    largest_difference = max(float(record["difference"]) for record in checks)
    payload = {
        "part": 1,
        "title": "The region E, its vertices, and the order of integration",
        "checks": checks,
        "tables": tables,
        "facts": {
            "volume_exact": str(exact_first),
            "volume_decimal": region.decimal(float(exact_first), 6),
            "vertices": [list(corner) for corner in corners],
            "monte_carlo_volume": monte_carlo_volume,
            "monte_carlo_standard_error": monte_carlo_error,
            "largest_difference": largest_difference,
            "check_count": len(checks),
        },
    }
    region.write_result(1, payload)
    print(f"[summary] {len(checks)} checks, largest difference {largest_difference:.3e}")


if __name__ == "__main__":
    main()
