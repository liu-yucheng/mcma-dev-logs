"""Surface grids that the figures draw and that the check layer verifies.

A figure script and a verification script import the same arrays, so the drawn mesh and the
checked mesh are one object.
"""

import math

import numpy as np

from silo_geometry import (
    CAP_RADIUS,
    CYLINDER_HEIGHT,
    CYLINDER_RADIUS,
    body_holds,
)

AZIMUTH_COUNT = 73
"""Number of samples around the axis of the body."""

HEIGHT_COUNT = 25
"""Number of samples along a height or an inclination."""


def cylinder_grid() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the mesh of the lateral face of the cylinder."""
    azimuths = np.linspace(0.0, 2.0 * math.pi, AZIMUTH_COUNT)
    heights = np.linspace(0.0, CYLINDER_HEIGHT, HEIGHT_COUNT)
    azimuth_mesh, height_mesh = np.meshgrid(azimuths, heights)
    x_values = CYLINDER_RADIUS * np.cos(azimuth_mesh)
    y_values = CYLINDER_RADIUS * np.sin(azimuth_mesh)
    return x_values, y_values, height_mesh


def cap_grid() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the mesh of the hemispherical cap, without its flat face."""
    azimuths = np.linspace(0.0, 2.0 * math.pi, AZIMUTH_COUNT)
    inclinations = np.linspace(0.0, 0.5 * math.pi, HEIGHT_COUNT)
    azimuth_mesh, inclination_mesh = np.meshgrid(azimuths, inclinations)
    x_values = CAP_RADIUS * np.sin(inclination_mesh) * np.cos(azimuth_mesh)
    y_values = CAP_RADIUS * np.sin(inclination_mesh) * np.sin(azimuth_mesh)
    z_values = CYLINDER_HEIGHT + CAP_RADIUS * np.cos(inclination_mesh)
    return x_values, y_values, z_values


def disk_grid(height: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the mesh of a flat circular face of the body at the given height."""
    azimuths = np.linspace(0.0, 2.0 * math.pi, AZIMUTH_COUNT)
    radii = np.linspace(0.0, CYLINDER_RADIUS, HEIGHT_COUNT)
    azimuth_mesh, radius_mesh = np.meshgrid(azimuths, radii)
    x_values = radius_mesh * np.cos(azimuth_mesh)
    y_values = radius_mesh * np.sin(azimuth_mesh)
    z_values = np.full_like(x_values, height)
    return x_values, y_values, z_values


def meridian_region(x_values: np.ndarray, z_values: np.ndarray) -> np.ndarray:
    """Return the indicator of the section of the body on the plane y = 0.

    The panel keeps the coordinates x and z, and it drops the coordinate y.  A point of the
    section therefore lies on the plane y = 0.
    """
    inside = np.zeros_like(x_values, dtype=bool)
    for index in np.ndindex(x_values.shape):
        inside[index] = body_holds(float(x_values[index]), 0.0, float(z_values[index]))
    return inside


def meridian_outline_half_width(height: float) -> float:
    """Return the half width of the section on the plane y = 0 at the given height."""
    if height < 0.0 or height > CYLINDER_HEIGHT + CAP_RADIUS:
        return 0.0
    if height <= CYLINDER_HEIGHT:
        return CYLINDER_RADIUS
    return math.sqrt(max(0.0, CAP_RADIUS**2 - (height - CYLINDER_HEIGHT) ** 2))
