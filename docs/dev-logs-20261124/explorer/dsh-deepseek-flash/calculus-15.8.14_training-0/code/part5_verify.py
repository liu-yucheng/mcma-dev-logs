"""Verify that the labels of the drawing sit on their surfaces and that the summary numbers agree.

Part 5 closes the tutorial.  It checks two things.  First, each label of the
drawing is attached to a point that the equation of its own surface satisfies.
Second, each number that the summary states is recomputed by a method that the
earlier parts did not use, so that the summary cannot drift away from the work.
"""

from __future__ import annotations

from fractions import Fraction
import math

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

from solid_geometry import RIM_SQUARED_RADIUS, build_label_anchors

TOLERANCE = 1.0e-9


def check_label_anchors_on_surfaces() -> None:
    """Check that each label anchor satisfies the equation of the surface that it names.

    The anchor of the lower surface must satisfy z = x^2 + y^2, the anchor of the
    upper surface must satisfy z = 5 - x^2 - y^2, and the anchor of the circle
    must satisfy both equations at the same time.
    """
    # BEGIN CHECK label_anchors_on_surfaces
    checked_count = 0
    for anchor in build_label_anchors():
        key = str(anchor["key"])
        anchor_x = float(anchor["x"])
        anchor_y = float(anchor["y"])
        anchor_z = float(anchor["z"])
        squared_radius = anchor_x**2 + anchor_y**2
        lower_gap = abs(anchor_z - squared_radius)
        upper_gap = abs(anchor_z - (5.0 - squared_radius))
        print(f"anchor {key}: squared radius {squared_radius:.9f}, height {anchor_z:.9f}")
        print(f"anchor {key}: gap to the lower surface {lower_gap:.3e}, gap to the upper surface {upper_gap:.3e}")
        if str(anchor["surface"]) == "lower":
            assert lower_gap < TOLERANCE, f"the lower anchor {key} leaves the lower surface"
        elif str(anchor["surface"]) == "upper":
            assert upper_gap < TOLERANCE, f"the upper anchor {key} leaves the upper surface"
        else:
            assert lower_gap < TOLERANCE and upper_gap < TOLERANCE, f"the circle anchor {key} is off the circle"
            assert abs(squared_radius - RIM_SQUARED_RADIUS) < TOLERANCE, f"the circle anchor {key} is off the rim"
        checked_count += 1
    print(f"label anchors checked against their equations: {checked_count}")
    assert checked_count == 3, "the drawing must carry one anchor for each of the three labels"
    # END CHECK label_anchors_on_surfaces


def check_summary_numbers_agree() -> None:
    """Recompute every number of the summary by a method that the earlier parts did not use.

    The squared radius of the rim comes from a root search, the area of the widest
    section comes from a cell count on a fine grid, and the volume comes from a
    one dimensional quadrature of the shell area.  Each value is compared with the
    closed form that the summary states.
    """
    # BEGIN CHECK summary_numbers_agree
    solved_radius = brentq(lambda radius: 5.0 - 2.0 * radius**2, 0.0, 3.0, xtol=1.0e-14)
    solved_squared_radius = solved_radius**2
    exact_squared_radius = float(Fraction(5, 2))
    print(f"squared radius from the root search: {solved_squared_radius:.9f}")
    print(f"squared radius of the closed form: {exact_squared_radius:.9f}")
    assert abs(solved_squared_radius - exact_squared_radius) < 1.0e-12, "the root search misses 5/2"

    cell_count = 1200
    coordinates = (np.arange(cell_count) + 0.5) / cell_count * 2.0 * solved_radius - solved_radius
    grid_x, grid_y = np.meshgrid(coordinates, coordinates)
    cell_area = (2.0 * solved_radius / cell_count) ** 2
    counted_area = float(np.count_nonzero(grid_x**2 + grid_y**2 <= solved_squared_radius)) * cell_area
    closed_form_area = math.pi * solved_squared_radius
    print(f"area of the widest section by the cell count: {counted_area:.9f}")
    print(f"area of the widest section by the closed form: {closed_form_area:.9f}")
    print(f"relative gap of the area: {abs(counted_area - closed_form_area) / closed_form_area:.3e}")
    assert abs(counted_area - closed_form_area) / closed_form_area < 2.0e-3, "the cell count misses the area"

    shell_integral, _ = quad(lambda radius: 2.0 * math.pi * radius * (5.0 - 2.0 * radius**2), 0.0, solved_radius)
    exact_volume = float(Fraction(25, 4)) * math.pi
    print(f"volume from the shell integral: {shell_integral:.9f}")
    print(f"volume from the closed form: {exact_volume:.9f}")
    print(f"relative gap of the volume: {abs(shell_integral - exact_volume) / exact_volume:.3e}")
    assert abs(shell_integral - exact_volume) / exact_volume < 1.0e-10, "the shell integral misses 25 pi / 4"

    print(f"height of the rim stated by the summary: {solved_squared_radius:.9f}")
    assert abs(solved_squared_radius - 2.5) < 1.0e-12, "the rim does not sit at the height 5/2"
    # END CHECK summary_numbers_agree


def main() -> None:
    """Run every check of Part 5."""
    check_label_anchors_on_surfaces()
    check_summary_numbers_agree()
    print("part5_verify.py: every check passed")


if __name__ == "__main__":
    main()
