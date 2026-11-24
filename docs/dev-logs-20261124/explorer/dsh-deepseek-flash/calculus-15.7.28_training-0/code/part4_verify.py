"""Check the drawing of the solid against the inequalities that define the region.

This module builds a triangular mesh of the five patches, and then checks the drawings with
values that come from a different computation: the volume from the closed mesh against the
volume from the horizontal cuts, the area of each drawn patch against an integral, the cut at a
height against the pair of limits, the projection against the rectangle that the limits give,
and the position of every label against the equation of the surface that the label names.
"""

import json
from pathlib import Path
from typing import NamedTuple

import numpy as np
from scipy.integrate import quad, tplquad

RANDOM_SEED = 20261125
"""Seed of every pseudo-random sample of this module."""

SUBDIVISION = 40
"""Count of the subdivisions of one parametric direction of one patch."""

PROJECTION_SAMPLE_COUNT = 200000
"""Count of the random points that the projection test uses."""

HEIGHTS_OF_CHECK = (0.51, 1.01, 1.51)
"""Heights at which the drawn solid is cut for a check.

Each height lies between two rows of mesh nodes, so each crossing point comes from an
interpolation along a mesh edge and not from a node that the parameter map placed there.
"""

RESULT_PATH = Path(__file__).with_name("results") / "part4_results.json"
"""Path of the record that the product page reads."""

LABEL_POINTS = {
    "S1": (2.2, 0.0, 1.0),
    "S2": (0.0, 0.6, 0.9),
    "S3": (1.5, 0.7, 0.0),
    "S4": (1.2, 0.75, 1.25),
    "S5": (3.84, 0.4, 1.0),
}
"""The point at which each patch carries its label in the drawing."""

VERTICES = {
    "A": (0.0, 0.0, 0.0),
    "B": (4.0, 0.0, 0.0),
    "C": (4.0, 0.0, 2.0),
    "D": (0.0, 0.0, 2.0),
    "T": (0.0, 2.0, 0.0),
}
"""The five corners of the solid."""


class Patch(NamedTuple):
    """One drawn patch of the boundary.

    Attributes:
        name: Short name of the patch, as S1 to S5.
        equation: The equation of the surface, as a text for the product page.
        grid: A function of the subdivision count that returns a point grid of shape (n+1, n+1, 3).
        outward: A function of a point array that returns the unit outward normal.
        area: The area of the patch from an independent integral.
    """

    name: str
    equation: str
    grid: object
    outward: object
    area: float


def grid_bottom(count):
    """Return the point grid of the patch y = 0, with x along the first index."""
    parameter = np.linspace(0.0, 1.0, count + 1)
    x_parameter, z_parameter = np.meshgrid(parameter, parameter, indexing="ij")
    return np.stack([4.0 * x_parameter, np.zeros_like(x_parameter), 2.0 * z_parameter], axis=2)


def grid_back(count):
    """Return the point grid of the patch x = 0, with y along the first index."""
    parameter = np.linspace(0.0, 1.0, count + 1)
    y_parameter, z_parameter = np.meshgrid(parameter, parameter, indexing="ij")
    y = 2.0 * y_parameter
    return np.stack([np.zeros_like(y), y, (2.0 - y) * z_parameter], axis=2)


def grid_floor(count):
    """Return the point grid of the patch z = 0, with y along the first index."""
    parameter = np.linspace(0.0, 1.0, count + 1)
    y_parameter, x_parameter = np.meshgrid(parameter, parameter, indexing="ij")
    y = 2.0 * y_parameter
    return np.stack([(4.0 - y * y) * x_parameter, y, np.zeros_like(y)], axis=2)


def grid_slope(count):
    """Return the point grid of the patch y + z = 2, with y along the first index."""
    parameter = np.linspace(0.0, 1.0, count + 1)
    y_parameter, x_parameter = np.meshgrid(parameter, parameter, indexing="ij")
    y = 2.0 * y_parameter
    return np.stack([(4.0 - y * y) * x_parameter, y, 2.0 - y], axis=2)


