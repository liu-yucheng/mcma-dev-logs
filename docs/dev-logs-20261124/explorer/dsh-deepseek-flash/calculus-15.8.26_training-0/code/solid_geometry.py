"""Geometry, volume formulas, and drawing helpers for problem 17.

The solid is the part of the ball of radius a that lies inside the cylinder
r = a cos(theta). This module holds the membership predicates, the closed form
of the volume, the quadrature methods that check the closed form, and the
drawing helpers that the figure scripts share.

Every check helper compares a value that one method computes with a value that
a different method computes. A check that compares a value with itself is a
fault, and no function of this module does that.
"""

from __future__ import annotations

import math
from typing import Callable, Iterable, Sequence

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Text
from scipy import integrate

REFERENCE_RADIUS = 1.0
"""Radius used by each numeric example. The symbol a stays symbolic in the text."""

MONTE_CARLO_SEED = 20261123
"""Seed of the Monte Carlo check, so that the printed estimate is reproducible."""

MONTE_CARLO_SAMPLES = 4_000_000
"""Number of samples of the Monte Carlo check."""

CHECKS: list[dict[str, object]] = []
"""Records of the checks that ran in this process."""


def report_check(
    name: str,
    computed: float,
    expected: float,
    tolerance: float,
    method: str,
) -> float:
    """Print one comparison of two independent values and assert its tolerance.

    Args:
        name: Identifier of the check. The step files cite this name.
        computed: Value that the first method computes.
        expected: Value that the second method computes.
        tolerance: Largest accepted absolute difference. Must be positive.
        method: Short text that names both methods.

    Returns:
        The signed difference computed minus expected.

    Raises:
        AssertionError: The difference is larger than the tolerance, or one
            value is not finite, or the tolerance is not positive.
    """
    computed_value = float(computed)
    expected_value = float(expected)
    assert math.isfinite(computed_value), f"{name}: computed value is not finite"
    assert math.isfinite(expected_value), f"{name}: expected value is not finite"
    assert tolerance > 0.0, f"{name}: the tolerance must be a positive number"
    difference = computed_value - expected_value
    passed = abs(difference) <= tolerance
    CHECKS.append(
        {
            "name": name,
            "computed": computed_value,
            "expected": expected_value,
            "difference": difference,
            "tolerance": tolerance,
            "method": method,
        }
    )
    print(
        f"CHECK {name}: computed={computed_value!r} expected={expected_value!r} "
        f"difference={difference:.6e} tolerance={tolerance:.3e} PASS={passed}"
    )
    print(f"  method: {method}")
    assert passed, (
        f"{name}: computed {computed_value!r} differs from expected {expected_value!r} "
        f"by {difference:.6e}, above the tolerance {tolerance:.3e}"
    )
    return difference


def report_falsification(
    name: str,
    wrong_value: float,
    reference_value: float,
    minimum_gap: float,
    method: str,
) -> float:
    """Show that a wrong model is measurably outside the accepted value.

    Args:
        name: Identifier of the falsification control.
        wrong_value: Value that the wrong model computes.
        reference_value: Accepted value of the same quantity.
        minimum_gap: Smallest accepted separation of the two values.
        method: Short text that names the wrong model and the accepted value.

    Returns:
        The absolute gap between the wrong value and the reference value.

    Raises:
        AssertionError: The gap is not larger than the minimum gap, which means
            that the check cannot discriminate the wrong model.
    """
    gap = abs(float(wrong_value) - float(reference_value))
    assert minimum_gap > 0.0, f"{name}: the minimum gap must be a positive number"
    print(
        f"CONTROL {name}: wrong model={float(wrong_value)!r} accepted={float(reference_value)!r} "
        f"gap={gap:.6e} minimum_gap={minimum_gap:.3e} DISCRIMINATES={gap > minimum_gap}"
    )
    print(f"  method: {method}")
    assert gap > minimum_gap, (
        f"{name}: the wrong model is only {gap:.6e} away from the accepted value, "
        f"so the check cannot discriminate it"
    )
    return gap


