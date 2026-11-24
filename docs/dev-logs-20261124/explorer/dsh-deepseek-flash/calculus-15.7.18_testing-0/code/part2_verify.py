"""Verify the nested bounds of Part 2 for six orders of integration.

Method one is the four defining inequalities of the solid.
Method two is the nested limit list of one order.
The script compares the two descriptions point by point, and it compares the volume that each
order integrates with the volume of Part 1.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy import integrate

from check_registry import CheckRegistry, write_values
from geometry_anchors import CYLINDER_RADIUS, DEMO_HEIGHT_Y, PLANE_SLOPE, RANDOM_SEED
from limit_expression import (
    ConstantLimit,
    LinearMultiple,
    LinearShare,
    QuotientLimit,
    ScaledLimit,
    SqrtRemainder,
)

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"
"""Directory that holds the JSON record of every part."""

MEMBERSHIP_TOLERANCE = 1.0e-12
"""Slack of the membership test of one description."""

BOUNDARY_BAND = 1.0e-9
"""Width of the band around a boundary surface in which the two descriptions may differ."""

LATTICE_SIDE = 61
"""Number of sample points on each side of the deterministic lattice."""

RANDOM_SAMPLE_COUNT = 400_000
"""Number of random points of the membership test."""

DEPENDENCE_STEP = 0.05
"""Change of one coordinate that the dependence probe applies."""

PROBE_POINT = {"x": 0.30, "y": 1.20, "z": 1.00}
"""One interior point at which the dependence probe evaluates every bound."""


def build_order_specs() -> list[dict[str, object]]:
    """Return the six orders of integration with their three nested bound pairs."""
    radius = CYLINDER_RADIUS
    slope = PLANE_SLOPE
    zero = ConstantLimit(0.0)
    three = ConstantLimit(radius)
    one = ConstantLimit(1.0)
    return [
        {
            "name": "dz dx dy",
            "variables": ("z", "x", "y"),
            "outer_range": (zero, three),
            "middle_range": (zero, LinearShare("y", slope)),
            "inner_range": (zero, SqrtRemainder(radius**2, "y")),
        },
        {
            "name": "dx dz dy",
            "variables": ("x", "z", "y"),
            "outer_range": (zero, three),
            "middle_range": (zero, SqrtRemainder(radius**2, "y")),
            "inner_range": (zero, LinearShare("y", slope)),
        },
        {
            "name": "dx dy dz",
            "variables": ("x", "y", "z"),
            "outer_range": (zero, three),
            "middle_range": (zero, SqrtRemainder(radius**2, "z")),
            "inner_range": (zero, LinearShare("y", slope)),
        },
        {
            "name": "dy dx dz",
            "variables": ("y", "x", "z"),
            "outer_range": (zero, three),
            "middle_range": (zero, QuotientLimit(SqrtRemainder(radius**2, "z"), slope)),
            "inner_range": (LinearMultiple(slope, "x"), SqrtRemainder(radius**2, "z")),
        },
        {
            "name": "dy dz dx",
            "variables": ("y", "z", "x"),
            "outer_range": (zero, one),
            "middle_range": (zero, ScaledLimit(slope, SqrtRemainder(1.0, "x"))),
            "inner_range": (LinearMultiple(slope, "x"), SqrtRemainder(radius**2, "z")),
        },
        {
            "name": "dz dy dx",
            "variables": ("z", "y", "x"),
            "outer_range": (zero, one),
            "middle_range": (LinearMultiple(slope, "x"), three),
            "inner_range": (zero, SqrtRemainder(radius**2, "y")),
        },
    ]


def inside_by_limits(
    spec: dict[str, object],
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    tolerance: float = MEMBERSHIP_TOLERANCE,
) -> np.ndarray:
    """Return a mask that is true where the point satisfies the nested limits of one order.

    Args:
        spec: One order of integration.
        x: Array of the first coordinate.
        y: Array of the second coordinate.
        z: Array of the third coordinate.
        tolerance: Slack of each comparison.
    """
    values = {"x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float), "z": np.asarray(z, dtype=float)}
    inner, middle, outer = spec["variables"]
    mask = np.ones(np.shape(values["x"]), dtype=bool)
    for variable, pair in (
        (outer, spec["outer_range"]),
        (middle, spec["middle_range"]),
        (inner, spec["inner_range"]),
    ):
        lower, upper = pair
        mask &= values[variable] >= lower.evaluate(values) - tolerance
        mask &= values[variable] <= upper.evaluate(values) + tolerance
    return mask


def inside_by_inequalities(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return a mask that is true where the point satisfies the four defining inequalities.

    Args:
        x: Array of the first coordinate.
        y: Array of the second coordinate.
        z: Array of the third coordinate.
    """
    return (
        (y * y + z * z <= CYLINDER_RADIUS**2 + MEMBERSHIP_TOLERANCE)
        & (x >= -MEMBERSHIP_TOLERANCE)
        & (y >= PLANE_SLOPE * x - MEMBERSHIP_TOLERANCE)
        & (z >= -MEMBERSHIP_TOLERANCE)
    )


