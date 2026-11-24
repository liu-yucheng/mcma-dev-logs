"""Geometric predicates and heights of the solid of Problem 9.

The solid E is bounded by the elliptic paraboloid y = 4 - x**2 - 4*z**2 and by the
plane y = 0. This module holds one function for each object that the tutorial names.
Every function is a definition, not a quadrature rule: the verification scripts compare
these definitions with a second, independent computation.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

# Coefficient of z**2 in the upper surface. The source image gives 4, not 1.
Z_SQUARED_COEFFICIENT = 4.0

# Height of the apex of the paraboloid on the axis x = 0, z = 0.
APEX_HEIGHT = 4.0

# Semi-axis of the base ellipse along the axis x, in the plane y = 0.
BASE_SEMI_AXIS_X = 2.0

# Semi-axis of the base ellipse along the axis z, in the plane y = 0.
BASE_SEMI_AXIS_Z = 1.0


def upper_height(x: ArrayLike, z: ArrayLike) -> NDArray[np.float64]:
    """Return the height y of the upper surface at the coordinates x and z.

    Args:
        x: Coordinate along the axis x.
        z: Coordinate along the axis z.

    Returns:
        The value 4 - x**2 - 4*z**2, element by element.
    """
    x_array = np.asarray(x, dtype=float)
    z_array = np.asarray(z, dtype=float)
    return APEX_HEIGHT - x_array**2 - Z_SQUARED_COEFFICIENT * z_array**2


def inside_solid(x: ArrayLike, y: ArrayLike, z: ArrayLike) -> NDArray[np.bool_]:
    """Return True where the point (x, y, z) lies in the closed solid E.

    The predicate uses the two given surfaces only: a point is in E when it lies above
    the plane y = 0 and below the paraboloid.

    Args:
        x: Coordinate along the axis x.
        y: Coordinate along the axis y.
        z: Coordinate along the axis z.

    Returns:
        A Boolean array with the membership of each point.
    """
    x_array, y_array, z_array = np.broadcast_arrays(
        np.asarray(x, dtype=float), np.asarray(y, dtype=float), np.asarray(z, dtype=float)
    )
    above_base = y_array >= 0.0
    below_roof = y_array <= upper_height(x_array, z_array)
    return np.asarray(above_base & below_roof)


def inside_projection(x: ArrayLike, z: ArrayLike) -> NDArray[np.bool_]:
    """Return True where the point (x, z) lies in the projection of E on the plane y = 0.

    Args:
        x: Coordinate along the axis x.
        z: Coordinate along the axis z.

    Returns:
        A Boolean array with the membership of each point of the plane y = 0.
    """
    x_array = np.asarray(x, dtype=float)
    z_array = np.asarray(z, dtype=float)
    return np.asarray(x_array**2 + Z_SQUARED_COEFFICIENT * z_array**2 <= 4.0)


def scaled_radius(x: ArrayLike, z: ArrayLike) -> NDArray[np.float64]:
    """Return the radius r of the unit disk after the substitution x = 2*r*cos(t), z = r*sin(t).

    Args:
        x: Coordinate along the axis x.
        z: Coordinate along the axis z.

    Returns:
        The value sqrt((x/2)**2 + z**2), element by element.
    """
    x_array = np.asarray(x, dtype=float)
    z_array = np.asarray(z, dtype=float)
    return np.sqrt((x_array / BASE_SEMI_AXIS_X) ** 2 + z_array**2)


def inside_solid_by_substitution(x: ArrayLike, y: ArrayLike, z: ArrayLike) -> NDArray[np.bool_]:
    """Return True where the substitution image of the solid holds the point.

    The substitution x = 2*r*cos(t), z = r*sin(t), with 0 <= r <= 1 and 0 <= y <= 4*(1 - r**2),
    is a second encoding of the same solid. It shares no expression with inside_solid.

    Args:
        x: Coordinate along the axis x.
        y: Coordinate along the axis y.
        z: Coordinate along the axis z.

    Returns:
        A Boolean array with the membership of each point.
    """
    x_array, y_array, z_array = np.broadcast_arrays(
        np.asarray(x, dtype=float), np.asarray(y, dtype=float), np.asarray(z, dtype=float)
    )
    radius = scaled_radius(x_array, z_array)
    inside_disk = radius <= 1.0
    below_roof = y_array <= APEX_HEIGHT * (1.0 - radius**2)
    return np.asarray(inside_disk & (y_array >= 0.0) & below_roof)


def section_half_width_x(z: ArrayLike, y: ArrayLike = 0.0) -> NDArray[np.float64]:
    """Return the half width in x of the section of E at fixed z and fixed y.

    The section of E at fixed values of y and z is the set of x with
    x**2 <= 4 - 4*z**2 - y. Its half width is sqrt(4 - 4*z**2 - y).

    Args:
        z: Coordinate along the axis z.
        y: Height of the section. The default value 0 gives the widest section.

    Returns:
        The half width, with a not-a-number value where the radicand is negative.
    """
    z_array = np.asarray(z, dtype=float)
    y_array = np.asarray(y, dtype=float)
    radicand = 4.0 - Z_SQUARED_COEFFICIENT * z_array**2 - y_array
    return np.sqrt(np.where(radicand >= 0.0, radicand, np.nan))


def section_half_width_z(x: ArrayLike, y: ArrayLike = 0.0) -> NDArray[np.float64]:
    """Return the half width in z of the section of E at fixed x and fixed y.

    The section of E at fixed values of x and y is the set of z with
    4*z**2 <= 4 - x**2 - y. Its half width is sqrt(4 - x**2 - y) / 2.

    Args:
        x: Coordinate along the axis x.
        y: Height of the section. The default value 0 gives the widest section.

    Returns:
        The half width, with a not-a-number value where the radicand is negative.
    """
    x_array = np.asarray(x, dtype=float)
    y_array = np.asarray(y, dtype=float)
    radicand = 4.0 - x_array**2 - y_array
    return np.sqrt(np.where(radicand >= 0.0, radicand, np.nan)) / 2.0