def grid_wall(count):
    """Return the point grid of the patch x = 4 - y^2, with y along the first index."""
    parameter = np.linspace(0.0, 1.0, count + 1)
    y_parameter, z_parameter = np.meshgrid(parameter, parameter, indexing="ij")
    y = 2.0 * y_parameter
    x = 4.0 - y * y
    return np.stack([x, y, (2.0 - y) * z_parameter], axis=2)


def outward_bottom(points):
    """Return the unit outward normal of the patch y = 0."""
    return np.tile(np.array([0.0, -1.0, 0.0]), (points.shape[0], 1))


def outward_back(points):
    """Return the unit outward normal of the patch x = 0."""
    return np.tile(np.array([-1.0, 0.0, 0.0]), (points.shape[0], 1))


def outward_floor(points):
    """Return the unit outward normal of the patch z = 0."""
    return np.tile(np.array([0.0, 0.0, -1.0]), (points.shape[0], 1))


def outward_slope(points):
    """Return the unit outward normal of the patch y + z = 2."""
    return np.tile(np.array([0.0, 1.0, 1.0]) / np.sqrt(2.0), (points.shape[0], 1))


def outward_wall(points):
    """Return the unit outward normal of the patch x = 4 - y^2."""
    y = points[:, 1]
    scale = np.sqrt(1.0 + 4.0 * y * y)
    return np.stack([np.ones_like(y), 2.0 * y, np.zeros_like(y)], axis=1) / scale[:, None]


def area_of_slope_patch():
    """Return the area of the patch on the surface y + z = 2 by a one-dimensional integral."""
    value, _ = quad(lambda y: (4.0 - y * y) * np.sqrt(2.0), 0.0, 2.0)
    return float(value)


def area_of_wall_patch():
    """Return the area of the patch on the surface x = 4 - y^2 by a one-dimensional integral."""
    value, _ = quad(lambda y: (2.0 - y) * np.sqrt(1.0 + 4.0 * y * y), 0.0, 2.0)
    return float(value)


def build_patches():
    """Return the five patches of the drawing with an independent area for each patch."""
    return (
        Patch("S1", "y = 0", grid_bottom, outward_bottom, 8.0),
        Patch("S2", "x = 0", grid_back, outward_back, 2.0),
        Patch("S3", "z = 0", grid_floor, outward_floor, 16.0 / 3.0),
        Patch("S4", "y + z = 2", grid_slope, outward_slope, area_of_slope_patch()),
        Patch("S5", "x = 4 - y^2", grid_wall, outward_wall, area_of_wall_patch()),
    )


def triangulate(grid, count):
    """Return the triangle list of one point grid, without the triangles of zero area.

    Args:
        grid: The point grid of shape (count + 1, count + 1, 3).
        count: The count of the subdivisions of the grid.

    Returns:
        An array of shape (m, 3, 3) that holds m triangles, each as three points.
    """
    triangles = []
    for first in range(count):
        for second in range(count):
            corner_00 = grid[first, second]
            corner_10 = grid[first + 1, second]
            corner_11 = grid[first + 1, second + 1]
            corner_01 = grid[first, second + 1]
            triangles.append((corner_00, corner_10, corner_11))
            triangles.append((corner_00, corner_11, corner_01))
    array = np.array(triangles, dtype=float)
    edge_a = array[:, 1] - array[:, 0]
    edge_b = array[:, 2] - array[:, 0]
    doubled_area = np.linalg.norm(np.cross(edge_a, edge_b), axis=1)
    return array[doubled_area > 1.0e-13]


def build_mesh():
    """Return the mesh of the solid, with the patch name of each triangle and its area.

    Returns:
        A tuple of the triangle array, the patch name of each triangle, and the grid count.
    """
    patches = build_patches()
    all_triangles = []
    all_names = []
    for patch in patches:
        grid = patch.grid(SUBDIVISION)
        triangles = triangulate(grid, SUBDIVISION)
        all_triangles.append(triangles)
        all_names.extend([patch.name] * len(triangles))
    return np.concatenate(all_triangles, axis=0), all_names