def summarize(part_name: str) -> None:
    """Print the count of the checks of one part and fail when the list is empty.

    Args:
        part_name: Name of the part, for example ``part1``.

    Raises:
        AssertionError: No check ran, which would leave the part unchecked.
    """
    assert CHECKS, f"{part_name}: no check ran"
    print(f"SUMMARY {part_name}: {len(CHECKS)} checks passed")
    for record in CHECKS:
        print(
            f"  {record['name']}: computed={record['computed']!r} "
            f"expected={record['expected']!r} tolerance={record['tolerance']:.3e}"
        )


def cylinder_membership_cartesian(x: np.ndarray, y: np.ndarray, radius: float) -> np.ndarray:
    """Return the mask of the points inside the solid cylinder, in Cartesian form.

    Args:
        x: x coordinates of the points.
        y: y coordinates of the points.
        radius: Radius a of the sphere, which is also the diameter of the cylinder.

    Returns:
        Boolean mask of the points that satisfy (x - a/2)^2 + y^2 <= (a/2)^2.
    """
    half = radius / 2.0
    return (x - half) ** 2 + y**2 <= half**2 + 1.0e-15


def cylinder_membership_polar(
    radial_distance: np.ndarray,
    angle: np.ndarray,
    radius: float,
) -> np.ndarray:
    """Return the mask of the points inside the solid cylinder, in polar form.

    Args:
        radial_distance: Distance r from the z axis. Must not be negative.
        angle: Angle theta measured from the positive x axis.
        radius: Radius a of the sphere.

    Returns:
        Boolean mask of the points that satisfy 0 <= r <= a cos(theta).
    """
    return (radial_distance >= 0.0) & (radial_distance <= radius * np.cos(angle) + 1.0e-15)


def sphere_membership(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    radius: float,
) -> np.ndarray:
    """Return the mask of the points inside the closed ball of the given radius.

    Args:
        x: x coordinates of the points.
        y: y coordinates of the points.
        z: z coordinates of the points.
        radius: Radius a of the ball.

    Returns:
        Boolean mask of the points that satisfy x^2 + y^2 + z^2 <= a^2.
    """
    return x**2 + y**2 + z**2 <= radius**2 + 1.0e-15


def region_membership(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    radius: float,
) -> np.ndarray:
    """Return the mask of the points of the solid of part (a).

    Args:
        x: x coordinates of the points.
        y: y coordinates of the points.
        z: z coordinates of the points.
        radius: Radius a of the sphere.

    Returns:
        Boolean mask of the points inside the ball and inside the cylinder.
    """
    return sphere_membership(x, y, z, radius) & cylinder_membership_cartesian(x, y, radius)


def upper_height(radial_distance: float, radius: float) -> float:
    """Return the height of the upper half of the sphere at a distance r.

    Args:
        radial_distance: Distance r from the z axis. Must satisfy 0 <= r <= a.
        radius: Radius a of the sphere.

    Returns:
        The value sqrt(a^2 - r^2).
    """
    return math.sqrt(max(radius**2 - radial_distance**2, 0.0))


def exact_volume(radius: float) -> float:
    """Return the closed form (2/3) pi a^3 - (8/9) a^3 of the volume.

    Args:
        radius: Radius a of the sphere.

    Returns:
        The volume of the solid of part (a).
    """
    return (2.0 / 3.0) * math.pi * radius**3 - (8.0 / 9.0) * radius**3


def exact_volume_factored(radius: float) -> float:
    """Return the closed form a^3 (6 pi - 8) / 9, factored in a different way.

    Args:
        radius: Radius a of the sphere.

    Returns:
        The same volume as :func:`exact_volume`, from another algebraic form.
    """
    return radius**3 * (6.0 * math.pi - 8.0) / 9.0


def theta_integral_closed_form() -> float:
    """Return the exact value pi - 4/3 of the integral of 1 - |sin(theta)|^3.

    Returns:
        The value of the integral over the interval from -pi/2 to pi/2.
    """
    return math.pi - 4.0 / 3.0


