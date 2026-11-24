"""Exact geometry of the solid of Exercise 15.7.27.

The solid is the set of points that the iterated integral describes:

    R = {(x, y, z) : 0 <= x <= 1, 0 <= z <= 1 - x, 0 <= y <= 2 - 2 z}.

The module stores that set as six half-spaces, clips a polygon with exact
fractions, and derives the vertices, the faces, the section areas, and the
volume. Every number of the tutorial comes from one of these functions, so the
tutorial never copies a value by hand.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Sequence

Point = tuple[Fraction, Fraction, Fraction]
Point2 = tuple[Fraction, Fraction]
HalfSpace = tuple[str, Point, Fraction]
Polygon = list[Point2]
Polynomial = list[Fraction]

AXIS_INDEX: dict[str, int] = {"x": 0, "y": 1, "z": 2}
"""Index of each coordinate in a point tuple."""

PLANE_AXES: dict[str, tuple[str, str]] = {
    "x": ("z", "y"),
    "y": ("x", "z"),
    "z": ("x", "y"),
}
"""The two coordinates of a slice, in the order (horizontal, vertical)."""

CLIP_LIMIT = Fraction(8)
"""Half width of the square that starts every polygon clip."""

SOLID_HALF_SPACES: tuple[HalfSpace, ...] = (
    ("x is not below 0", (Fraction(-1), Fraction(0), Fraction(0)), Fraction(0)),
    ("x is not above 1", (Fraction(1), Fraction(0), Fraction(0)), Fraction(1)),
    ("z is not below 0", (Fraction(0), Fraction(0), Fraction(-1)), Fraction(0)),
    ("z is not above 1 - x", (Fraction(1), Fraction(0), Fraction(1)), Fraction(1)),
    ("y is not below 0", (Fraction(0), Fraction(-1), Fraction(0)), Fraction(0)),
    ("y is not above 2 - 2 z", (Fraction(0), Fraction(1), Fraction(2)), Fraction(2)),
)
"""The six half-spaces a . p <= d that the three pairs of limits describe."""

LIMIT_LOWER: dict[str, Fraction] = {"x": Fraction(0), "y": Fraction(0), "z": Fraction(0)}
"""Lower limit of each variable. Each lower limit is the constant 0."""


def dot(coefficients: Sequence[Fraction], point: Sequence[Fraction]) -> Fraction:
    """Return the scalar product of a coefficient triple and a point."""
    return sum(coefficient * value for coefficient, value in zip(coefficients, point))


def contains(point: Sequence[Fraction]) -> bool:
    """Return True when a point satisfies all six half-spaces of the solid."""
    return all(dot(coefficients, point) <= bound for _, coefficients, bound in SOLID_HALF_SPACES)


def contains_by_limits(point: Sequence[Fraction]) -> bool:
    """Return True when a point satisfies the three pairs of limits in order.

    This test reads the limits exactly as the integral prints them: the pair of
    x, then the pair of z, then the pair of y. It is a second method beside
    `contains`, which reads the six half-spaces of the closed form.
    """
    x, y, z = point
    if not (Fraction(0) <= x <= Fraction(1)):
        return False
    if not (Fraction(0) <= z <= 1 - x):
        return False
    return Fraction(0) <= y <= 2 - 2 * z


def inner_upper_limit(x: Fraction, z: Fraction) -> Fraction:
    """Return the upper limit of y, which is 2 - 2 z and holds no x."""
    del x
    return 2 - 2 * z


def middle_upper_limit(x: Fraction, z: Fraction) -> Fraction:
    """Return the upper limit of z, which is 1 - x and holds no y."""
    del z
    return 1 - x


def outer_upper_limit(x: Fraction, y: Fraction) -> Fraction:
    """Return the upper limit of x, which is the constant 1."""
    del x, y
    return Fraction(1)


def clip_polygon_by_half_space(
    polygon: Polygon,
    coefficients: tuple[Fraction, Fraction],
    bound: Fraction,
) -> Polygon:
    """Clip a convex polygon by the half plane `coefficients . p <= bound`.

    Uses the Sutherland-Hodgman walk with exact fraction arithmetic, so a
    clipped vertex stays exact and never moves by a rounding error.
    """
    if not polygon:
        return []
    clipped: Polygon = []
    count = len(polygon)
    for index in range(count):
        current = polygon[index]
        following = polygon[(index + 1) % count]
        current_value = coefficients[0] * current[0] + coefficients[1] * current[1]
        following_value = coefficients[0] * following[0] + coefficients[1] * following[1]
        current_inside = current_value <= bound
        following_inside = following_value <= bound
        if current_inside:
            clipped.append(current)
        if current_inside != following_inside:
            share = (bound - current_value) / (following_value - current_value)
            crossing = (
                current[0] + share * (following[0] - current[0]),
                current[1] + share * (following[1] - current[1]),
            )
            clipped.append(crossing)
    return clipped


def slice_polygon(axis: str, value: Fraction) -> Polygon:
    """Return the polygon of the solid in the plane `axis = value`.

    The returned points use the two coordinates of `PLANE_AXES[axis]`, in that
    order. An empty list means that the plane misses the solid.
    """
    horizontal_axis, vertical_axis = PLANE_AXES[axis]
    horizontal_index = AXIS_INDEX[horizontal_axis]
    vertical_index = AXIS_INDEX[vertical_axis]
    fixed_index = AXIS_INDEX[axis]
    limit = CLIP_LIMIT
    polygon: Polygon = [
        (-limit, -limit),
        (limit, -limit),
        (limit, limit),
        (-limit, limit),
    ]
    for _, coefficients, bound in SOLID_HALF_SPACES:
        remaining = bound - coefficients[fixed_index] * value
        plane_coefficients = (
            coefficients[horizontal_index],
            coefficients[vertical_index],
        )
        if plane_coefficients == (Fraction(0), Fraction(0)):
            if Fraction(0) > remaining:
                return []
            continue
        polygon = clip_polygon_by_half_space(polygon, plane_coefficients, remaining)
        if not polygon:
            return []
    return remove_repeated_points(polygon)


def remove_repeated_points(polygon: Polygon) -> Polygon:
    """Drop a point that equals its neighbour, and drop a point of a straight edge."""
    cleaned: Polygon = []
    for point in polygon:
        if cleaned and point == cleaned[-1]:
            continue
        cleaned.append(point)
    if len(cleaned) > 1 and cleaned[0] == cleaned[-1]:
        cleaned.pop()
    if len(cleaned) < 3:
        return cleaned
    without_collinear: Polygon = []
    count = len(cleaned)
    for index in range(count):
        previous = cleaned[index - 1]
        current = cleaned[index]
        following = cleaned[(index + 1) % count]
        first_edge = (current[0] - previous[0], current[1] - previous[1])
        second_edge = (following[0] - current[0], following[1] - current[1])
        cross = first_edge[0] * second_edge[1] - first_edge[1] * second_edge[0]
        if cross != 0:
            without_collinear.append(current)
    return without_collinear


def polygon_area(polygon: Polygon) -> Fraction:
    """Return the area of a simple polygon by the shoelace formula."""
    if len(polygon) < 3:
        return Fraction(0)
    total = Fraction(0)
    count = len(polygon)
    for index in range(count):
        current = polygon[index]
        following = polygon[(index + 1) % count]
        total += current[0] * following[1] - following[0] * current[1]
    return abs(total) / 2


def describe_polygon(polygon: Polygon) -> dict[str, object]:
    """Return the vertex count, the parallel side pairs, and the right angles.

    A rectangle has two pairs of parallel sides and four right angles. A
    trapezoid has one pair of parallel sides and no right angle in this
    problem. The tutorial takes the name of each cross section from this
    report, so the name follows the inequalities and not the drawing.
    """
    if len(polygon) < 3:
        return {"vertex_count": len(polygon), "parallel_pairs": 0, "right_angles": 0, "edges": []}
    count = len(polygon)
    edges: list[tuple[Fraction, Fraction]] = []
    for index in range(count):
        current = polygon[index]
        following = polygon[(index + 1) % count]
        edges.append((following[0] - current[0], following[1] - current[1]))
    parallel_pairs = 0
    for first in range(count):
        for second in range(first + 1, count):
            cross = edges[first][0] * edges[second][1] - edges[first][1] * edges[second][0]
            if cross == 0:
                parallel_pairs += 1
    right_angles = 0
    for index in range(count):
        current = polygon[index]
        following = polygon[(index + 1) % count]
        third = polygon[(index + 2) % count]
        first_edge = (following[0] - current[0], following[1] - current[1])
        second_edge = (third[0] - following[0], third[1] - following[1])
        if first_edge[0] * second_edge[0] + first_edge[1] * second_edge[1] == 0:
            right_angles += 1
    return {
        "vertex_count": count,
        "parallel_pairs": parallel_pairs,
        "right_angles": right_angles,
        "edges": edges,
    }


def name_polygon(report: dict[str, object]) -> str:
    """Return the plane-figure name that the counts of a polygon report give."""
    vertex_count = int(report["vertex_count"])
    parallel_pairs = int(report["parallel_pairs"])
    right_angles = int(report["right_angles"])
    if vertex_count < 3:
        return "degenerate"
    if vertex_count == 3:
        return "triangle"
    if vertex_count == 4 and parallel_pairs == 2 and right_angles == 4:
        return "rectangle"
    if vertex_count == 4 and parallel_pairs == 1:
        return "trapezoid"
    return "quadrilateral"


def section_area_from_formula(axis: str, value: Fraction) -> Fraction:
    """Return the closed-form area of the slice at `axis = value`.

    Only the variables that the slice keeps may appear, so the closed forms are:

    - z fixed: (1 - z) (2 - 2 z), the product of a width and a height.
    - x fixed: 1 - x ** 2, the trapezoid with parallel sides 2 and 2 x.
    - y fixed: 1 / 2 - y ** 2 / 8, the trapezoid with parallel sides 1 and 1 - y / 2.
    """
    if axis == "z":
        return (1 - value) * (2 - 2 * value)
    if axis == "x":
        return 1 - value**2
    if axis == "y":
        return Fraction(1, 2) - value**2 / 8
    raise ValueError(f"unknown axis {axis}")


def section_area_from_polygon(axis: str, value: Fraction) -> Fraction:
    """Return the area of the slice at `axis = value` with polygon clipping."""
    return polygon_area(slice_polygon(axis, value))


def section_area_from_grid(axis: str, value: Fraction, count: int = 800) -> float:
    """Return the area of a slice by the midpoint rule on a square grid.

    This method is independent of both the closed form and the clipping walk.
    It counts the grid cells whose centre satisfies the three pairs of limits.
    """
    horizontal_axis, vertical_axis = PLANE_AXES[axis]
    horizontal_index = AXIS_INDEX[horizontal_axis]
    vertical_index = AXIS_INDEX[vertical_axis]
    fixed_index = AXIS_INDEX[axis]
    width = 3.0
    inside = 0
    step = width / count
    for row in range(count):
        vertical_value = -0.5 + (row + 0.5) * step
        for column in range(count):
            horizontal_value = -0.5 + (column + 0.5) * step
            point = [Fraction(0), Fraction(0), Fraction(0)]
            point[fixed_index] = value
            point[horizontal_index] = Fraction(horizontal_value).limit_denominator(10**9)
            point[vertical_index] = Fraction(vertical_value).limit_denominator(10**9)
            if contains_by_limits(point):
                inside += 1
    return inside * step * step


def polynomial_antiderivative(polynomial: Polynomial) -> Polynomial:
    """Return the antiderivative whose constant term is zero."""
    result: Polynomial = [Fraction(0)]
    for degree, coefficient in enumerate(polynomial):
        result.append(coefficient / (degree + 1))
    return result


def polynomial_multiply(first: Polynomial, second: Polynomial) -> Polynomial:
    """Return the product of two polynomials."""
    product = [Fraction(0)] * (len(first) + len(second) - 1)
    for left_degree, left_coefficient in enumerate(first):
        for right_degree, right_coefficient in enumerate(second):
            product[left_degree + right_degree] += left_coefficient * right_coefficient
    return product


def polynomial_compose_linear(polynomial: Polynomial, slope: Fraction, intercept: Fraction) -> Polynomial:
    """Return the polynomial p(slope * t + intercept) as a polynomial in t."""
    result: Polynomial = [Fraction(0)]
    for coefficient in reversed(polynomial):
        result = polynomial_multiply(result, [intercept, slope])
        result[0] += coefficient
    return result


def polynomial_evaluate(polynomial: Polynomial, value: Fraction) -> Fraction:
    """Return the value of a polynomial at one point, by the Horner rule."""
    total = Fraction(0)
    for coefficient in reversed(polynomial):
        total = total * value + coefficient
    return total


def polynomial_integral(polynomial: Polynomial, lower: Fraction, upper: Fraction) -> Fraction:
    """Return the exact integral of a polynomial over an interval."""
    antiderivative = polynomial_antiderivative(polynomial)
    return polynomial_evaluate(antiderivative, upper) - polynomial_evaluate(antiderivative, lower)


def exact_volume() -> Fraction:
    """Return the volume of the solid by three nested exact integrations.

    The integrand is 1. The inner integral over y has the exact length
    2 - 2 z. The middle integral over z runs from 0 to 1 - x. The outer
    integral over x runs from 0 to 1. No value is written by hand.
    """
    inner_length = [Fraction(2), Fraction(-2)]
    middle_integrand = polynomial_antiderivative(inner_length)
    middle_value = polynomial_compose_linear(middle_integrand, Fraction(-1), Fraction(1))
    middle_value[0] -= polynomial_evaluate(middle_integrand, Fraction(0))
    return polynomial_integral(middle_value, Fraction(0), Fraction(1))


def volume_by_sections(axis: str) -> Fraction:
    """Return the volume as the exact integral of the closed-form section area."""
    if axis == "z":
        polynomial = polynomial_multiply([Fraction(1), Fraction(-1)], [Fraction(2), Fraction(-2)])
    elif axis == "x":
        polynomial = [Fraction(1), Fraction(0), Fraction(-1)]
    elif axis == "y":
        polynomial = [Fraction(1, 2), Fraction(0), Fraction(-1, 8)]
    else:
        raise ValueError(f"unknown axis {axis}")
    return polynomial_integral(polynomial, Fraction(0), Fraction(2) if axis == "y" else Fraction(1))


def determinant3(rows: Sequence[Sequence[Fraction]]) -> Fraction:
    """Return the determinant of a three by three matrix of fractions."""
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def solve_three_planes(first: HalfSpace, second: HalfSpace, third: HalfSpace) -> Point | None:
    """Return the common point of three plane boundaries, or None if they do not meet."""
    rows = [first[1], second[1], third[1]]
    bounds = [first[2], second[2], third[2]]
    determinant = determinant3(rows)
    if determinant == 0:
        return None
    solution: list[Fraction] = []
    for column in range(3):
        replaced = [list(row) for row in rows]
        for row_index in range(3):
            replaced[row_index][column] = bounds[row_index]
        solution.append(determinant3(replaced) / determinant)
    return (solution[0], solution[1], solution[2])


def enumerate_vertices() -> list[Point]:
    """Return every corner of the solid, found from the six half-spaces.

    A corner is the common point of three boundary planes that satisfies all
    six half-spaces. The function tries every triple, so the corner list comes
    from the inequalities and not from the drawing.
    """
    found: list[Point] = []
    count = len(SOLID_HALF_SPACES)
    for first in range(count):
        for second in range(first + 1, count):
            for third in range(second + 1, count):
                point = solve_three_planes(
                    SOLID_HALF_SPACES[first],
                    SOLID_HALF_SPACES[second],
                    SOLID_HALF_SPACES[third],
                )
                if point is None:
                    continue
                if not contains(point):
                    continue
                if point not in found:
                    found.append(point)
    return sorted(found)


def vertices_on_boundary(half_space: HalfSpace, vertices: Sequence[Point]) -> list[Point]:
    """Return the vertices of the solid that lie on the boundary of one half-space."""
    _, coefficients, bound = half_space
    return [point for point in vertices if dot(coefficients, point) == bound]


def triangle_area(first: Point, second: Point, third: Point) -> float:
    """Return the area of a triangle in space from a cross product."""
    first_edge = [second[index] - first[index] for index in range(3)]
    second_edge = [third[index] - first[index] for index in range(3)]
    cross = [
        float(first_edge[1] * second_edge[2] - first_edge[2] * second_edge[1]),
        float(first_edge[2] * second_edge[0] - first_edge[0] * second_edge[2]),
        float(first_edge[0] * second_edge[1] - first_edge[1] * second_edge[0]),
    ]
    return 0.5 * math.hypot(cross[0], cross[1], cross[2])


def convex_face_area(points: Sequence[Point]) -> float:
    """Return the area of a convex plane face by a fan of triangles."""
    if len(points) < 3:
        return 0.0
    total = 0.0
    for index in range(1, len(points) - 1):
        total += triangle_area(points[0], points[index], points[index + 1])
    return total


def order_face_points(points: Sequence[Point], half_space: HalfSpace) -> list[Point]:
    """Return the points of a plane face counter-clockwise around their centre."""
    normal = half_space[1]
    centre = [sum(point[index] for point in points) / len(points) for index in range(3)]
    helper = (Fraction(1), Fraction(0), Fraction(0))
    if normal[0] != 0:
        helper = (Fraction(0), Fraction(1), Fraction(0))
    first_axis = [
        normal[1] * helper[2] - normal[2] * helper[1],
        normal[2] * helper[0] - normal[0] * helper[2],
        normal[0] * helper[1] - normal[1] * helper[0],
    ]
    length = math.sqrt(sum(component * component for component in first_axis))
    first_axis = [component / length for component in first_axis]
    second_axis = [
        float(normal[1]) * first_axis[2] - float(normal[2]) * first_axis[1],
        float(normal[2]) * first_axis[0] - float(normal[0]) * first_axis[2],
        float(normal[0]) * first_axis[1] - float(normal[1]) * first_axis[0],
    ]

    def angle(point: Point) -> float:
        """Return the angle of a face point around the face centre."""
        offset = [float(point[index]) - centre[index] for index in range(3)]
        horizontal = sum(offset[index] * first_axis[index] for index in range(3))
        vertical = sum(offset[index] * second_axis[index] for index in range(3))
        return math.atan2(vertical, horizontal)

    return sorted(points, key=angle)


def bounding_box(points: Sequence[Point]) -> tuple[tuple[Fraction, Fraction], ...]:
    """Return the lowest and the highest value of each coordinate."""
    return tuple(
        (min(point[index] for point in points), max(point[index] for point in points)) for index in range(3)
    )


def face_report(vertices: Sequence[Point]) -> list[dict[str, object]]:
    """Return one record for each half-space: its name, its face points, and its area."""
    records: list[dict[str, object]] = []
    for half_space in SOLID_HALF_SPACES:
        points = vertices_on_boundary(half_space, vertices)
        records.append(
            {
                "name": half_space[0],
                "coefficients": half_space[1],
                "bound": half_space[2],
                "point_count": len(points),
                "points": points,
                "area": convex_face_area(order_face_points(points, half_space)) if len(points) >= 3 else 0.0,
            }
        )
    return records
