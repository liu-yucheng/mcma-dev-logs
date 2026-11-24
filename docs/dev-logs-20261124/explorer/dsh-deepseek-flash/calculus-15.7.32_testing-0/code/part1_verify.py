"""Verification of Part 1, the solid E.

This script derives the vertices, the faces, the coordinate projections, and the volume
of the solid E. It compares each value with a value of a different method.

Run: code/.venv/Scripts/python.exe code/part1_verify.py
"""

import os
import sys
from fractions import Fraction

import numpy as np
import sympy
from scipy.optimize import linprog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import orders
import solid
from verify_common import as_text, check, record

SEED = 20261123
SAMPLE_COUNT = 4_000_000
PROJECTION_CORNERS = {
    "xy": [(2, 0), (0, 2), (2, 2)],
    "xz": [(0, 0), (2, 0), (2, 1)],
    "yz": [(0, 0), (2, 0), (2, 1)],
}


def inequality_matrix():
    """Return the matrix and the right side of the four half-spaces of E.

    Returns:
        A tuple of a 4 by 3 float array and a length-four float array.
    """
    matrix = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, -1.0],
            [-1.0, -1.0, 2.0],
        ]
    )
    right_side = np.array([2.0, 2.0, 0.0, -2.0])
    return matrix, right_side


def extreme_point(direction, equality_row=None, equality_value=None):
    """Return one optimal point of a linear program over E.

    Args:
        direction: A length-three float array for the objective.
        equality_row: An optional length-three float array of one equality constraint.
        equality_value: The right side of the equality constraint.

    Returns:
        A tuple of the optimal value and the optimal point.
    """
    matrix, right_side = inequality_matrix()
    if equality_row is None:
        result = linprog(direction, A_ub=matrix, b_ub=right_side, bounds=None, method="highs")
    else:
        result = linprog(
            direction,
            A_ub=matrix,
            b_ub=right_side,
            A_eq=[equality_row],
            b_eq=[equality_value],
            bounds=None,
            method="highs",
        )
    return float(result.fun), result.x


def face_area_from_vectors(vertices):
    """Return the area of a triangle from three vertices by the cross product.

    Args:
        vertices: A list of three points.

    Returns:
        The area as a float.
    """
    first = np.array(vertices[1], dtype=float) - np.array(vertices[0], dtype=float)
    second = np.array(vertices[2], dtype=float) - np.array(vertices[0], dtype=float)
    return float(np.linalg.norm(np.cross(first, second))) / 2.0


def projection_membership(name, samples):
    """Return the mask of the points of a coordinate plane that lie in the projection.

    Args:
        name: The name of the plane, one of "xy", "xz", and "yz".
        samples: An array of shape (n, 2) of points of that plane.

    Returns:
        A boolean array of shape (n,).
    """
    first = samples[:, 0]
    second = samples[:, 1]
    if name == "xy":
        return (first + second >= 2.0) & (first <= 2.0) & (second <= 2.0)
    return second <= first / 2.0