def volume_by_triple_quadrature(radius: float) -> float:
    """Return the volume from a full triple integral in the order dz dr dtheta.

    The integrand is r, and the bounds are the bounds of the solid. The call
    never uses an antiderivative, so it is independent of the closed form.

    Args:
        radius: Radius a of the sphere.

    Returns:
        The numeric value of the triple integral.
    """
    value, _ = integrate.tplquad(
        lambda z, r, theta: r,
        -math.pi / 2.0,
        math.pi / 2.0,
        0.0,
        lambda theta: radius * math.cos(theta),
        lambda theta, r: -upper_height(r, radius),
        lambda theta, r: upper_height(r, radius),
        epsabs=1.0e-10,
        epsrel=1.0e-10,
    )
    return value


def volume_by_cylinder_axis_polar(radius: float) -> float:
    """Return the volume from polar coordinates about the axis of the cylinder.

    The substitution is x = a/2 + rho cos(phi), y = rho sin(phi). The integrand
    is 2 sqrt(a^2 - x^2 - y^2) rho over the disk of radius a/2.

    Args:
        radius: Radius a of the sphere.

    Returns:
        The numeric value of the double integral.
    """

    def height(x_value: float, y_value: float) -> float:
        """Return the full vertical length of the ball above one base point."""
        square = radius**2 - x_value**2 - y_value**2
        return 2.0 * math.sqrt(max(square, 0.0))

    def integrand(rho: float, phi: float) -> float:
        """Return the vertical length times the Jacobian rho at one base point."""
        x_value = radius / 2.0 + rho * math.cos(phi)
        y_value = rho * math.sin(phi)
        return height(x_value, y_value) * rho

    value, _ = integrate.dblquad(
        integrand,
        0.0,
        2.0 * math.pi,
        0.0,
        radius / 2.0,
        epsabs=1.0e-11,
        epsrel=1.0e-11,
    )
    return value


def lens_area(radius_large: float, radius_small: float, distance: float) -> float:
    """Return the area of the intersection of two disks from the lens formula.

    Args:
        radius_large: Radius R of the disk that is centered at the origin.
        radius_small: Radius r of the disk whose center is on the x axis.
        distance: Distance d between the two centers.

    Returns:
        The area of the intersection of the two closed disks. The value is zero
        when the disks do not meet.
    """
    if radius_large <= 0.0 or radius_small <= 0.0:
        return 0.0
    if distance >= radius_large + radius_small:
        return 0.0
    if distance <= abs(radius_large - radius_small):
        return math.pi * min(radius_large, radius_small) ** 2
    cos_large = (distance**2 + radius_large**2 - radius_small**2) / (2.0 * distance * radius_large)
    cos_small = (distance**2 + radius_small**2 - radius_large**2) / (2.0 * distance * radius_small)
    cos_large = min(max(cos_large, -1.0), 1.0)
    cos_small = min(max(cos_small, -1.0), 1.0)
    product = (
        (-distance + radius_large + radius_small)
        * (distance + radius_large - radius_small)
        * (distance - radius_large + radius_small)
        * (distance + radius_large + radius_small)
    )
    triangle_term = 0.5 * math.sqrt(max(product, 0.0))
    return (
        radius_large**2 * math.acos(cos_large)
        + radius_small**2 * math.acos(cos_small)
        - triangle_term
    )


def volume_by_horizontal_slices(radius: float) -> float:
    """Return the volume from horizontal slices with the lens area formula.

    At height z the slice is the intersection of the disk of radius
    sqrt(a^2 - z^2) with the footprint disk of radius a/2 at distance a/2.

    Args:
        radius: Radius a of the sphere.

    Returns:
        The numeric value of the integral of the slice area over z.
    """

    def slice_area(height_value: float) -> float:
        """Return the area of the horizontal slice at one height."""
        large = math.sqrt(max(radius**2 - height_value**2, 0.0))
        return lens_area(large, radius / 2.0, radius / 2.0)

    value, _ = integrate.quad(
        slice_area,
        -radius,
        radius,
        epsabs=1.0e-12,
        epsrel=1.0e-12,
        limit=400,
    )
    return value


