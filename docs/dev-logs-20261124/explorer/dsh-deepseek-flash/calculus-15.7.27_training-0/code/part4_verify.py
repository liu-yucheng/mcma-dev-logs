"""Verification of Part 4: the face table, the volume, and the final answer.

The script reads the five faces off the six half-spaces, computes the volume by
the divergence theorem over those faces, and compares that volume with the
nested exact integral, with the sections, and with a rejection sample. It also
checks the two degenerate cuts that the sketch must show.
Run this script with the interpreter of the session environment:

    code/.venv/Scripts/python.exe code/part4_verify.py
"""

from fractions import Fraction
import math

import numpy as np

import figure_anchors
import region_tools as region

RANDOM_SEED = 424242
"""Seed of the rejection sample of this check."""

SAMPLE_COUNT = 600000
"""Number of points of the rejection sample."""

BOX_LOWER = (-0.1, -0.1, -0.1)
"""Lowest corner of the box of the rejection sample."""

BOX_UPPER = (1.1, 2.1, 1.1)
"""Highest corner of the box of the rejection sample."""

FACE_OF_INEQUALITY: tuple[tuple[str, str, str], ...] = (
    ("y is not below 0", "bottom face, the plane y = 0", "y >= 0"),
    ("y is not above 2 - 2 z", "top face, the plane y + 2 z = 2", "y <= 2 - 2 z"),
    ("x is not below 0", "wall, the plane x = 0", "x >= 0"),
    ("z is not below 0", "wall, the plane z = 0", "z >= 0"),
    ("z is not above 1 - x", "wall, the plane x + z = 1", "z <= 1 - x"),
)
"""One record for each inequality that owns a face, with the face name and the statement."""


def report(name: str, computed: float, expected: float, tolerance: float) -> None:
    """Print one comparison and assert that the values agree."""
    difference = abs(computed - expected)
    print(f"{name}: computed = {computed!r}, expected = {expected!r}, difference = {difference:.3e}")
    assert difference <= tolerance, f"{name} failed: {computed!r} differs from {expected!r}"


def corner_text(point: tuple) -> str:
    """Return a corner as a short text with exact fractions."""
    return "(" + ", ".join(str(value) for value in point) + ")"


def check_face_table(vertices: list) -> None:
    """Print the face table and check that every listed face has a positive area."""
    records = {str(record["name"]): record for record in region.face_report(vertices)}
    plane_of_name = {name: (name, coefficients, bound) for name, coefficients, bound in region.SOLID_HALF_SPACES}
    print("check the face table")
    for half_space_name, face_name, statement in FACE_OF_INEQUALITY:
        record = records[half_space_name]
        points = record["points"]
        area = float(record["area"])
        ordered = region.order_face_points(points, plane_of_name[half_space_name])
        corners = "; ".join(corner_text(point) for point in ordered)
        print(f"  {statement} gives {face_name}: {len(points)} corners, area = {area:.6f}")
        print(f"    corners: {corners}")
        assert len(points) >= 3, f"{face_name} has fewer than three corners"
        assert area > 0.0, f"{face_name} has no area"
    print("  x <= 1 gives one edge only, from P1 to P4, so the sketch has five faces")


def check_divergence_volume(vertices: list) -> None:
    """Check the volume by the divergence theorem over the five faces."""
    total = 0.0
    for record in region.face_report(vertices):
        coefficients = record["coefficients"]
        bound = float(record["bound"])
        norm = math.sqrt(sum(float(component) ** 2 for component in coefficients))
        total += bound / norm * float(record["area"])
    volume = total / 3.0
    exact = float(region.exact_volume())
    print(f"check the volume by the divergence theorem: {volume!r}")
    report("volume from the faces", volume, exact, 1.0e-12)


def check_rejection_volume() -> None:
    """Check the volume by a rejection sample in a box that holds the solid."""
    generator = np.random.default_rng(RANDOM_SEED)
    draws = generator.uniform(low=BOX_LOWER, high=BOX_UPPER, size=(SAMPLE_COUNT, 3))
    inside = (
        (draws[:, 0] >= 0.0)
        & (draws[:, 0] <= 1.0)
        & (draws[:, 2] >= 0.0)
        & (draws[:, 2] <= 1.0 - draws[:, 0])
        & (draws[:, 1] >= 0.0)
        & (draws[:, 1] <= 2.0 - 2.0 * draws[:, 2])
    )
    share = float(np.count_nonzero(inside)) / SAMPLE_COUNT
    box_volume = math.prod(BOX_UPPER[index] - BOX_LOWER[index] for index in range(3))
    estimate = share * box_volume
    standard_error = box_volume * math.sqrt(share * (1.0 - share) / SAMPLE_COUNT)
    print(f"check the volume by rejection: share = {share!r}, estimate = {estimate!r}")
    report("volume from the rejection sample", estimate, float(region.exact_volume()), 3.0 * standard_error)