def main():
    """Derive the geometry of E and write the record of Part 1."""
    checks = []
    values = {}

    vertices = solid.all_vertices()
    rounded = [tuple(int(round(component)) for component in point) for point in vertices]
    values["vertex_list"] = ", ".join("(%d, %d, %d)" % point for point in rounded)
    values["vertex_count"] = len(rounded)

    membership = solid.contains(np.array(vertices))
    checks.append(check("four vertices satisfy all four half-spaces", int(np.count_nonzero(membership)), 4))
    distinct = len({tuple(np.round(point, 9)) for point in vertices})
    checks.append(check("four distinct vertices from the four plane triples", distinct, 4))

    interior = np.array([1.5, 1.5, 0.25])
    checks.append(check("the centroid (1.5, 1.5, 0.25) lies in E", int(np.count_nonzero(solid.contains(interior))), 1))

    volume_determinant = float(solid.determinant_volume(rounded))
    base_area = solid.shoelace_area([(2, 2), (2, 0), (0, 2)])
    height = 1
    volume_pyramid = float(Fraction(int(base_area)) * height / 3)
    volume_calculus = float(orders.symbolic_value("dz dx dy", sympy.Integer(1)))
    volume_monte_carlo, standard_error, fraction = solid.monte_carlo_volume(SAMPLE_COUNT, SEED)
    volume_fraction = Fraction(int(base_area)) * height / 3

    checks.append(check("volume by determinant against volume by pyramid formula", volume_determinant, volume_pyramid))
    checks.append(
        check("volume by iterated integral against volume by pyramid formula", volume_calculus, volume_pyramid)
    )
    checks.append(
        check(
            "volume by Monte Carlo against volume by pyramid formula, four standard errors",
            volume_monte_carlo,
            volume_pyramid,
            4.0 * standard_error,
        )
    )

    box_volume = 4.0
    wrong_side_volume = box_volume - volume_pyramid
    volume_without_third = float(int(base_area) * height)
    checks.append(
        check(
            "wrong side of the slanted plane: its volume differs from the volume of E",
            wrong_side_volume,
            volume_pyramid,
            comparison="differ",
        )
    )
    checks.append(
        check(
            "base times height without the factor one third differs from the volume of E",
            volume_without_third,
            volume_pyramid,
            comparison="differ",
        )
    )

    minimum_x, point_minimum_x = extreme_point(np.array([1.0, 0.0, 0.0]))
    maximum_x = -extreme_point(np.array([-1.0, 0.0, 0.0]))[0]
    minimum_y, _ = extreme_point(np.array([0.0, 1.0, 0.0]))
    maximum_y = -extreme_point(np.array([0.0, -1.0, 0.0]))[0]
    z_largest = -extreme_point(np.array([0.0, 0.0, -1.0]))[0]
    checks.append(check("smallest x over E by linear programming", minimum_x, 0.0, 1e-9))
    checks.append(check("largest x over E by linear programming", maximum_x, 2.0, 1e-9))
    checks.append(check("smallest y over E by linear programming", minimum_y, 0.0, 1e-9))
    checks.append(check("largest y over E by linear programming", maximum_y, 2.0, 1e-9))
    checks.append(check("largest z over E by linear programming", z_largest, 1.0, 1e-9))

    equality = np.array([1.0, 0.0, 0.0])
    y_on_x_zero_small = extreme_point(np.array([0.0, 1.0, 0.0]), equality, 0.0)[0]
    y_on_x_zero_large = -extreme_point(np.array([0.0, -1.0, 0.0]), equality, 0.0)[0]
    z_on_x_zero_large = -extreme_point(np.array([0.0, 0.0, -1.0]), equality, 0.0)[0]
    checks.append(check("in the plane x = 0 the smallest y equals 2", y_on_x_zero_small, 2.0, 1e-9))
    checks.append(check("in the plane x = 0 the largest y equals 2", y_on_x_zero_large, 2.0, 1e-9))
    checks.append(check("in the plane x = 0 the largest z equals 0", z_on_x_zero_large, 0.0, 1e-9))

    equality = np.array([0.0, 1.0, 0.0])
    x_on_y_zero_small = extreme_point(np.array([1.0, 0.0, 0.0]), equality, 0.0)[0]
    x_on_y_zero_large = -extreme_point(np.array([-1.0, 0.0, 0.0]), equality, 0.0)[0]
    z_on_y_zero_large = -extreme_point(np.array([0.0, 0.0, -1.0]), equality, 0.0)[0]
    checks.append(check("in the plane y = 0 the smallest x equals 2", x_on_y_zero_small, 2.0, 1e-9))
    checks.append(check("in the plane y = 0 the largest x equals 2", x_on_y_zero_large, 2.0, 1e-9))
    checks.append(check("in the plane y = 0 the largest z equals 0", z_on_y_zero_large, 0.0, 1e-9))

    generator = np.random.default_rng(SEED + 1)
    for name, corners in PROJECTION_CORNERS.items():
        exact_area = solid.shoelace_area(corners)
        samples = generator.uniform([0.0, 0.0], [2.0, 2.0], size=(SAMPLE_COUNT, 2))
        inside = projection_membership(name, samples)
        sampled_area = 4.0 * float(np.count_nonzero(inside)) / SAMPLE_COUNT
        values["projection_%s_area" % name] = float(exact_area)
        values["projection_%s_corners" % name] = ", ".join("(%d, %d)" % corner for corner in corners)
        checks.append(
            check(
                "projection on the %s plane: corner list against sampling" % name,
                float(exact_area),
                sampled_area,
                0.01,
            )
        )

    face_z_zero = face_area_from_vectors([(2, 2, 0), (2, 0, 0), (0, 2, 0)])
    face_x_two = face_area_from_vectors([(2, 2, 0), (2, 0, 0), (2, 2, 1)])
    face_y_two = face_area_from_vectors([(2, 2, 0), (0, 2, 0), (2, 2, 1)])
    face_slanted = face_area_from_vectors([(2, 0, 0), (0, 2, 0), (2, 2, 1)])
    projected_slanted = float(solid.shoelace_area(PROJECTION_CORNERS["xy"]))
    normal_length = float(np.linalg.norm(np.array([1.0, 1.0, -2.0])))
    slanted_by_projection = projected_slanted * normal_length / 2.0
    checks.append(
        check("slanted face: cross product against the projection rule", face_slanted, slanted_by_projection, 1e-12)
    )
    checks.append(check("face in the plane z = 0 against the base area", face_z_zero, float(base_area)))

    values["volume"] = volume_pyramid
    values["volume_latex"] = r"\frac{%d}{%d}" % (volume_fraction.numerator, volume_fraction.denominator)
    values["volume_text"] = "%.12g" % volume_pyramid
    values["volume_mc"] = as_text(volume_monte_carlo)
    values["volume_mc_error"] = as_text(standard_error)
    values["volume_without_third"] = as_text(volume_without_third)
    values["wrong_side_volume"] = as_text(wrong_side_volume)
    values["slanted_face_area"] = as_text(face_slanted)
    values["face_z_zero_area"] = as_text(face_z_zero)
    values["face_x_two_area"] = as_text(face_x_two)
    values["face_y_two_area"] = as_text(face_y_two)
    values["z_largest"] = as_text(z_largest)
    values["z_on_x_zero_large"] = as_text(0.0 if abs(z_on_x_zero_large) < 1e-12 else z_on_x_zero_large)
    values["sample_count"] = SAMPLE_COUNT
    values["seed"] = SEED
    values["box_volume"] = box_volume
    values["base_area"] = int(base_area)
    values["height"] = height
    values["centroid"] = "(1.5, 1.5, 0.25)"
    values["sampled_fraction"] = as_text(fraction)

    record(1, values, checks)


if __name__ == "__main__":
    main()
