"""Verification of Part 2: the three cross sections of the solid.

Every section shape and every section area comes from the inequalities by
polygon clipping. The closed forms of the tutorial are compared with the
clipping result, with a midpoint grid, and with an exact vertex list. Run this
script with the interpreter of the session environment:

    code/.venv/Scripts/python.exe code/part2_verify.py
"""

from fractions import Fraction

import region_tools as region

SECTION_VALUES: dict[str, tuple[Fraction, ...]] = {
    "z": (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)),
    "x": (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)),
    "y": (Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3, 2)),
}
"""Sample values of each slicing variable, all strictly inside the range."""

def expected_shape(axis: str, value: Fraction) -> str:
    """Return the plane-figure name that the inequalities give for one slice.

    At the two ends of its range a family loses one pair of sides. The section
    at x = 0 and the section at y = 0 are triangles, and the section at z = 0
    keeps all four sides.
    """
    if axis == "z":
        return "rectangle"
    if value == 0:
        return "triangle"
    return "trapezoid"


def report(name: str, computed: float, expected: float, tolerance: float) -> None:
    """Print one comparison and assert that the values agree."""
    difference = abs(computed - expected)
    print(f"{name}: computed = {computed!r}, expected = {expected!r}, difference = {difference:.3e}")
    assert difference <= tolerance, f"{name} failed: {computed!r} differs from {expected!r}"


def expected_vertices(axis: str, value: Fraction) -> set[tuple[Fraction, Fraction]]:
    """Return the corner list that the inequalities give for one slice.

    The list is written from the inequalities directly, in the plane
    coordinates of `region.PLANE_AXES`, and it does not use the clipping walk.
    """
    if axis == "z":
        return {
            (Fraction(0), Fraction(0)),
            (1 - value, Fraction(0)),
            (1 - value, 2 - 2 * value),
            (Fraction(0), 2 - 2 * value),
        }
    if axis == "x":
        return {
            (Fraction(0), Fraction(0)),
            (1 - value, Fraction(0)),
            (1 - value, 2 * value),
            (Fraction(0), Fraction(2)),
        }
    if axis == "y":
        return {
            (Fraction(0), Fraction(0)),
            (Fraction(1), Fraction(0)),
            (value / 2, 1 - value / 2),
            (Fraction(0), 1 - value / 2),
        }
    raise ValueError(f"unknown axis {axis}")


def check_sections(axis: str) -> None:
    """Check the shape, the corner list, and the area of each slice of one family."""
    print(f"check the sections at constant {axis}")
    for value in SECTION_VALUES[axis]:
        polygon = region.slice_polygon(axis, value)
        clipped_area = region.polygon_area(polygon)
        closed_area = region.section_area_from_formula(axis, value)
        print(
            f"  {axis} = {value}: corners = {len(polygon)}, clipped area = {clipped_area}, "
            f"closed form = {closed_area}"
        )
        assert clipped_area == closed_area, f"the closed form misses the clip at {axis} = {value}"
        corners = {(point[0], point[1]) for point in polygon}
        assert corners == expected_vertices(axis, value), f"corner list differs at {axis} = {value}"
        shape = region.name_polygon(region.describe_polygon(polygon))
        assert shape == expected_shape(axis, value), f"a section at {axis} = {value} is a {shape}"
        grid_area = region.section_area_from_grid(axis, value, count=300)
        report(f"  grid area at {axis} = {value}", grid_area, float(closed_area), 0.02)
    print(f"  each section at constant {axis} has the shape that the inequalities give")


def check_section_size(axis: str) -> None:
    """Check that the closed form agrees with the width and the height of the clip."""
    print(f"check the size of the sections at constant {axis}")
    for value in SECTION_VALUES[axis]:
        polygon = region.slice_polygon(axis, value)
        horizontal = [point[0] for point in polygon]
        vertical = [point[1] for point in polygon]
        width = max(horizontal) - min(horizontal)
        height = max(vertical) - min(vertical)
        print(f"  {axis} = {value}: width = {width}, height = {height}, product = {width * height}")
        if axis == "z":
            report(f"  width of the rectangle at z = {value}", float(width), float(1 - value), 0.0)
            report(f"  height of the rectangle at z = {value}", float(height), float(2 - 2 * value), 0.0)


def check_shrinking() -> None:
    """Check that a section area falls as the slicing variable grows."""
    print("check that each section area falls with its own variable")
    for axis, values in SECTION_VALUES.items():
        areas = [region.section_area_from_polygon(axis, value) for value in values]
        decreasing = all(areas[index] > areas[index + 1] for index in range(len(areas) - 1))
        print(f"  {axis}: areas = {[str(area) for area in areas]}, strictly falling = {decreasing}")
        assert decreasing, f"the areas of the slices at constant {axis} do not fall"


def check_volume_by_sections() -> None:
    """Check the volume through the sections of each family."""
    exact = region.exact_volume()
    for axis in ("z", "x", "y"):
        by_closed_form = region.volume_by_sections(axis)
        print(f"check the volume from the closed sections at constant {axis}: {by_closed_form}")
        assert by_closed_form == exact, f"the sections at constant {axis} give {by_closed_form}"
        upper = Fraction(2) if axis == "y" else Fraction(1)
        step_count = 240
        step = upper / step_count
        total = Fraction(0)
        for index in range(step_count):
            centre = (index + Fraction(1, 2)) * step
            total += region.section_area_from_polygon(axis, centre) * step
        report(f"volume from clipped sections at constant {axis}", float(total), float(exact), 1.0e-3)
    print(f"check the volume: every family of sections gives {exact}")


def main() -> None:
    """Run every check of Part 2 in order."""
    print("Part 2: the cross sections")
    for axis in ("z", "x", "y"):
        check_sections(axis)
        check_section_size(axis)
    check_shrinking()
    check_volume_by_sections()
    print("Part 2: every check passed")


if __name__ == "__main__":
    main()