def check_volume_agreement() -> None:
    """Check that the three nested integrations and the three section families agree."""
    exact = region.exact_volume()
    print(f"check the volume: nested integration gives {exact}")
    for axis in ("z", "x", "y"):
        by_sections = region.volume_by_sections(axis)
        print(f"  the sections at constant {axis} give {by_sections}")
        assert by_sections == exact, f"the sections at constant {axis} give {by_sections}"


def check_degenerate_cuts() -> None:
    """Check the two cuts of the sketch that shrink to a segment and to a point."""
    segment_section = region.slice_polygon("x", Fraction(1))
    print(f"check the cut at x = 1: {[(str(p[0]), str(p[1])) for p in segment_section]} in the plane coordinates")
    area_at_one = region.section_area_from_polygon("x", Fraction(1))
    report("area of the cut at x = 1", float(area_at_one), 0.0, 0.0)
    point_section = region.slice_polygon("z", Fraction(1))
    report("area of the cut at z = 1", float(region.polygon_area(point_section)), 0.0, 0.0)
    corners_at_one = [point for point in region.enumerate_vertices() if point[0] == 1]
    print(f"  the corners with x = 1: {[corner_text(point) for point in corners_at_one]}")
    assert len(corners_at_one) == 2, "the plane x = 1 must meet the solid in one edge"
    corners_at_z_one = [point for point in region.enumerate_vertices() if point[2] == 1]
    print(f"  the corners with z = 1: {[corner_text(point) for point in corners_at_z_one]}")
    assert len(corners_at_z_one) == 1, "the plane z = 1 must meet the solid in one point"


def check_top_edge() -> None:
    """Check that the top edge is the highest part of the solid."""
    vertices = region.enumerate_vertices()
    highest = max(point[1] for point in vertices)
    on_top = [corner_text(point) for point in vertices if point[1] == highest]
    print(f"check the top edge: highest y = {highest}, corners = {on_top}")
    assert highest == 2, "the highest y of the corners is not 2"
    assert len(on_top) == 2, "the top height must belong to one edge"
    for point in vertices:
        if point[1] == highest:
            assert point[2] == 0, "a top corner does not lie in the plane z = 0"
    generator = np.random.default_rng(RANDOM_SEED + 1)
    draws = generator.uniform(low=BOX_LOWER, high=BOX_UPPER, size=(20000, 3))
    inside = (
        (draws[:, 0] >= 0.0)
        & (draws[:, 0] <= 1.0)
        & (draws[:, 2] >= 0.0)
        & (draws[:, 2] <= 1.0 - draws[:, 0])
        & (draws[:, 1] >= 0.0)
        & (draws[:, 1] <= 2.0 - 2.0 * draws[:, 2])
    )
    top_gap = draws[inside, 1] + 2.0 * draws[inside, 2]
    sample_count = int(np.count_nonzero(inside))
    highest_y = float(draws[inside, 1].max())
    print(f"  highest y of the {sample_count} sample points of the solid = {highest_y!r}")
    print(f"  highest y + 2 z of the sample = {float(top_gap.max())!r}")
    assert float(top_gap.max()) <= 2.0 + 1.0e-12, "a sample point lies above the top face"
    near_top = int(np.count_nonzero(top_gap > 1.99))
    print(f"  sample points within 0.01 of the top face = {near_top}")
    assert near_top > 0, "the sample never reaches the top face"


def check_convexity() -> None:
    """Check that the midpoint of each pair of corners is inside the solid."""
    vertices = region.enumerate_vertices()
    checked = 0
    for first in range(len(vertices)):
        for second in range(first + 1, len(vertices)):
            middle = tuple((vertices[first][index] + vertices[second][index]) / 2 for index in range(3))
            assert region.contains(middle), f"the midpoint of two corners is outside at {middle}"
            checked += 1
    print(f"check the convexity: {checked} midpoints of corner pairs lie inside the solid")


def check_final_answer() -> None:
    """Check the numbers that the final answer of the tutorial states."""
    vertices = region.enumerate_vertices()
    box = region.bounding_box(vertices)
    print("check the final answer")
    for index, name in enumerate(("x", "y", "z")):
        print(f"  {name}: {box[index][0]} <= {name} <= {box[index][1]}")
    assert box == (
        (Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(2)),
        (Fraction(0), Fraction(1)),
    ), f"the box is {box}"
    base = float(region.polygon_area(region.slice_polygon("y", Fraction(0))))
    report("base area of the final answer", base, 0.5, 0.0)
    report("volume of the final answer", float(region.exact_volume()), float(2) / 3.0, 0.0)
    anchor = figure_anchors.TOP_FACE_ANCHOR
    assert anchor[1] == 2 - 2 * anchor[2], "the top face anchor is not on the top plane"
    print("  the five corners and the five faces of the sketch are the ones that the checks use")


def main() -> None:
    """Run every check of Part 4 in order."""
    print("Part 4: the face table, the volume, and the final answer")
    vertices = region.enumerate_vertices()
    check_face_table(vertices)
    check_divergence_volume(vertices)
    check_rejection_volume()
    check_volume_agreement()
    check_degenerate_cuts()
    check_top_edge()
    check_convexity()
    check_final_answer()
    print("Part 4: every check passed")


if __name__ == "__main__":
    main()
