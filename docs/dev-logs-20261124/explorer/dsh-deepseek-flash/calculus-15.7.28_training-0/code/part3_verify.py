"""Check the five boundary surfaces and the eight edges of the solid.

The region has five defining inequalities, so its boundary has five pieces.  This module builds
one patch for each inequality, checks that each patch lies on its own level set and on the
boundary of the region, and checks the eight edges where two patches meet.
"""

import json
from pathlib import Path
from typing import NamedTuple

import numpy as np
from scipy.integrate import quad

RANDOM_SEED = 20261124
"""Seed of every pseudo-random sample of this module."""

SAMPLE_COUNT = 600
"""Count of the sample points that one patch uses."""

STEP = 1.0e-5
"""Length of the step that the boundary test takes along the outward normal."""

RESULT_PATH = Path(__file__).with_name("results") / "part3_results.json"
"""Path of the record that the product page reads."""

VERTICES = {
    "A": (0.0, 0.0, 0.0),
    "B": (4.0, 0.0, 0.0),
    "C": (4.0, 0.0, 2.0),
    "D": (0.0, 0.0, 2.0),
    "T": (0.0, 2.0, 0.0),
}
"""The five corners of the solid.  T is the point where the solid ends."""


class Surface(NamedTuple):
    """One piece of the boundary of the solid.

    Attributes:
        name: Short name of the patch, as S1 to S5.
        equation: The equation of the surface, as a text for the product page.
        residual: A function of a point array that returns the signed distance function.
        outward: A function of a point array that returns the unit outward normal.
        sample: A function of a generator and a count that returns points of the patch.
        area: The area of the patch, computed by an independent integral.
    """

    name: str
    equation: str
    residual: object
    outward: object
    sample: object
    area: float


def residual_bottom(points):
    """Return the signed distance to the surface y = 0, positive below the surface."""
    return -points[:, 1]


def residual_back(points):
    """Return the signed distance to the surface x = 0, positive behind the surface."""
    return -points[:, 0]


def residual_floor(points):
    """Return the signed distance to the surface z = 0, positive below the surface."""
    return -points[:, 2]


def residual_slope(points):
    """Return the signed distance to the surface y + z = 2, positive above the surface."""
    return (points[:, 1] + points[:, 2] - 2.0) / np.sqrt(2.0)


def residual_wall(points):
    """Return the signed distance to the surface x = 4 - y^2, positive outside the wall."""
    y = points[:, 1]
    return (points[:, 0] + y * y - 4.0) / np.sqrt(1.0 + 4.0 * y * y)


def outward_bottom(points):
    """Return the unit outward normal of the surface y = 0."""
    return np.tile(np.array([0.0, -1.0, 0.0]), (points.shape[0], 1))


def outward_back(points):
    """Return the unit outward normal of the surface x = 0."""
    return np.tile(np.array([-1.0, 0.0, 0.0]), (points.shape[0], 1))


def outward_floor(points):
    """Return the unit outward normal of the surface z = 0."""
    return np.tile(np.array([0.0, 0.0, -1.0]), (points.shape[0], 1))


def outward_slope(points):
    """Return the unit outward normal of the surface y + z = 2."""
    return np.tile(np.array([0.0, 1.0, 1.0]) / np.sqrt(2.0), (points.shape[0], 1))


def outward_wall(points):
    """Return the unit outward normal of the surface x = 4 - y^2."""
    y = points[:, 1]
    scale = np.sqrt(1.0 + 4.0 * y * y)
    return np.stack([np.ones_like(y), 2.0 * y, np.zeros_like(y)], axis=1) / scale[:, None]


def sample_bottom(generator, count):
    """Return points of the patch y = 0, away from its edges."""
    u = 0.05 + 0.9 * generator.random(count)
    v = 0.05 + 0.9 * generator.random(count)
    return np.stack([4.0 * u, np.zeros(count), 2.0 * v], axis=1)


def sample_back(generator, count):
    """Return points of the patch x = 0, away from its edges."""
    u = 0.05 + 0.9 * generator.random(count)
    v = 0.05 + 0.9 * generator.random(count)
    return np.stack([np.zeros(count), 2.0 * u, (2.0 - 2.0 * u) * v], axis=1)


def sample_floor(generator, count):
    """Return points of the patch z = 0, away from its edges."""
    u = 0.05 + 0.9 * generator.random(count)
    v = 0.05 + 0.9 * generator.random(count)
    y = 2.0 * u
    return np.stack([(4.0 - y * y) * v, y, np.zeros(count)], axis=1)


def sample_slope(generator, count):
    """Return points of the patch y + z = 2, away from its edges."""
    u = 0.05 + 0.9 * generator.random(count)
    v = 0.05 + 0.9 * generator.random(count)
    y = 2.0 * u
    return np.stack([(4.0 - y * y) * v, y, 2.0 - y], axis=1)


