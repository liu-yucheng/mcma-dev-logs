"""Part 4: compute the same volume by a second order and by a grid rule.

The first instrument integrates y first.  At a fixed pair (x, z) the point is in the solid when
x^2 + z^2 <= 1, and then y runs from x to sqrt(1 - z^2).  The integral over the quarter disk in
the plane y = 0 is computed in polar coordinates, so it shares no limit with the order of Part 2.

The second instrument is a midpoint rule on a uniform grid of the unit cube.  It uses only the
two membership tests of Part 1 and no limit at all.
"""

from __future__ import annotations

import math

import numpy as np

import mcma_support as support

GRID = 240
"""Number of cells per axis of the midpoint rule."""

POLAR_NODES = 600
"""Number of nodes per axis of the polar quadrature."""


def inner_difference(height: float, x: float) -> float:
    """Return the length sqrt(1 - z^2) - x of the interval of y at a fixed (x, z)."""
    return height - x


def polar_volume() -> float:
    """Return the volume by a polar midpoint rule over the quarter disk of the plane y = 0.

    The point (x, z) is (r cos(t), r sin(t)).  The length of the interval of y is
    sqrt(1 - r^2 sin(t)^2) - r cos(t), and the area element is r dr dt.
    """
    radial = (np.arange(POLAR_NODES) + 0.5) / POLAR_NODES
    angular = (np.arange(POLAR_NODES) + 0.5) / POLAR_NODES * (math.pi / 2.0)
    radius, angle = np.meshgrid(radial, angular, indexing="ij")
    height = np.sqrt(np.maximum(0.0, 1.0 - (radius * np.sin(angle)) ** 2))
    length = np.maximum(0.0, height - radius * np.cos(angle))
    weight = radius * (1.0 / POLAR_NODES) * (math.pi / 2.0 / POLAR_NODES)
    return float(np.sum(length * weight))


def midpoint_volume() -> float:
    """Return the volume by a midpoint rule over the unit cube."""
    axis = (np.arange(GRID) + 0.5) / GRID
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    inside = (x <= y) & (x <= 1.0) & (y * y + z * z <= 1.0)
    return float(np.count_nonzero(inside)) / GRID ** 3


def main() -> None:
    """Run the checks of Part 4 and write its record."""
    recorder = support.Recorder(4)

    polar = polar_volume()
    midpoint = midpoint_volume()
    exact = 1.0 / 3.0
    recorder.record("polar quadrature of the projection against one third", polar, exact,
                    tolerance=1.0e-6)
    recorder.record("midpoint rule of the cube against one third", midpoint, exact,
                    tolerance=5.0e-3)
    recorder.record("midpoint rule against the polar quadrature", midpoint, polar,
                    tolerance=5.0e-3)

    disk_area = float(np.sum(((np.arange(POLAR_NODES) + 0.5) / POLAR_NODES)
                             * (1.0 / POLAR_NODES) * (math.pi / 2.0)))
    recorder.record("quarter disk area by the polar rule against pi / 4", disk_area,
                    math.pi / 4.0, tolerance=1.0e-6)
    recorder.record("inner length at the corner (0, 0) against one",
                    inner_difference(support.slice_length_at_height(0.0), 0.0), 1.0)
    recorder.record("inner length at the corner (1, 0) against zero",
                    inner_difference(support.slice_length_at_height(0.0), 1.0), 0.0)

    recorder.publish("p4_polar", f"{polar:.9f}")
    recorder.publish("p4_midpoint", f"{midpoint:.9f}")
    recorder.publish("p4_grid", str(GRID))
    recorder.publish("p4_polar_nodes", str(POLAR_NODES))
    recorder.publish("p4_disk_area", f"{disk_area:.9f}")
    recorder.publish("p4_exact", f"{exact:.9f}")
    recorder.write()


if __name__ == "__main__":
    main()
