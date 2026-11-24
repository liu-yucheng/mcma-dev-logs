"""Verification of Part 3: the corners, the faces, and the label anchors.

The script derives the corners from the six half-spaces, compares them with the
corner list of the drawing, compares each face area with an integral over the
same face, and checks that every label of the figure sits on its own surface.
Run this script with the interpreter of the session environment:

    code/.venv/Scripts/python.exe code/part3_verify.py
"""

from fractions import Fraction
import math

import figure_anchors
import region_tools as region

AREA_TOLERANCE = 1.0e-12
"""Largest allowed difference between a face area and its integral."""


def report(name: str, computed: float, expected: float, tolerance: float) -> None:
    """Print one comparison and assert that the values agree."""
    difference = abs(computed - expected)
    print(f"{name}: computed = {computed!r}, expected = {expected!r}, difference = {difference:.3e}")
    assert difference <= tolerance, f"{name} failed: {computed!r} differs from {expected!r}"


def check_corners() -> list:
    """Check that the half-spaces and the named corners give the same five points."""
    derived = region.enumerate_vertices()
    named = [point for _, point in figure_anchors.VERTEX_NAMES]
    print(f"check the corners: derived = {[(str(p[0]), str(p[1]), str(p[2])) for p in derived]}")
    assert len(derived) == len(named), f"the half-spaces give {len(derived)} corners and not {len(named)}"
    assert sorted(derived) == sorted(named), "the derived corners differ from the named corners"
    for name, point in figure_anchors.VERTEX_NAMES:
        assert region.contains(point), f"{name} is not in the solid"
    print(f"check the corners: the {len(named)} named corners are the corners of the half-spaces")
    return derived


def check_faces(vertices: list) -> None:
    """Check the corner count and the area of every face."""
    base_area = float(region.polygon_area(region.slice_polygon("y", Fraction(0))))
    expected_areas = {
        "x is not below 0": region.polynomial_integral([Fraction(2), Fraction(-2)], Fraction(0), Fraction(1)),
        "x is not above 1": Fraction(0),
        "z is not below 0": Fraction(2),
        "z is not above 1 - x": math.sqrt(2.0),
        "y is not below 0": Fraction(1, 2),
        "y is not above 2 - 2 z": math.sqrt(5.0) * base_area,
    }
    print(f"check the faces: the base area is {base_area!r}")
    for record in region.face_report(vertices):
        name = str(record["name"])
        points = int(record["point_count"])
        area = float(record["area"])
        expected = float(expected_areas[name])
        print(f"  {name}: {points} corners, area = {area!r}")
        report(f"  area of the face {name}", area, expected, AREA_TOLERANCE)
        if name == "x is not above 1":
            assert points == 2, "the plane x = 1 must meet the solid in one edge"
            print("  the plane x = 1 meets the solid in one edge, so it is not a face")
        else:
            assert points >= 3, f"the face {name} must have at least three corners"
    total = sum(float(record["area"]) for record in region.face_report(vertices))
    independent = (
        0.5 + 1.0 + 2.0 + math.sqrt(2.0) + math.sqrt(5.0) * 0.5
    )
    report("total surface area", total, independent, AREA_TOLERANCE)


def check_anchors() -> None:
    """Check that each label anchor lies on its own surface and inside the solid."""
    bound_by_name = {name: (coefficients, bound) for name, coefficients, bound in region.SOLID_HALF_SPACES}
    print("check the label anchors")
    for face_name, half_space_name, point in figure_anchors.FACE_ANCHORS:
        coefficients, bound = bound_by_name[half_space_name]
        value = region.dot(coefficients, point)
        print(f"  {face_name}: point = {tuple(str(item) for item in point)}, plane value = {value}, bound = {bound}")
        assert value == bound, f"the anchor of {face_name} is not on the plane {half_space_name}"
        assert region.contains(point), f"the anchor of {face_name} is outside the solid"
        for other_name, other_coefficients, other_bound in region.SOLID_HALF_SPACES:
            if other_name == half_space_name:
                continue
            margin = other_bound - region.dot(other_coefficients, point)
            assert margin > 0, f"the anchor of {face_name} lies on the edge {other_name}"
    print("check the label anchors: each anchor satisfies its own plane and avoids every other plane")


def check_height_segment() -> None:
    """Check the drawn height segment: it stands on the base and ends on the top face."""
    foot = figure_anchors.HEIGHT_SEGMENT_FOOT
    head = figure_anchors.HEIGHT_SEGMENT_HEAD
    print(f"check the height segment: foot = {tuple(str(item) for item in foot)}")
    print(f"check the height segment: head = {tuple(str(item) for item in head)}")
    assert foot[1] == 0, "the foot of the height segment is not on the bottom face"
    assert head[1] == 2 - 2 * head[2], "the head of the height segment is not on the top face"
    assert head[0] == foot[0] and head[2] == foot[2], "the height segment is not parallel to the y axis"
    samples = 200
    for index in range(samples + 1):
        share = Fraction(index, samples)
        point = (
            foot[0],
            foot[1] + share * (head[1] - foot[1]),
            foot[2],
        )
        assert region.contains(point), f"the height segment leaves the solid at {point}"
    length = float(head[1] - foot[1])
    report("length of the height segment", length, float(2 - 2 * foot[2]), 1.0e-15)


def check_projection() -> None:
    """Check that the drawn base triangle is the projection of the solid."""
    drawn = list(figure_anchors.PROJECTION_TRIANGLE)
    clipped = region.slice_polygon("y", Fraction(0))
    drawn_set = {(point[0], point[1]) for point in drawn}
    clipped_set = {(point[0], point[1]) for point in clipped}
    print(f"check the projection: drawn = {[(str(u), str(v)) for u, v in drawn]}")
    assert drawn_set == clipped_set, "the drawn base triangle differs from the section at y = 0"
    report(
        "area of the drawn base triangle",
        float(region.polygon_area(drawn)),
        float(region.polygon_area(clipped)),
        0.0,
    )


def main() -> None:
    """Run every check of Part 3 in order."""
    print("Part 3: the corners, the faces, and the drawing")
    vertices = check_corners()
    check_faces(vertices)
    check_anchors()
    check_height_segment()
    check_projection()
    print("Part 3: every check passed")


if __name__ == "__main__":
    main()