def sample_wall(generator, count):
    """Return points of the patch x = 4 - y^2, away from its edges."""
    u = 0.05 + 0.9 * generator.random(count)
    v = 0.05 + 0.9 * generator.random(count)
    y = 2.0 * u
    return np.stack([4.0 - y * y, y, (2.0 - y) * v], axis=1)


def area_of_slope_patch():
    """Return the area of the patch on the surface y + z = 2 by a two-dimensional integral."""
    value, _ = quad(lambda y: (4.0 - y * y) * np.sqrt(2.0), 0.0, 2.0)
    return value


def area_of_wall_patch():
    """Return the area of the patch on the surface x = 4 - y^2 by a two-dimensional integral."""
    value, _ = quad(lambda y: (2.0 - y) * np.sqrt(1.0 + 4.0 * y * y), 0.0, 2.0)
    return value


def build_surfaces():
    """Return the five patches of the boundary, each with an area from an integral."""
    return (
        Surface("S1", "y = 0", residual_bottom, outward_bottom, sample_bottom, 8.0),
        Surface("S2", "x = 0", residual_back, outward_back, sample_back, 2.0),
        Surface("S3", "z = 0", residual_floor, outward_floor, sample_floor, 16.0 / 3.0),
        Surface("S4", "y + z = 2", residual_slope, outward_slope, sample_slope, area_of_slope_patch()),
        Surface(
            "S5",
            "x = 4 - y^2",
            residual_wall,
            outward_wall,
            sample_wall,
            area_of_wall_patch(),
        ),
    )


def inside_region(points):
    """Return the membership of points in the closed region, read from the five inequalities."""
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    inside = (
        (x >= -1.0e-12)
        & (z >= -1.0e-12)
        & (y >= -1.0e-12)
        & (y + z <= 2.0 + 1.0e-12)
        & (x + y * y <= 4.0 + 1.0e-12)
    )
    return inside


def count_surfaces_at_point(point):
    """Return the count of surfaces of the boundary that hold one point."""
    array = np.array([point])
    return sum(1 for surface in build_surfaces() if abs(float(surface.residual(array)[0])) < 1.0e-12)


def edge_records():
    """Return the eight edges, each with a name, two corners, two surfaces, and a curve."""
    edges = (
        (
            "e1",
            "A",
            "B",
            "S1",
            "S3",
            "y = 0 and z = 0",
            lambda t: np.stack([4.0 * t, 0.0 * t, 0.0 * t], axis=1),
        ),
        (
            "e2",
            "B",
            "C",
            "S1",
            "S5",
            "y = 0 and x = 4 - y^2",
            lambda t: np.stack([4.0 + 0.0 * t, 0.0 * t, 2.0 * t], axis=1),
        ),
        (
            "e3",
            "C",
            "D",
            "S1",
            "S4",
            "y = 0 and y + z = 2",
            lambda t: np.stack([4.0 - 4.0 * t, 0.0 * t, 2.0 + 0.0 * t], axis=1),
        ),
        (
            "e4",
            "D",
            "A",
            "S1",
            "S2",
            "y = 0 and x = 0",
            lambda t: np.stack([0.0 * t, 0.0 * t, 2.0 - 2.0 * t], axis=1),
        ),
        (
            "e5",
            "A",
            "T",
            "S2",
            "S3",
            "x = 0 and z = 0",
            lambda t: np.stack([0.0 * t, 2.0 * t, 0.0 * t], axis=1),
        ),
        (
            "e6",
            "D",
            "T",
            "S2",
            "S4",
            "x = 0 and y + z = 2",
            lambda t: np.stack([0.0 * t, 2.0 * t, 2.0 - 2.0 * t], axis=1),
        ),
        (
            "e7",
            "B",
            "T",
            "S3",
            "S5",
            "z = 0 and x = 4 - y^2",
            lambda t: np.stack([4.0 - 4.0 * t * t, 2.0 * t, 0.0 * t], axis=1),
        ),
        (
            "e8",
            "C",
            "T",
            "S4",
            "S5",
            "y + z = 2 and x = 4 - y^2",
            lambda t: np.stack([4.0 - 4.0 * t * t, 2.0 * t, 2.0 - 2.0 * t], axis=1),
        ),
    )
    return edges


