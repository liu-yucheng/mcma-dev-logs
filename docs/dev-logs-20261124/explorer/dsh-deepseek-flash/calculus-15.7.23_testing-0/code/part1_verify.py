"""Part 1: turn the words of the statement into inequalities and test the result.

Two descriptions of the solid are compared.  The first description stacks three intervals and
uses the square root of the cylinder.  The second description tests the four surface
expressions one at a time.  A random sample and a fixed list of named points are the two
instruments of the comparison.  A Monte Carlo volume over the unit cube is the third
instrument: it does not use either description as an integration limit, and it compares with
the closed form of Part 3.
"""

from __future__ import annotations

import random

import mcma_support as support

SEED = 20261123
"""Seed of the random sample."""

SAMPLE_SIZE = 60000
"""Number of random points of the membership test."""

NAMED_POINTS = [
    ((0.0, 0.0, 0.0), True, "corner of the octant and of the plane y = x"),
    ((0.5, 0.5, 0.0), True, "point of the plane y = x inside the cylinder"),
    ((0.5, 0.5, 0.8660254037844386), True, "point of the cylinder on the plane y = x"),
    ((0.25, 0.75, 0.5), True, "interior point"),
    ((0.75, 0.25, 0.5), False, "point of the wrong side of the plane y = x"),
    ((0.25, 0.75, 0.9), False, "point above the cylinder"),
    ((1.0, 0.5, 0.0), False, "point of the wrong side of the plane y = x"),
    ((0.25, 0.75, -0.1), False, "point below the octant"),
]
"""Named points, with the status that the geometry of the four surfaces gives."""


def main() -> None:
    """Run the checks of Part 1 and write its record."""
    recorder = support.Recorder(1)
    random.seed(SEED)

    disagreements = 0
    hits = 0
    for _ in range(SAMPLE_SIZE):
        x = random.uniform(0.0, 1.0)
        y = random.uniform(0.0, 1.0)
        z = random.uniform(0.0, 1.0)
        first = support.inside_by_limits(x, y, z)
        second = support.inside_by_surfaces(x, y, z)
        hits += int(first)
        disagreements += int(first != second)
    recorder.record("random points: interval form against surface form", float(disagreements), 0.0)
    recorder.publish("p1_sample_size", str(SAMPLE_SIZE))
    recorder.publish("p1_hits", str(hits))
    recorder.publish("p1_seed", str(SEED))

    named_inside = sum(1 for point, status, _ in NAMED_POINTS if status)
    counted_inside = 0
    limit_hits = 0
    surface_hits = 0
    for point, status, _ in NAMED_POINTS:
        counted_inside += int(status)
        limit_hits += int(support.inside_by_limits(*point))
        surface_hits += int(support.inside_by_surfaces(*point))
    recorder.record("named points inside: interval form against the status list",
                    float(limit_hits), float(named_inside))
    recorder.record("named points inside: surface form against the status list",
                    float(surface_hits), float(named_inside))
    recorder.publish("p1_named_points", str(len(NAMED_POINTS)))
    recorder.publish("p1_named_inside", str(named_inside))

    monte_carlo = hits / SAMPLE_SIZE
    standard_error = (monte_carlo * (1.0 - monte_carlo) / SAMPLE_SIZE) ** 0.5
    closed_form = 1.0 / 3.0
    difference = abs(monte_carlo - closed_form)
    recorder.record("Monte Carlo volume against one third: absolute difference",
                    difference / standard_error, 0.0, tolerance=4.0)
    recorder.publish("p1_monte_carlo", f"{monte_carlo:.6f}")
    recorder.publish("p1_monte_carlo_error", f"{standard_error:.6f}")
    recorder.publish("p1_monte_carlo_z", f"{difference / standard_error:.3f}")

    ratio_cylinder = support.integrate(support.cylinder_height, 0.0, 1.0) / (3.141592653589793 / 4.0)
    recorder.record("quarter cylinder: quadrature against pi / 4, ratio", ratio_cylinder, 1.0,
                    tolerance=1.0e-12)
    recorder.publish("p1_quarter_cylinder", f"{3.141592653589793 / 4.0:.9f}")

    recorder.write()


if __name__ == "__main__":
    main()