def volume_by_monte_carlo(radius: float) -> tuple[float, float]:
    """Return the Monte Carlo volume estimate and its standard error.

    Args:
        radius: Radius a of the sphere.

    Returns:
        A pair of the estimate and one standard error of the estimate.
    """
    generator = np.random.default_rng(MONTE_CARLO_SEED)
    half = radius / 2.0
    count = MONTE_CARLO_SAMPLES
    x_values = generator.uniform(0.0, radius, count)
    y_values = generator.uniform(-half, half, count)
    z_values = generator.uniform(-radius, radius, count)
    inside = region_membership(x_values, y_values, z_values, radius)
    box_volume = radius * (2.0 * half) * (2.0 * radius)
    fraction = float(np.count_nonzero(inside)) / count
    estimate = fraction * box_volume
    standard_error = box_volume * math.sqrt(fraction * (1.0 - fraction) / count)
    return estimate, standard_error


def radial_integral_closed_form(angle: float, radius: float) -> float:
    """Return the exact inner integral (2/3) a^3 (1 - |sin theta|^3).

    Args:
        angle: Angle theta in radians.
        radius: Radius a of the sphere.

    Returns:
        The value of the integral of 2 r sqrt(a^2 - r^2) from r = 0 to a cos(theta).
    """
    return (2.0 / 3.0) * radius**3 * (1.0 - abs(math.sin(angle)) ** 3)


def radial_integral_numeric(angle: float, radius: float) -> float:
    """Return the inner integral from adaptive quadrature, with no antiderivative.

    Args:
        angle: Angle theta in radians.
        radius: Radius a of the sphere.

    Returns:
        The numeric value of the integral of 2 r sqrt(a^2 - r^2).
    """
    upper = max(radius * math.cos(angle), 0.0)
    value, _ = integrate.quad(
        lambda r: 2.0 * r * math.sqrt(max(radius**2 - r**2, 0.0)),
        0.0,
        upper,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
    )
    return value


def polar_cell_area(
    inner_radius: float,
    outer_radius: float,
    start_angle: float,
    end_angle: float,
) -> float:
    """Return the exact area of one annular sector in polar coordinates.

    Args:
        inner_radius: Inner radius of the sector.
        outer_radius: Outer radius of the sector.
        start_angle: First angle of the sector in radians.
        end_angle: Last angle of the sector in radians.

    Returns:
        The area (outer^2 - inner^2) / 2 times the angle width.
    """
    return 0.5 * (outer_radius**2 - inner_radius**2) * (end_angle - start_angle)


def polygon_area(x_values: Sequence[float], y_values: Sequence[float]) -> float:
    """Return the area of a closed polygon from the shoelace formula.

    Args:
        x_values: x coordinates of the vertices in order.
        y_values: y coordinates of the vertices in order.

    Returns:
        The absolute area of the polygon.
    """
    x_array = np.asarray(x_values, dtype=float)
    y_array = np.asarray(y_values, dtype=float)
    return 0.5 * abs(
        float(np.dot(x_array, np.roll(y_array, -1)) - np.dot(y_array, np.roll(x_array, -1)))
    )


def draw_arrowed_axis(
    axes: Axes,
    start: Sequence[float],
    end: Sequence[float],
    color: str = "#35424d",
    line_width: float = 1.1,
) -> None:
    """Draw one coordinate axis as an arrow, with no text of its own.

    Args:
        axes: Three dimensional axes of the figure.
        start: Coordinates of the tail of the arrow.
        end: Coordinates of the tip of the arrow.
        color: Stroke color.
        line_width: Stroke width in points.
    """
    axes.quiver(
        start[0],
        start[1],
        start[2],
        end[0] - start[0],
        end[1] - start[1],
        end[2] - start[2],
        color=color,
        linewidth=line_width,
        arrow_length_ratio=0.07,
        normalize=False,
    )


