"""Model of the solid E of Exercise 40 in Section 15.7 of the textbook.

The statement gives four boundary surfaces and one constant density. This module turns that statement into
predicates, cross-section descriptions, and sampling helpers that every verification script shares.
Every constant of this module is a reading of the statement. A computed value of the tutorial stays in the
verification script that computes it.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence

import numpy as np

DENSITY: Fraction = Fraction(4)
"""The constant density rho of the solid, read from the phrase 'rho(x, y, z) = 4'."""

COORDINATE_Y_LOWEST: Fraction = Fraction(-1)
"""The smallest coordinate y of the solid, read from the condition 1 - y^2 >= 0."""

COORDINATE_Y_HIGHEST: Fraction = Fraction(1)
"""The largest coordinate y of the solid, read from the condition 1 - y^2 >= 0."""

SURFACE_STATEMENTS: tuple[str, ...] = (
    "the parabolic cylinder $z = 1 - y^{2}$",
    "the plane $x + z = 1$",
    "the plane $x = 0$",
    "the plane $z = 0$",
)
"""The four boundary surfaces of the solid, in the order of the statement."""


def point_in_solid_by_height(
    coordinate_x: float | np.ndarray,
    coordinate_y: float | np.ndarray,
    coordinate_z: float | np.ndarray,
) -> np.ndarray:
    """Return True for a point that the height form of the four inequalities keeps.

    The height form reads the cylinder as a ceiling: z <= 1 - y^2.

    Args:
        coordinate_x: The x coordinate of the point.
        coordinate_y: The y coordinate of the point.
        coordinate_z: The z coordinate of the point.

    Returns:
        A boolean array that marks the points of the closed solid E.
    """
    x = np.asarray(coordinate_x, dtype=float)
    y = np.asarray(coordinate_y, dtype=float)
    z = np.asarray(coordinate_z, dtype=float)
    return (z >= 0.0) & (z <= 1.0 - y**2) & (x >= 0.0) & (x <= 1.0 - z)


def point_in_solid_by_width(
    coordinate_x: float | np.ndarray,
    coordinate_y: float | np.ndarray,
    coordinate_z: float | np.ndarray,
) -> np.ndarray:
    """Return True for a point that the width form of the four inequalities keeps.

    The width form solves the cylinder for y: |y| <= sqrt(1 - z).

    Args:
        coordinate_x: The x coordinate of the point.
        coordinate_y: The y coordinate of the point.
        coordinate_z: The z coordinate of the point.

    Returns:
        A boolean array that marks the points of the closed solid E.
    """
    x = np.asarray(coordinate_x, dtype=float)
    y = np.asarray(coordinate_y, dtype=float)
    z = np.asarray(coordinate_z, dtype=float)
    half_width = np.sqrt(np.clip(1.0 - z, 0.0, None))
    return (z >= 0.0) & (z <= 1.0) & (np.abs(y) <= half_width) & (x >= 0.0) & (x <= 1.0 - z)


def half_width_at_height(coordinate_z: float | np.ndarray) -> np.ndarray:
    """Return the half width sqrt(1 - z) of the solid at the height z.

    Args:
        coordinate_z: The height z, with 0 <= z <= 1.

    Returns:
        The largest |y| that the solid allows at that height.
    """
    return np.sqrt(np.clip(1.0 - np.asarray(coordinate_z, dtype=float), 0.0, None))


def length_in_x_at_height(coordinate_z: float | np.ndarray) -> np.ndarray:
    """Return the length 1 - z of the x interval at the height z.

    Args:
        coordinate_z: The height z, with 0 <= z <= 1.

    Returns:
        The length of the x interval that the plane x + z = 1 allows.
    """
    return 1.0 - np.asarray(coordinate_z, dtype=float)


def cross_section_area_at_z(coordinate_z: float | np.ndarray) -> np.ndarray:
    """Return the area 2 (1 - z)^(3/2) of the horizontal section at the height z.

    The section is the rectangle [0, 1 - z] x [-sqrt(1 - z), sqrt(1 - z)].

    Args:
        coordinate_z: The height z, with 0 <= z <= 1.

    Returns:
        The area of the horizontal section.
    """
    z = np.asarray(coordinate_z, dtype=float)
    return 2.0 * np.clip(1.0 - z, 0.0, None) ** 1.5


def cross_section_area_at_x(coordinate_x: float | np.ndarray) -> np.ndarray:
    """Return the area (4/3) (1 - x^(3/2)) of the section at the coordinate x.

    Args:
        coordinate_x: The coordinate x, with 0 <= x <= 1.

    Returns:
        The area of the section in the plane of constant x.
    """
    x = np.asarray(coordinate_x, dtype=float)
    return (4.0 / 3.0) * (1.0 - np.clip(x, 0.0, None) ** 1.5)


def cross_section_area_at_y(coordinate_y: float | np.ndarray) -> np.ndarray:
    """Return the area u - u^2 / 2 of the section at the coordinate y, with u = 1 - y^2.

    The section is the right trapezoid 0 <= x <= 1 - z, 0 <= z <= u. Its parallel sides have the lengths 1 and
    1 - u, and its height is u.

    Args:
        coordinate_y: The coordinate y, with |y| <= 1.

    Returns:
        The area of the section in the plane of constant y.
    """
    y = np.asarray(coordinate_y, dtype=float)
    height = 1.0 - y**2
    return height - height**2 / 2.0


def corners_at_z(coordinate_z: float) -> np.ndarray:
    """Return the four corners of the horizontal section at the height z.

    Args:
        coordinate_z: The height z, with 0 <= z <= 1.

    Returns:
        An array of shape (4, 3) that holds the corners in cyclic order.
    """
    width = float(half_width_at_height(coordinate_z))
    length = float(length_in_x_at_height(coordinate_z))
    z = float(coordinate_z)
    return np.array(
        [
            [0.0, -width, z],
            [length, -width, z],
            [length, width, z],
            [0.0, width, z],
        ]
    )


def corners_at_y(coordinate_y: float) -> np.ndarray:
    """Return the four corners of the section at the coordinate y.

    Args:
        coordinate_y: The coordinate y, with |y| <= 1.

    Returns:
        An array of shape (4, 3) that holds the corners in cyclic order. The section is a right trapezoid.
    """
    y = float(coordinate_y)
    height = 1.0 - y**2
    return np.array(
        [
            [0.0, y, 0.0],
            [1.0, y, 0.0],
            [1.0 - height, y, height],
            [0.0, y, height],
        ]
    )


def corners_at_x(coordinate_x: float) -> np.ndarray:
    """Return the four corners of the section at the coordinate x.

    Args:
        coordinate_x: The coordinate x, with 0 <= x <= 1.

    Returns:
        An array of shape (4, 3) that holds the corners in cyclic order. At x = 1 the four corners meet at one
        point.
    """
    x = float(coordinate_x)
    top = 1.0 - x
    edge = float(np.sqrt(max(top, 0.0)))
    return np.array(
        [
            [x, -1.0, 0.0],
            [x, 1.0, 0.0],
            [x, edge, top],
            [x, -edge, top],
        ]
    )


def polygon_area(points: np.ndarray, first_axis: int, second_axis: int) -> float:
    """Return the area of a planar polygon with the shoelace formula.

    Args:
        points: The corners of the polygon in cyclic order.
        first_axis: The column index of the first coordinate of the plane.
        second_axis: The column index of the second coordinate of the plane.

    Returns:
        The area of the polygon.
    """
    first = points[:, first_axis]
    second = points[:, second_axis]
    shifted_first = np.roll(first, -1)
    shifted_second = np.roll(second, -1)
    return float(abs(np.dot(first, shifted_second) - np.dot(second, shifted_first)) / 2.0)


def sample_box(count: int, generator: np.random.Generator) -> np.ndarray:
    """Return uniformly random points of the box [0, 1] x [-1, 1] x [0, 1].

    Args:
        count: The number of points.
        generator: The random generator of the script.

    Returns:
        An array of shape (count, 3).
    """
    return np.column_stack(
        (
            generator.uniform(0.0, 1.0, count),
            generator.uniform(-1.0, 1.0, count),
            generator.uniform(0.0, 1.0, count),
        )
    )


def sample_solid(count: int, generator: np.random.Generator) -> np.ndarray:
    """Return uniformly random points of the solid E by rejection from the box.

    Args:
        count: The number of accepted points.
        generator: The random generator of the script.

    Returns:
        An array of shape (count, 3).
    """
    accepted: list[np.ndarray] = []
    held = 0
    while held < count:
        candidates = sample_box(4 * count, generator)
        keep = point_in_solid_by_width(candidates[:, 0], candidates[:, 1], candidates[:, 2])
        selected = candidates[keep]
        accepted.append(selected)
        held += selected.shape[0]
    return np.vstack(accepted)[:count]


def fraction_to_latex(value: Fraction) -> str:
    """Return the LaTeX source of an exact fraction.

    Args:
        value: The exact value.

    Returns:
        A string such as '\\frac{16}{5}' or '-\\frac{1}{2}' or '3'.
    """
    if value.denominator == 1:
        return str(value.numerator)
    sign = "-" if value < 0 else ""
    return f"{sign}\\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"


def format_decimal(value: float, digits: int = 6) -> str:
    """Return a decimal string with a fixed number of digits.

    Args:
        value: The value to print.
        digits: The number of digits after the decimal point.

    Returns:
        The decimal string.
    """
    return f"{value:.{digits}f}"


def describe_points(points: Sequence[Sequence[float]]) -> str:
    """Return one short text line for each point.

    Args:
        points: The points to describe.

    Returns:
        One line per point, in the form '(x, y, z)'.
    """
    return "; ".join(f"({point[0]:.3f}, {point[1]:.3f}, {point[2]:.3f})" for point in points)
