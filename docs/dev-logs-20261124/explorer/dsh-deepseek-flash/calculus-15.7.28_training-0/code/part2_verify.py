"""Check the horizontal cut of the solid at a fixed height.

The region is a stack of horizontal cuts.  This module derives each cut from the defining
inequalities, measures the area of the cut at five heights in two ways, and prints the list of
corners of each cut.  The area of the cut must come from the inequalities, not from a drawing.
"""

import json
from pathlib import Path

import numpy as np

RANDOM_SEED = 20261123
"""Seed of every pseudo-random sample of this module."""

SAMPLE_COUNT = 2000000
"""Count of the random points that the area estimate of one cut uses."""

RECTANGLE_TEST_COUNT = 4000
"""Count of the random points that the rectangle test of one cut uses."""

HEIGHTS = (0.0, 0.5, 1.0, 1.5, 2.0)
"""Heights at which the cut is measured."""

PLANE_LOW = (0.0, 0.0)
"""Lower corner of the box that holds the sampled points of one cut, as (x, z)."""

PLANE_HIGH = (4.0, 2.0)
"""Upper corner of the box that holds the sampled points of one cut, as (x, z)."""

RESULT_PATH = Path(__file__).with_name("results") / "part2_results.json"
"""Path of the record that the product page reads."""


def cut_membership(x, z, height):
    """Return the membership of points of the plane y = height, read from the inequalities.

    Args:
        x: Array of the x coordinates.
        z: Array of the z coordinates.
        height: The fixed value of y.

    Returns:
        A boolean array.  An entry is True when the point (x, height, z) obeys the region.
    """
    inside = (
        (height >= 0.0)
        & (height <= 2.0)
        & (z >= 0.0)
        & (z <= 2.0 - height)
        & (x >= 0.0)
        & (x <= 4.0 - height * height)
    )
    return inside


def cut_lengths(height):
    """Return the two side lengths of the cut from the pair of limits of x and of z.

    Args:
        height: The fixed value of y.

    Returns:
        A tuple of the length along x and the length along z.  Each length is zero when the
        pair of limits collapses.
    """
    length_x = max(0.0, 4.0 - height * height)
    length_z = max(0.0, 2.0 - height)
    return length_x, length_z


def cut_area_by_product(height):
    """Return the area of the cut as the product of the two side lengths.

    Args:
        height: The fixed value of y.

    Returns:
        The area of the cut as a float.
    """
    length_x, length_z = cut_lengths(height)
    return length_x * length_z


def cut_area_by_sampling(height, generator):
    """Return the area of the cut as a fraction of a box, without the side lengths.

    Args:
        height: The fixed value of y.
        generator: The pseudo-random generator of the module.

    Returns:
        The estimated area of the cut as a float.
    """
    low = np.array(PLANE_LOW)
    high = np.array(PLANE_HIGH)
    points = low + (high - low) * generator.random((SAMPLE_COUNT, 2))
    inside = cut_membership(points[:, 0], points[:, 1], height)
    box_area = (high[0] - low[0]) * (high[1] - low[1])
    return box_area * float(np.count_nonzero(inside)) / float(SAMPLE_COUNT)


def cut_corners(height):
    """Return the corner list of the cut, and the name of the shape that the list gives.

    Args:
        height: The fixed value of y.

    Returns:
        A dictionary with the corner list, the shape name, and the side lengths.
    """
    length_x, length_z = cut_lengths(height)
    corner_set = []
    for x in (0.0, length_x):
        for z in (0.0, length_z):
            point = (round(x, 12), round(height, 12), round(z, 12))
            if point not in corner_set:
                corner_set.append(point)
    shape_by_count = {1: "point", 2: "segment", 4: "rectangle"}
    return {
        "height": height,
        "length_x": length_x,
        "length_z": length_z,
        "corners": [list(point) for point in corner_set],
        "corner_count": len(corner_set),
        "shape": shape_by_count.get(len(corner_set), "region with a curved side"),
    }


def rectangle_test(height, generator):
    """Compare the cut with the product of the two intervals on random points.

    Args:
        height: The fixed value of y.
        generator: The pseudo-random generator of the module.

    Returns:
        The count of the points at which the two descriptions disagree.
    """
    low = np.array(PLANE_LOW)
    high = np.array(PLANE_HIGH)
    points = low + (high - low) * generator.random((RECTANGLE_TEST_COUNT, 2))
    x, z = points[:, 0], points[:, 1]
    length_x, length_z = cut_lengths(height)
    product_form = (x >= 0.0) & (x <= length_x) & (z >= 0.0) & (z <= length_z)
    return int(np.count_nonzero(cut_membership(x, z, height) != product_form))