def check_edges():
    """Check each edge against its two named surfaces, its endpoints, and its length.

    Returns:
        A list of records, one for each edge.
    """
    parameters = np.linspace(0.0, 1.0, 401)
    surfaces = {surface.name: surface for surface in build_surfaces()}
    records = []
    for name, start, end, first, second, description, curve in edge_records():
        points = curve(parameters)
        residual_first = float(np.max(np.abs(surfaces[first].residual(points))))
        residual_second = float(np.max(np.abs(surfaces[second].residual(points))))
        others = [key for key in surfaces if key not in (first, second)]
        residual_other = min(
            float(np.max(np.abs(surfaces[key].residual(points)))) for key in others
        )
        start_error = float(np.linalg.norm(points[0] - np.array(VERTICES[start])))
        end_error = float(np.linalg.norm(points[-1] - np.array(VERTICES[end])))
        chord = float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())

        def speed(parameter):
            """Return the speed of the curve at one parameter value."""
            small = 1.0e-6
            forward = curve(np.array([parameter + small]))
            backward = curve(np.array([parameter - small]))
            return float(np.linalg.norm((forward - backward)[0]) / (2.0 * small))

        arc, _ = quad(speed, 0.0, 1.0)
        records.append(
            {
                "name": name,
                "from": start,
                "to": end,
                "surfaces": [first, second],
                "description": description,
                "residual_first": residual_first,
                "residual_second": residual_second,
                "largest_residual": max(residual_first, residual_second),
                "residual_other": residual_other,
                "start_error": start_error,
                "end_error": end_error,
                "arc_length": float(arc),
                "chord_length": chord,
                "on_boundary": bool(np.all(inside_region(points))),
            }
        )
    return records


def main():
    """Run every check of part 3 and write the record of the checked values."""
    generator = np.random.default_rng(RANDOM_SEED)
    surfaces = build_surfaces()
    surface_records = []
    print("part 3 checks: the five patches")
    for surface in surfaces:
        points = surface.sample(generator, SAMPLE_COUNT)
        residual = surface.residual(points)
        normal = surface.outward(points)
        outward_points = points + STEP * normal
        inward_points = points - STEP * normal
        record = {
            "name": surface.name,
            "equation": surface.equation,
            "largest_residual": float(np.max(np.abs(residual))),
            "all_inside": bool(np.all(inside_region(points))),
            "outward_step_outside": bool(np.all(~inside_region(outward_points))),
            "inward_step_inside": bool(np.all(inside_region(inward_points))),
            "area": float(surface.area),
        }
        surface_records.append(record)
        print(
            f"{surface.name} {surface.equation:14s} residual {record['largest_residual']:.3e} "
            f"inside {record['all_inside']} outward step outside {record['outward_step_outside']} "
            f"inward step inside {record['inward_step_inside']} area {record['area']:.6f}"
        )

    print("part 3 checks: the five corners")
    corner_records = {}
    for name, point in VERTICES.items():
        count = count_surfaces_at_point(point)
        corner_records[name] = {"point": list(point), "surface_count": count}
        print(f"{name} {point} lies on {count} surfaces")

    print("part 3 checks: the eight edges")
    edges = check_edges()
    for record in edges:
        print(
            f"{record['name']} {record['from']}->{record['to']} residual "
            f"{record['largest_residual']:.3e} start error {record['start_error']:.3e} "
            f"end error {record['end_error']:.3e} arc {record['arc_length']:.6f} "
            f"chord {record['chord_length']:.6f}"
        )

    for record in surface_records:
        assert record["largest_residual"] < 1.0e-12, f"{record['name']} is not on its surface"
        assert record["all_inside"], f"{record['name']} holds a point outside the region"
        assert record["outward_step_outside"], f"{record['name']} does not bound the region"
        assert record["inward_step_inside"], f"{record['name']} holds a point on the wrong side"
        assert record["area"] > 0.5, f"{record['name']} has no positive area"
    counts = [corner_records[name]["surface_count"] for name in ("A", "B", "C", "D", "T")]
    assert counts[:4] == [3, 3, 3, 3], "a corner below the top does not join three surfaces"
    assert corner_records["T"]["surface_count"] == 4, "the top point does not join four surfaces"
    for record in edges:
        assert record["largest_residual"] < 1.0e-9, f"{record['name']} leaves its two surfaces"
        assert record["residual_other"] > 1.0e-3, (
            f"{record['name']} also lies on a third surface"
        )
        assert record["start_error"] < 1.0e-12, f"{record['name']} has a wrong start point"
        assert record["end_error"] < 1.0e-12, f"{record['name']} has a wrong end point"
        assert record["on_boundary"], f"{record['name']} leaves the closed region"
        assert abs(record["arc_length"] - record["chord_length"]) < 1.0e-4, (
            f"{record['name']} length disagrees between the integral and the polyline"
        )

    output = {
        "surfaces": surface_records,
        "corners": corner_records,
        "edges": edges,
        "step": STEP,
        "sample_count": SAMPLE_COUNT,
    }
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"record written to {RESULT_PATH}")
    print("part 3: all checks passed")


if __name__ == "__main__":
    main()