def orient_outward(triangles, names):
    """Return the triangles with an outward orientation and the patch of each triangle.

    Args:
        triangles: The triangle array of shape (m, 3, 3).
        names: The patch name of each triangle.

    Returns:
        A tuple of the outward triangle array and the outward normal of each triangle.
    """
    patches = {patch.name: patch for patch in build_patches()}
    oriented = triangles.copy()
    for index, name in enumerate(names):
        triangle = oriented[index]
        normal = np.cross(triangle[1] - triangle[0], triangle[2] - triangle[0])
        centroid = triangle.mean(axis=0)
        outward = patches[name].outward(centroid[None, :])[0]
        if float(np.dot(normal, outward)) < 0.0:
            oriented[index] = triangle[[0, 2, 1]]
    normals = np.cross(oriented[:, 1] - oriented[:, 0], oriented[:, 2] - oriented[:, 0])
    return oriented, normals


def volume_from_mesh(triangles, normals):
    """Return the volume of the closed mesh by the divergence theorem.

    Args:
        triangles: The outward triangle array.
        normals: The vector that equals twice the area times the unit normal of each triangle.

    Returns:
        The volume of the mesh as a float.
    """
    centroids = triangles.mean(axis=1)
    flux = np.sum(centroids * normals, axis=1) / 2.0
    return float(np.sum(flux) / 3.0)


def volume_from_slices():
    """Return the volume of the region from the integral of the area of the horizontal cut."""
    value, _ = quad(lambda height: (4.0 - height * height) * (2.0 - height), 0.0, 2.0)
    return float(value)


def volume_from_iterated_integral():
    """Return the volume of the region from the iterated integral of the problem page."""
    value, _ = tplquad(
        lambda y, z, x: 1.0,
        0.0,
        2.0,
        lambda y: 0.0,
        lambda y: 2.0 - y,
        lambda y, z: 0.0,
        lambda y, z: 4.0 - y * y,
    )
    return float(value)


def count_boundary_edges(triangles):
    """Return the count of the mesh edges that belong to one triangle only.

    Args:
        triangles: The triangle array of shape (m, 3, 3).

    Returns:
        A tuple of the count of the boundary edges and the list of those edges.
    """
    counts = {}
    for triangle in triangles:
        keys = [tuple(np.round(point, 9)) for point in triangle]
        for first in range(3):
            second = (first + 1) % 3
            edge = tuple(sorted((keys[first], keys[second])))
            counts[edge] = counts.get(edge, 0) + 1
    boundary = [edge for edge, count in counts.items() if count == 1]
    return len(boundary), boundary


def cut_area_from_mesh(triangles, names, height):
    """Return the area of the horizontal cut of the mesh at one height.

    The cut is bounded by four segments.  Two of them lie on the patch z = 0 and on the patch
    x = 0.  This function measures the two lengths from the crossing points of the mesh edges,
    so the area comes from the drawing and not from the pair of limits.

    Args:
        triangles: The triangle array of shape (m, 3, 3).
        names: The patch name of each triangle.
        height: The height of the cut.

    Returns:
        The area of the cut of the drawn mesh as a float.
    """
    points_on_floor = []
    points_on_back = []
    for index, triangle in enumerate(triangles):
        name = names[index]
        if name not in ("S2", "S3"):
            continue
        for first in range(3):
            second = (first + 1) % 3
            start = triangle[first]
            end = triangle[second]
            span = end[1] - start[1]
            if span == 0.0:
                continue
            if (start[1] - height) * (end[1] - height) <= 0.0:
                weight = (height - start[1]) / span
                point = start + weight * (end - start)
                if name == "S3":
                    points_on_floor.append(point)
                else:
                    points_on_back.append(point)
    floor_points = np.array(points_on_floor, dtype=float).reshape(-1, 3)
    back_points = np.array(points_on_back, dtype=float).reshape(-1, 3)
    if floor_points.size == 0 or back_points.size == 0:
        raise ValueError(f"no mesh edge crosses the plane y = {height}")
    length_x = float(floor_points[:, 0].max() - floor_points[:, 0].min())
    length_z = float(back_points[:, 2].max() - back_points[:, 2].min())
    return length_x * length_z


