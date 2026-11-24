"""Geometry of the solid E of Exercise 15.7.32 of Calculus, Early Transcendentals.

The solid E is bounded by four planes. This module derives its vertices, its faces,
its coordinate projections, and its volume. Every function returns a value that an
independent method can check.

Constants:
    PLANE_ROWS: The four boundary planes, each as a name, a normal vector, and a right side.
    BOX_LOWER: The lower corner of the axis-aligned box that contains E.
    BOX_UPPER: The upper corner of the axis-aligned box that contains E.
"""

from fractions import Fraction
import itertools

import numpy as np

PLANE_ROWS = (
    ("x = 2", np.array([1.0, 0.0, 0.0]), 2.0),
    ("y = 2", np.array([0.0, 1.0, 0.0]), 2.0),
    ("z = 0", np.array([0.0, 0.0, 1.0]), 0.0),
    ("x + y - 2z = 2", np.array([1.0, 1.0, -2.0]), 2.0),
)

BOX_LOWER = np.array([0.0, 0.0, 0.0])
BOX_UPPER = np.array([2.0, 2.0, 1.0])


def vertex_from_three_planes(first_index, second_index, third_index):
    """Return the point where three of the four planes meet.

    Args:
        first_index: The index of the first plane in PLANE_ROWS.
        second_index: The index of the second plane in PLANE_ROWS.
        third_index: The index of the third plane in PLANE_ROWS.

    Returns:
        The intersection point as a float array of shape (3,).
    """
    rows = [PLANE_ROWS[index] for index in (first_index, second_index, third_index)]
    matrix = np.array([row[1] for row in rows])
    right_side = np.array([row[2] for row in rows])
    return np.linalg.solve(matrix, right_side)


def all_vertices():
    """Return the four points where three of the four planes meet.

    Returns:
        A list of four float arrays. The order follows the omitted plane index.
    """
    return [vertex_from_three_planes(*triple) for triple in itertools.combinations(range(4), 3)]


HALF_SPACE_TOLERANCE = 1e-12


def contains(points):
    """Test whether each point lies in E given by the four half-spaces.

    The four half-spaces are x <= 2, y <= 2, z >= 0, and x + y - 2z >= 2.

    Args:
        points: An array of shape (n, 3) of points to test.

    Returns:
        A boolean array of shape (n,), true where the point lies in E.
    """
    points = np.atleast_2d(np.asarray(points, dtype=float))
    x_value = points[:, 0]
    y_value = points[:, 1]
    z_value = points[:, 2]
    return (
        (x_value <= 2.0 + HALF_SPACE_TOLERANCE)
        & (y_value <= 2.0 + HALF_SPACE_TOLERANCE)
        & (z_value >= -HALF_SPACE_TOLERANCE)
        & (x_value + y_value - 2.0 * z_value >= 2.0 - HALF_SPACE_TOLERANCE)
    )


def determinant_volume(vertices):
    """Return the volume of the tetrahedron with the given four vertices.

    The volume is one sixth of the absolute value of the determinant of the three
    edge vectors. All vertices have integer coordinates, so the result is exact.

    Args:
        vertices: A list of four integer points.

    Returns:
        The volume as a Fraction.
    """
    origin = np.array(vertices[0], dtype=object)
    edge_one = np.array(vertices[1], dtype=object) - origin
    edge_two = np.array(vertices[2], dtype=object) - origin
    edge_three = np.array(vertices[3], dtype=object) - origin
    determinant = (
        edge_one[0] * (edge_two[1] * edge_three[2] - edge_two[2] * edge_three[1])
        - edge_one[1] * (edge_two[0] * edge_three[2] - edge_two[2] * edge_three[0])
        + edge_one[2] * (edge_two[0] * edge_three[1] - edge_two[1] * edge_three[0])
    )
    return Fraction(int(abs(determinant)), 6)


def shoelace_area(corners):
    """Return the area of a polygon in the plane from its corner list.

    Args:
        corners: A list of two-dimensional corners in counter-clockwise or clockwise order.

    Returns:
        The area as a Fraction.
    """
    total = Fraction(0)
    count = len(corners)
    for index in range(count):
        first = corners[index]
        second = corners[(index + 1) % count]
        total += Fraction(int(first[0])) * Fraction(int(second[1]))
        total -= Fraction(int(second[0])) * Fraction(int(first[1]))
    return abs(total) / 2


def monte_carlo_volume(sample_count, seed):
    """Estimate the volume of E by uniform sampling in the bounding box.

    Args:
        sample_count: The number of random points.
        seed: The random seed of the reported result.

    Returns:
        A tuple of the estimate, its standard error, and the sampled fraction.
    """
    generator = np.random.default_rng(seed)
    lower = BOX_LOWER
    upper = BOX_UPPER
    points = generator.uniform(lower, upper, size=(sample_count, 3))
    inside = contains(points)
    box_volume = float(np.prod(upper - lower))
    fraction = float(np.count_nonzero(inside)) / sample_count
    estimate = box_volume * fraction
    standard_error = box_volume * float(np.sqrt(fraction * (1.0 - fraction) / sample_count))
    return estimate, standard_error, fraction


def plane_side_value(point):
    """Return the value of x + y - 2z at a point.

    Args:
        point: A point as a length-three sequence.

    Returns:
        The value x + y - 2z as a float.
    """
    return float(point[0] + point[1] - 2.0 * point[2])
