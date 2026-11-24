"""Verify the enumeration of the six integration orders from one bound rule.

The solid E has a special structure.  Two of its surfaces, x = -2 and x = 2, fix the coordinate x
between two constants.  The third surface, y^2 + z^2 = 9, fixes y and z only against each other.
One bound rule follows from this structure:

    the bounds of x are always -2 and 2;
    the bounds of y are -3 and 3, or the two halves of the cylinder at the fixed value of z;
    the bounds of z are -3 and 3, or the two halves of the cylinder at the fixed value of y.

A choice of one variable for each of the three levels, with no variable used twice, is a
permutation of the three names.  This script counts the permutations, builds the six limit sets
from the rule alone, and checks three claims.

1.  There are 3! = 6 permutations, counted by three separate methods.
2.  Each limit set built from the rule accepts exactly the points of E that the defining
    inequalities accept, and it rejects the points of the bounding box that lie outside E.
3.  Each limit set gives 36*pi for f = 1, and the value agrees with the value that the
    hand-written script of Part 3, Part 4, or Part 5 reports.

Run this script with the interpreter of `code/.venv`.  It writes
`code/results/part6_results.json`.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy import integrate

RADIUS = 3.0
"""Radius of the circular cylinder y^2 + z^2 = 9."""

HALF_LENGTH = 2.0
"""Half of the distance between the planes x = -2 and x = 2."""

CYLINDER_LENGTH = 2.0 * HALF_LENGTH
"""Distance between the two planes x = -2 and x = 2."""

EXACT_VOLUME = math.pi * RADIUS**2 * CYLINDER_LENGTH
"""Volume of E, thus 36*pi."""

RANDOM_SEED = 20261122
"""Seed of the random sample of the discrimination test."""

SAMPLE_COUNT = 20000
"""Number of random points of the discrimination test."""

COORDINATE_NAMES = ("x", "y", "z")
"""Names of the three coordinates."""

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "part6_results.json"
"""Path of the machine-readable record of the checks."""


def bounds_of(variable: str, fixed: dict[str, float]) -> tuple[float, float]:
    """Return the two bounds of one variable from the bound rule.

    Args:
        variable: Name of the variable.
        fixed: Values of the variables that an outer level already fixed.

    Returns:
        The lower bound and the upper bound.
    """
    if variable == "x":
        return (-HALF_LENGTH, HALF_LENGTH)
    if variable == "y":
        if "z" in fixed:
            half_width = math.sqrt(max(RADIUS**2 - fixed["z"] ** 2, 0.0))
            return (-half_width, half_width)
        return (-RADIUS, RADIUS)
    if "y" in fixed:
        half_width = math.sqrt(max(RADIUS**2 - fixed["y"] ** 2, 0.0))
        return (-half_width, half_width)
    return (-RADIUS, RADIUS)


def point_is_inside_limits(spec: tuple[str, str, str], point: dict[str, float],
                           tolerance: float = 1e-12) -> bool:
    """Return True when the point satisfies every bound of the nested limit set.

    Args:
        spec: The three variable names, from the outer level to the inner level.
        point: The point, with one value for each coordinate.
        tolerance: Largest accepted violation of a bound.

    Returns:
        True when the point satisfies the limit set.
    """
    fixed: dict[str, float] = {}
    for variable in spec:
        low, high = bounds_of(variable, fixed)
        if point[variable] < low - tolerance or point[variable] > high + tolerance:
            return False
        fixed[variable] = point[variable]
    return True


def point_is_inside_solid(point: dict[str, float], tolerance: float = 1e-12) -> bool:
    """Return True when the point satisfies the defining inequalities of E."""
    inside_box = (abs(point["x"]) <= HALF_LENGTH + tolerance)
    inside_cylinder = (point["y"] ** 2 + point["z"] ** 2
                       <= RADIUS**2 + tolerance)
    return inside_box and inside_cylinder


def integrate_once(integrand, low: float, high: float) -> float:
    """Return the one-dimensional integral of `integrand` between two limits."""
    value, _ = integrate.quad(integrand, low, high, epsabs=1e-12, epsrel=1e-12, limit=200)
    return float(value)


def integrate_over_limits(spec: tuple[str, str, str], integrand) -> float:
    """Return the nested integral of `integrand` over the limit set of one order.

    Args:
        spec: The three variable names, from the outer level to the inner level.
        integrand: Function of a dictionary that holds one value for each coordinate.

    Returns:
        The value of the nested integral.
    """
    def build(level: int, fixed: dict[str, float]) -> float:
        variable = spec[level]
        low, high = bounds_of(variable, fixed)
        if level == len(spec) - 1:
            return integrate_once(
                lambda value: integrand({**fixed, variable: value}), low, high)
        return integrate_once(
            lambda value: build(level + 1, {**fixed, variable: value}), low, high)

    return build(0, {})


def count_permutations_by_formula() -> int:
    """Return the number of orders from the factorial formula."""
    return math.factorial(len(COORDINATE_NAMES))


def count_permutations_by_loops() -> int:
    """Return the number of orders by three nested loops that skip a repeated name."""
    count = 0
    for first in COORDINATE_NAMES:
        for second in COORDINATE_NAMES:
            for third in COORDINATE_NAMES:
                if len({first, second, third}) == 3:
                    count += 1
    return count


def load_part5_values() -> dict[str, float]:
    """Return the order values that the script of Part 5 recorded, keyed by order name."""
    path = RESULTS_PATH.parent / "part5_results.json"
    records = json.loads(path.read_text(encoding="utf-8"))
    values: dict[str, float] = {}
    for record in records:
        label = record["label"]
        if label.startswith("order ") and " against 198*pi" in label:
            name = label[len("order "):label.index(" against")]
            values[name] = float(record["computed"])
    return values


def record(results: list[dict[str, object]], label: str, computed: float, expected: float,
           tolerance: float) -> None:
    """Append one comparison to the record, print it, and raise when it fails."""
    difference = abs(computed - expected)
    passed = difference <= tolerance
    results.append({
        "label": label,
        "computed": computed,
        "expected": expected,
        "difference": difference,
        "tolerance": tolerance,
        "passed": passed,
    })
    print(f"{label}: computed={computed:.12f} expected={expected:.12f} "
          f"difference={difference:.3e} tolerance={tolerance:.3e}")
    if not passed:
        raise AssertionError(f"{label}: difference {difference:.6e} exceeds {tolerance:.6e}")


def order_name_from_spec(spec: tuple[str, str, str]) -> str:
    """Return the written order name of a spec, with the inner variable first."""
    return " ".join(f"d{variable}" for variable in reversed(spec))


def main() -> None:
    """Run every check of Part 6 and write the record."""
    results: list[dict[str, object]] = []

    specs = list(itertools.permutations(COORDINATE_NAMES))
    record(results, "number of orders against 3! from the factorial formula",
           float(len(specs)), float(count_permutations_by_formula()), 0.0)
    record(results, "number of orders against the count of three nested loops",
           float(len(specs)), float(count_permutations_by_loops()), 0.0)

    inner_counts = {name: 0 for name in COORDINATE_NAMES}
    for spec in specs:
        inner_counts[spec[-1]] += 1
    for name, count in inner_counts.items():
        record(results, f"number of orders with {name} innermost against 6/3",
               float(count), float(len(specs) // len(COORDINATE_NAMES)), 0.0)

    generator = np.random.default_rng(RANDOM_SEED)
    sample_count = SAMPLE_COUNT
    sample_x = generator.uniform(-HALF_LENGTH, HALF_LENGTH, sample_count)
    sample_y = generator.uniform(-RADIUS, RADIUS, sample_count)
    sample_z = generator.uniform(-RADIUS, RADIUS, sample_count)
    points = [{"x": float(sample_x[index]), "y": float(sample_y[index]),
               "z": float(sample_z[index])} for index in range(sample_count)]
    inside_solid_count = sum(1 for point in points if point_is_inside_solid(point))
    outside_solid_count = sample_count - inside_solid_count
    print(f"random sample: {inside_solid_count} points inside E, "
          f"{outside_solid_count} points outside E, of {sample_count} points")
    if inside_solid_count == 0 or outside_solid_count == 0:
        raise AssertionError("the random sample does not contain both kinds of point")

    part5_values = load_part5_values()

    for spec in specs:
        name = order_name_from_spec(spec)
        accepted = sum(1 for point in points if point_is_inside_limits(spec, point))
        record(results, f"order {name} accepts the points of E only", float(accepted),
               float(inside_solid_count), 0.0)

        value = integrate_over_limits(spec, lambda point: 1.0)
        record(results, f"order {name} from the bound rule against 36*pi", value,
               EXACT_VOLUME, 1e-6 * EXACT_VOLUME)

        if name not in part5_values:
            raise AssertionError(f"no value of Part 5 for the order {name}")
        reference = part5_values[name]
        quadratic_value = integrate_over_limits(
            spec, lambda point: 1.0 + point["x"] + point["y"] ** 2 + point["z"] ** 2)
        record(results, f"order {name} from the bound rule against the value of Part 5",
               quadratic_value, reference, 1e-6 * reference)

    order_names = [order_name_from_spec(spec) for spec in specs]
    record(results, "number of distinct written order names", float(len(set(order_names))),
           float(len(specs)), 0.0)

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RESULTS_PATH}")


if __name__ == "__main__":
    main()