def projection_test(generator):
    """Check the projection of the solid on the xz-plane against the rectangle of the limits.

    Args:
        generator: The pseudo-random generator of the module.

    Returns:
        A dictionary with the mesh extent, the fraction of the rectangle that the solid covers,
        and the area of the rectangle that a disk of radius 2 does not hold.
    """
    x = 4.0 * generator.random(PROJECTION_SAMPLE_COUNT)
    z = 2.0 * generator.random(PROJECTION_SAMPLE_COUNT)
    reachable_height = np.minimum(np.minimum(2.0, 2.0 - z), np.sqrt(np.maximum(4.0 - x, 0.0)))
    covered = reachable_height >= 0.0
    outside_disk = (x * x + z * z) > 4.0
    return {
        "covered_fraction": float(np.count_nonzero(covered)) / float(PROJECTION_SAMPLE_COUNT),
        "area_outside_disk": 8.0 * float(np.count_nonzero(covered & outside_disk)) / float(
            PROJECTION_SAMPLE_COUNT
        ),
        "sample_count": PROJECTION_SAMPLE_COUNT,
    }


def check_labels():
    """Check each label point against the equation of the surface that it names.

    Returns:
        A list of records, one for each label point.
    """
    patches = build_patches()
    residuals = {
        "S1": lambda points: -points[:, 1],
        "S2": lambda points: -points[:, 0],
        "S3": lambda points: -points[:, 2],
        "S4": lambda points: (points[:, 1] + points[:, 2] - 2.0) / np.sqrt(2.0),
        "S5": lambda points: (points[:, 0] + points[:, 1] ** 2 - 4.0)
        / np.sqrt(1.0 + 4.0 * points[:, 1] ** 2),
    }
    records = []
    for patch in patches:
        point = np.array([LABEL_POINTS[patch.name]])
        own = float(abs(residuals[patch.name](point)[0]))
        others = {
            key: float(abs(function(point)[0]))
            for key, function in residuals.items()
            if key != patch.name
        }
        x, y, z = LABEL_POINTS[patch.name]
        inside = (
            x >= 0.0
            and z >= 0.0
            and y >= 0.0
            and y + z <= 2.0
            and x + y * y <= 4.0
        )
        records.append(
            {
                "name": patch.name,
                "equation": patch.equation,
                "point": list(LABEL_POINTS[patch.name]),
                "residual_on_own_surface": own,
                "nearest_other_surface": min(others.values()),
                "inside_region": bool(inside),
            }
        )
    return records