def place_axis_letter(
    axes: Axes,
    letter: str,
    position: Sequence[float],
    font_size: float = 13.0,
) -> Text:
    """Place the one letter of one axis at the tip of its arrow.

    Args:
        axes: Three dimensional axes of the figure.
        letter: Letter of the axis, for example ``$x$``.
        position: Coordinates of the letter.
        font_size: Font size in points.

    Returns:
        The text object, so that a later check can measure its box.
    """
    return axes.text(
        position[0],
        position[1],
        position[2],
        letter,
        fontsize=font_size,
        color="#35424d",
        ha="center",
        va="center",
        zorder=30,
    )


def draw_numeric_tick(
    axes: Axes,
    position: Sequence[float],
    offset: Sequence[float],
    label: str,
    font_size: float = 8.5,
) -> Text:
    """Draw one tick mark of one axis and its numeric label.

    Args:
        axes: Three dimensional axes of the figure.
        position: Coordinates of the tick on the axis.
        offset: Short vector from the axis to the outer end of the tick.
        label: Numeric label of the tick.
        font_size: Font size in points.

    Returns:
        The text object of the numeric label.
    """
    axes.plot(
        [position[0], position[0] + offset[0]],
        [position[1], position[1] + offset[1]],
        [position[2], position[2] + offset[2]],
        color="#5b6a76",
        linewidth=0.8,
    )
    return axes.text(
        position[0] + 1.9 * offset[0],
        position[1] + 1.9 * offset[1],
        position[2] + 1.9 * offset[2],
        label,
        fontsize=font_size,
        color="#5b6a76",
        ha="center",
        va="center",
        zorder=29,
    )


def assert_texts_inside_axes(
    figure: Figure,
    axes: Axes,
    texts: Iterable[Text],
    margin_pixels: float = 2.0,
) -> list[float]:
    """Assert that each text lies inside the axes box and return the margins.

    Args:
        figure: Figure that holds the axes.
        axes: Axes that must contain the texts.
        texts: Text objects to measure.
        margin_pixels: Smallest accepted distance from the axes edge.

    Returns:
        The margin in pixels of each text, in the order of the input.

    Raises:
        AssertionError: A text crosses the axes edge.
    """
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    axes_box = axes.get_window_extent(renderer)
    margins: list[float] = []
    for text in texts:
        box = text.get_window_extent(renderer)
        margin = min(
            box.x0 - axes_box.x0,
            axes_box.x1 - box.x1,
            box.y0 - axes_box.y0,
            axes_box.y1 - box.y1,
        )
        print(
            f"  label {text.get_text()!r}: margin={margin:.2f}px "
            f"box=({box.x0:.1f},{box.y0:.1f})-({box.x1:.1f},{box.y1:.1f}) "
            f"axes=({axes_box.x0:.1f},{axes_box.y0:.1f})-({axes_box.x1:.1f},{axes_box.y1:.1f})"
        )
        assert margin >= margin_pixels, (
            f"the label {text.get_text()!r} crosses the axes edge by "
            f"{margin_pixels - margin:.2f} pixels"
        )
        margins.append(margin)
    return margins


def assert_texts_disjoint(figure: Figure, texts: Sequence[Text], gap_pixels: float = 1.0) -> None:
    """Assert that no two texts of one panel overlap.

    Args:
        figure: Figure that holds the texts.
        texts: Text objects to measure.
        gap_pixels: Smallest accepted gap between two boxes.

    Raises:
        AssertionError: Two texts overlap or touch.
    """
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    boxes = [text.get_window_extent(renderer) for text in texts]
    for first_index in range(len(boxes)):
        for second_index in range(first_index + 1, len(boxes)):
            first = boxes[first_index]
            second = boxes[second_index]
            overlap_x = min(first.x1, second.x1) - max(first.x0, second.x0)
            overlap_y = min(first.y1, second.y1) - max(first.y0, second.y0)
            if overlap_x > -gap_pixels and overlap_y > -gap_pixels:
                raise AssertionError(
                    f"the labels {texts[first_index].get_text()!r} and "
                    f"{texts[second_index].get_text()!r} overlap"
                )
    print(f"  label pairs checked for overlap: {len(boxes) * (len(boxes) - 1) // 2}, none overlap")