def disk_test(height, generator, radius=2.0):
    """Compare the cut with a disk of the given radius on random points.

    Args:
        height: The fixed value of y.
        generator: The pseudo-random generator of the module.
        radius: The radius of the disk that the test compares with the cut.

    Returns:
        The count of the points at which the cut and the disk disagree.
    """
    low = np.array(PLANE_LOW)
    high = np.array(PLANE_HIGH)
    points = low + (high - low) * generator.random((RECTANGLE_TEST_COUNT, 2))
    x, z = points[:, 0], points[:, 1]
    disk_form = (x * x + z * z) <= radius * radius
    return int(np.count_nonzero(cut_membership(x, z, height) != disk_form))


def area_of_misread_cut(height):
    """Return the area of the cut when the inner limit holds z instead of y.

    Args:
        height: The fixed value of y.

    Returns:
        The area of the misread cut as a float.
    """
    length_z = max(0.0, 2.0 - height)
    return max(0.0, 4.0 * length_z - length_z ** 3 / 3.0)


def main():
    """Run every check of part 2 and write the record of the checked values."""
    generator = np.random.default_rng(RANDOM_SEED)
    rows = []
    print("part 2 checks")
    print(f"{'height':>7} {'length x':>10} {'length z':>10} {'area product':>13} "
          f"{'area sampling':>14} {'rel. gap':>10} {'shape':>10}")
    for height in HEIGHTS:
        length_x, length_z = cut_lengths(height)
        product_area = cut_area_by_product(height)
        sampled_area = cut_area_by_sampling(height, generator)
        relative_gap = 0.0 if product_area == 0.0 else abs(sampled_area - product_area) / product_area
        corners = cut_corners(height)
        print(
            f"{height:7.2f} {length_x:10.6f} {length_z:10.6f} {product_area:13.6f} "
            f"{sampled_area:14.6f} {relative_gap:10.2e} {corners['shape']:>10}"
        )
        print(f"        corners: {corners['corners']}")
        rows.append(
            {
                "height": height,
                "length_x": length_x,
                "length_z": length_z,
                "area_product": product_area,
                "area_sampled": sampled_area,
                "relative_gap": relative_gap,
                "shape": corners["shape"],
                "corner_count": corners["corner_count"],
                "corners": corners["corners"],
                "rectangle_disagreements": rectangle_test(height, generator),
                "disk_disagreements": disk_test(height, generator),
                "area_of_misread_cut": area_of_misread_cut(height),
            }
        )

    areas = [row["area_product"] for row in rows]
    monotone = all(areas[index] > areas[index + 1] for index in range(len(areas) - 1))
    shapes = [row["shape"] for row in rows]
    at_two = rows[-1]
    print(f"areas fall with the height          : {monotone}")
    print(f"shapes of the five cuts             : {shapes}")
    print(f"cut at y = 2 has {at_two['corner_count']} corner: {at_two['corners']}")
    print(f"area of the cut at y = 1            : {rows[2]['area_product']:.6f}")
    print(f"area of the misread cut at y = 1    : {rows[2]['area_of_misread_cut']:.6f}")

    for row in rows[:-1]:
        assert row["rectangle_disagreements"] == 0, (
            f"the cut at y = {row['height']} is not the product of two intervals"
        )
        assert row["relative_gap"] < 5.0e-3, (
            f"the sampled area at y = {row['height']} disagrees with the product"
        )
        assert row["disk_disagreements"] > 500, (
            f"the cut at y = {row['height']} is not distinguishable from a disk"
        )
    assert monotone, "the area of the cut does not fall with the height"
    assert shapes[:4] == ["rectangle"] * 4, "a cut below the top is not a rectangle"
    assert at_two["shape"] == "point", "the cut at y = 2 is not a single point"
    assert at_two["corners"] == [[0.0, 2.0, 0.0]], "the top point is not (0, 2, 0)"
    assert rows[2]["area_of_misread_cut"] - rows[2]["area_product"] > 0.5, (
        "the misread cut is not distinguishable at y = 1"
    )

    record = {
        "heights": list(HEIGHTS),
        "rows": rows,
        "monotone": monotone,
        "top_point": at_two["corners"][0],
        "shapes": shapes,
    }
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"record written to {RESULT_PATH}")
    print("part 2: all checks passed")


if __name__ == "__main__":
    main()