def main():
    """Run every check of part 4 and write the record of the checked values."""
    generator = np.random.default_rng(RANDOM_SEED)
    triangles, names = build_mesh()
    oriented, normals = orient_outward(triangles, names)

    mesh_volume = volume_from_mesh(oriented, normals)
    slice_volume = volume_from_slices()
    iterated_volume = volume_from_iterated_integral()

    boundary_count, boundary_edges = count_boundary_edges(oriented)

    area_records = []
    print("part 4 checks: the area of each drawn patch")
    for patch in build_patches():
        selected = oriented[np.array(names) == patch.name]
        edge_a = selected[:, 1] - selected[:, 0]
        edge_b = selected[:, 2] - selected[:, 0]
        mesh_area = float(np.sum(np.linalg.norm(np.cross(edge_a, edge_b), axis=1)) / 2.0)
        relative_gap = abs(mesh_area - patch.area) / patch.area
        area_records.append(
            {
                "name": patch.name,
                "equation": patch.equation,
                "mesh_area": mesh_area,
                "integral_area": patch.area,
                "relative_gap": relative_gap,
            }
        )
        print(
            f"{patch.name} {patch.equation:14s} mesh {mesh_area:.6f} integral {patch.area:.6f} "
            f"relative gap {relative_gap:.2e}"
        )

    print("part 4 checks: the volume of the closed mesh")
    print(f"mesh volume      : {mesh_volume:.12f}")
    print(f"volume of slices : {slice_volume:.12f}")
    print(f"iterated integral: {iterated_volume:.12f}")
    print(f"relative gap     : {abs(mesh_volume - slice_volume) / slice_volume:.3e}")
    print(f"boundary edges   : {boundary_count}")

    print("part 4 checks: the cut of the drawn mesh")
    cut_records = []
    for height in HEIGHTS_OF_CHECK:
        drawn = cut_area_from_mesh(oriented, names, height)
        expected = (4.0 - height * height) * (2.0 - height)
        relative_gap = abs(drawn - expected) / expected
        cut_records.append(
            {
                "height": height,
                "drawn_area": drawn,
                "area_from_limits": expected,
                "relative_gap": relative_gap,
            }
        )
        print(
            f"height {height:.2f}: drawn {drawn:.6f} limits {expected:.6f} "
            f"relative gap {relative_gap:.2e}"
        )

    projection = projection_test(generator)
    print(f"projection covered fraction: {projection['covered_fraction']:.6f}")
    print(f"projection area outside a disk of radius 2: {projection['area_outside_disk']:.6f}")

    labels = check_labels()
    print("part 4 checks: the label points")
    for record in labels:
        print(
            f"{record['name']} {record['equation']:14s} point {record['point']} "
            f"residual {record['residual_on_own_surface']:.3e} "
            f"nearest other {record['nearest_other_surface']:.3f} "
            f"inside {record['inside_region']}"
        )

    assert boundary_count == 0, f"the mesh is not closed: {boundary_count} boundary edges"
    assert abs(mesh_volume - slice_volume) / slice_volume < 5.0e-3, (
        "the volume of the mesh disagrees with the volume of the cuts"
    )
    assert abs(slice_volume - iterated_volume) < 1.0e-9, (
        "the iterated integral disagrees with the volume of the cuts"
    )
    for record in area_records:
        assert record["relative_gap"] < 5.0e-3, (
            f"the drawn area of {record['name']} disagrees with the integral"
        )
    for record in cut_records:
        assert record["relative_gap"] < 5.0e-3, (
            f"the drawn cut at y = {record['height']} disagrees with the limits"
        )
    assert projection["covered_fraction"] == 1.0, (
        "the projection does not cover the rectangle of the limits"
    )
    assert projection["area_outside_disk"] > 1.5, (
        "the projection is not distinguishable from a disk of radius 2"
    )
    for record in labels:
        assert record["residual_on_own_surface"] < 1.0e-12, (
            f"the label of {record['name']} does not lie on its own surface"
        )
        assert record["inside_region"], f"the label of {record['name']} is outside the region"
        assert record["nearest_other_surface"] > 0.05, (
            f"the label of {record['name']} also lies on another surface"
        )

    output = {
        "subdivision": SUBDIVISION,
        "triangle_count": int(oriented.shape[0]),
        "boundary_edge_count": boundary_count,
        "volume": {
            "mesh": mesh_volume,
            "slices": slice_volume,
            "iterated_integral": iterated_volume,
            "relative_gap": abs(mesh_volume - slice_volume) / slice_volume,
        },
        "areas": area_records,
        "cuts": cut_records,
        "projection": projection,
        "labels": labels,
        "vertices": {name: list(point) for name, point in VERTICES.items()},
    }
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"record written to {RESULT_PATH}")
    print("part 4: all checks passed")


if __name__ == "__main__":
    main()