def boundary_slack(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return the smallest distance-like slack of the four defining inequalities.

    Args:
        x: Array of the first coordinate.
        y: Array of the second coordinate.
        z: Array of the third coordinate.
    """
    return np.minimum.reduce(
        [
            CYLINDER_RADIUS**2 - y * y - z * z,
            np.abs(x),
            np.abs(y - PLANE_SLOPE * x),
            np.abs(z),
        ]
    )


def bound_value(bound: object, named_values: dict[str, float]) -> float:
    """Return the value of one bound at one point.

    Args:
        bound: Limit expression to evaluate.
        named_values: Coordinate values of the point.
    """
    arrays = {name: np.asarray(value, dtype=float) for name, value in named_values.items()}
    return float(np.asarray(bound.evaluate(arrays)))


def volume_by_nquad(spec: dict[str, object]) -> float:
    """Return the volume of the solid by nested adaptive quadrature in one order.

    Args:
        spec: One order of integration.
    """
    inner, middle, outer = spec["variables"]
    inner_lower, inner_upper = spec["inner_range"]
    middle_lower, middle_upper = spec["middle_range"]
    outer_lower, outer_upper = spec["outer_range"]
    quad_options = {"epsabs": 1.0e-11, "epsrel": 1.0e-11, "limit": 400}

    def section_area(outer_value: float) -> float:
        """Return the area of the section at one value of the outer variable."""
        outer_point = dict(PROBE_POINT)
        outer_point[outer] = outer_value
        middle_low = bound_value(middle_lower, outer_point)
        middle_high = bound_value(middle_upper, outer_point)

        def inner_width(middle_value: float) -> float:
            """Return the length of the inner segment at one value of the middle variable."""
            named = dict(outer_point)
            named[middle] = middle_value
            return bound_value(inner_upper, named) - bound_value(inner_lower, named)

        return float(integrate.quad(inner_width, middle_low, middle_high, **quad_options)[0])

    outer_low = bound_value(outer_lower, PROBE_POINT)
    outer_high = bound_value(outer_upper, PROBE_POINT)
    return float(integrate.quad(section_area, outer_low, outer_high, **quad_options)[0])


def probe_dependence(bound: object, name: str, registry: CheckRegistry) -> dict[str, bool]:
    """Check which coordinates a bound depends on, and that the declared set is the true set.

    Args:
        bound: Limit expression to probe.
        name: Label of the bound, used in the check names.
        registry: Registry that records the checks.
    """
    observed: dict[str, bool] = {}
    for coordinate in ("x", "y", "z"):
        base = dict(PROBE_POINT)
        shifted = dict(PROBE_POINT)
        shifted[coordinate] = shifted[coordinate] + DEPENDENCE_STEP
        change = abs(bound_value(bound, base) - bound_value(bound, shifted))
        observed[coordinate] = change > 1.0e-9
    declared = {coordinate: coordinate in bound.variables for coordinate in ("x", "y", "z")}
    if observed != declared:
        raise AssertionError(f"bound {name} declares {declared} but the probe observes {observed}")
    registry.compare_absolute(
        f"part2.dependence_{name}",
        float(sum(observed.values())),
        float(len(bound.variables)),
        0.0,
        "Number of coordinates that the probe observes in the bound against the declared count.",
    )
    return observed


def main() -> None:
    """Run every check of Part 2 and write the values of the part."""
    registry = CheckRegistry("part2")
    values: dict[str, object] = {}
    volume_reference = CYLINDER_RADIUS**3 / (3.0 * PLANE_SLOPE)
    specs = build_order_specs()

    lattice_axis = [np.linspace(0.0, 1.0, LATTICE_SIDE), np.linspace(0.0, CYLINDER_RADIUS, LATTICE_SIDE)]
    grid_x, grid_y, grid_z = np.meshgrid(lattice_axis[0], lattice_axis[1], lattice_axis[1], indexing="ij")
    generator = np.random.default_rng(RANDOM_SEED)
    random_x = generator.uniform(0.0, 1.0, RANDOM_SAMPLE_COUNT)
    random_y = generator.uniform(0.0, CYLINDER_RADIUS, RANDOM_SAMPLE_COUNT)
    random_z = generator.uniform(0.0, CYLINDER_RADIUS, RANDOM_SAMPLE_COUNT)
    sample_x = np.concatenate([grid_x.ravel(), random_x])
    sample_y = np.concatenate([grid_y.ravel(), random_y])
    sample_z = np.concatenate([grid_z.ravel(), random_z])
    keep = boundary_slack(sample_x, sample_y, sample_z) > BOUNDARY_BAND
    sample_x, sample_y, sample_z = sample_x[keep], sample_y[keep], sample_z[keep]
    inequality_mask = inside_by_inequalities(sample_x, sample_y, sample_z)

    order_rows: list[dict[str, object]] = []
    dependence_rows: list[dict[str, str]] = []
    for spec in specs:
        limit_mask = inside_by_limits(spec, sample_x, sample_y, sample_z)
        disagreements = int(np.count_nonzero(limit_mask != inequality_mask))
        registry.compare_absolute(
            f"part2.membership_{spec['name'].replace(' ', '_')}",
            float(disagreements),
            0.0,
            0.5,
            "Number of sampled points where the nested limits and the inequalities disagree against zero.",
        )
        inner, middle, outer = spec["variables"]
        for bound, label in (
            (spec["outer_range"][0], "outer_lower"),
            (spec["outer_range"][1], "outer_upper"),
            (spec["middle_range"][0], "middle_lower"),
            (spec["middle_range"][1], "middle_upper"),
            (spec["inner_range"][0], "inner_lower"),
            (spec["inner_range"][1], "inner_upper"),
        ):
            observed = probe_dependence(bound, f"{spec['name'].replace(' ', '_')}_{label}", registry)
            if label.endswith("upper") or label.endswith("lower"):
                dependence_rows.append(
                    {
                        "order": str(spec["name"]),
                        "bound": label,
                        "latex": bound.latex,
                        "depends_on": ", ".join(name for name, flag in observed.items() if flag) or "none",
                    }
                )
        volume = volume_by_nquad(spec)
        registry.compare(
            f"part2.volume_{spec['name'].replace(' ', '_')}",
            volume,
            volume_reference,
            1.0e-7,
            "Nested quadrature in this order against the volume that Part 1 computes from the two slicings.",
        )
        order_rows.append(
            {
                "order": str(spec["name"]),
                "outer": f"{spec['outer_range'][0].latex} \\le {outer} \\le {spec['outer_range'][1].latex}",
                "middle": f"{spec['middle_range'][0].latex} \\le {middle} \\le {spec['middle_range'][1].latex}",
                "inner": f"{spec['inner_range'][0].latex} \\le {inner} \\le {spec['inner_range'][1].latex}",
                "volume": f"{volume:.9f}",
            }
        )
        print(f"order {spec['name']}: volume={volume:.12f} disagreements={disagreements}")

    chosen = specs[0]
    demo = dict(PROBE_POINT)
    demo["y"] = DEMO_HEIGHT_Y
    chosen_demo = {
        "y": DEMO_HEIGHT_Y,
        "x_high": bound_value(chosen["middle_range"][1], demo),
        "z_high": bound_value(chosen["inner_range"][1], demo),
    }
    registry.compare(
        "part2.demo_x_width",
        chosen_demo["x_high"],
        DEMO_HEIGHT_Y / PLANE_SLOPE,
        1.0e-12,
        "Bound value at the demo height against the quotient of that height by the slope.",
    )
    registry.compare(
        "part2.demo_z_height",
        chosen_demo["z_high"],
        math.sqrt(CYLINDER_RADIUS**2 - DEMO_HEIGHT_Y**2),
        1.0e-12,
        "Bound value at the demo height against the square root of the remainder of the cylinder equation.",
    )

    inner_depends_on = [row for row in dependence_rows if row["order"] == "dz dx dy" and row["bound"] == "inner_upper"]
    registry.compare_absolute(
        "part2.chosen_inner_upper_count",
        float(len(inner_depends_on)),
        1.0,
        0.0,
        "One row must describe the inner upper limit of the chosen order.",
    )
    chosen_inner_dependence = inner_depends_on[0]["depends_on"]

    registry.write(OUTPUT_DIRECTORY / "part2_checks.json")
    values.update(
        {
            "p2_order_rows": order_rows,
            "p2_chosen_order": "dz dx dy",
            "p2_dependence_rows": [
                row for row in dependence_rows if row["order"] in ("dz dx dy", "dy dx dz")
            ],
            "p2_chosen_inner_dependence": chosen_inner_dependence,
            "p2_demo_height": f"{DEMO_HEIGHT_Y:.3f}",
            "p2_demo_x_high": f"{chosen_demo['x_high']:.9f}",
            "p2_demo_z_high": f"{chosen_demo['z_high']:.9f}",
            "p2_volume": f"{volume_reference:.9f}",
            "p2_check_count": str(registry.passed_count()),
            "p2_membership_sample_count": str(int(sample_x.size)),
        }
    )
    write_values(OUTPUT_DIRECTORY / "part2_values.json", values)


if __name__ == "__main__":
    main()
