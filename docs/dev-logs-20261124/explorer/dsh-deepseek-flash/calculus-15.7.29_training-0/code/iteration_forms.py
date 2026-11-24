"""The six iterated integrals over the solid of Problem 9, one function for each order.

The solid E is the set of points with 0 <= y <= 4 - x**2 - 4*z**2, so its projection on the
plane y = 0 is the ellipse x**2 + 4*z**2 <= 4. Each function of this module evaluates one
order with adaptive quadrature and states its limits in the docstring. Each function named
limits_* tests the same limits as inequalities, so a sampling check can compare the limits
with the defining inequalities of the solid.
"""

from __future__ import annotations

import math
from typing import Callable

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.integrate import tplquad

# Absolute tolerance asked of the adaptive quadrature.
QUADRATURE_ABSOLUTE_TOLERANCE = 1.0e-11

# Relative tolerance asked of the adaptive quadrature.
QUADRATURE_RELATIVE_TOLERANCE = 1.0e-11

# Integrand of three variables.
Integrand = Callable[[float, float, float], float]

# Order labels of the six forms, keyed by the name of the function that evaluates the form.
ORDER_LABELS = {
    "dy_dz_dx": "dy dz dx",
    "dy_dx_dz": "dy dx dz",
    "dz_dy_dx": "dz dy dx",
    "dz_dx_dy": "dz dx dy",
    "dx_dz_dy": "dx dz dy",
    "dx_dy_dz": "dx dy dz",
}


def evaluate_dy_dz_dx(function: Integrand) -> tuple[float, float]:
    """Evaluate the form with the inner integral in y, then z, then x.

    The integral is the iterated integral of f over
    -2 <= x <= 2, -sqrt(4 - x**2)/2 <= z <= sqrt(4 - x**2)/2, 0 <= y <= 4 - x**2 - 4*z**2.

    Args:
        function: Integrand of the three coordinates.

    Returns:
        The value and the estimated absolute error.
    """
    return tplquad(
        lambda inner_y, middle_z, outer_x: function(outer_x, inner_y, middle_z),
        -2.0,
        2.0,
        lambda outer_x: -math.sqrt(max(4.0 - outer_x**2, 0.0)) / 2.0,
        lambda outer_x: math.sqrt(max(4.0 - outer_x**2, 0.0)) / 2.0,
        lambda outer_x, middle_z: 0.0,
        lambda outer_x, middle_z: 4.0 - outer_x**2 - 4.0 * middle_z**2,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=QUADRATURE_RELATIVE_TOLERANCE,
    )


def evaluate_dy_dx_dz(function: Integrand) -> tuple[float, float]:
    """Evaluate the form with the inner integral in y, then x, then z.

    The integral is the iterated integral of f over
    -1 <= z <= 1, -2*sqrt(1 - z**2) <= x <= 2*sqrt(1 - z**2), 0 <= y <= 4 - x**2 - 4*z**2.

    Args:
        function: Integrand of the three coordinates.

    Returns:
        The value and the estimated absolute error.
    """
    return tplquad(
        lambda inner_y, middle_x, outer_z: function(middle_x, inner_y, outer_z),
        -1.0,
        1.0,
        lambda outer_z: -2.0 * math.sqrt(max(1.0 - outer_z**2, 0.0)),
        lambda outer_z: 2.0 * math.sqrt(max(1.0 - outer_z**2, 0.0)),
        lambda outer_z, middle_x: 0.0,
        lambda outer_z, middle_x: 4.0 - middle_x**2 - 4.0 * outer_z**2,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=QUADRATURE_RELATIVE_TOLERANCE,
    )


def evaluate_dz_dy_dx(function: Integrand) -> tuple[float, float]:
    """Evaluate the form with the inner integral in z, then y, then x.

    The integral is the iterated integral of f over
    -2 <= x <= 2, 0 <= y <= 4 - x**2,
    -sqrt(4 - x**2 - y)/2 <= z <= sqrt(4 - x**2 - y)/2.

    Args:
        function: Integrand of the three coordinates.

    Returns:
        The value and the estimated absolute error.
    """
    return tplquad(
        lambda inner_z, middle_y, outer_x: function(outer_x, middle_y, inner_z),
        -2.0,
        2.0,
        lambda outer_x: 0.0,
        lambda outer_x: max(4.0 - outer_x**2, 0.0),
        lambda outer_x, middle_y: -math.sqrt(max(4.0 - outer_x**2 - middle_y, 0.0)) / 2.0,
        lambda outer_x, middle_y: math.sqrt(max(4.0 - outer_x**2 - middle_y, 0.0)) / 2.0,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=QUADRATURE_RELATIVE_TOLERANCE,
    )


def evaluate_dz_dx_dy(function: Integrand) -> tuple[float, float]:
    """Evaluate the form with the inner integral in z, then x, then y.

    The integral is the iterated integral of f over
    0 <= y <= 4, -sqrt(4 - y) <= x <= sqrt(4 - y),
    -sqrt(4 - y - x**2)/2 <= z <= sqrt(4 - y - x**2)/2.

    Args:
        function: Integrand of the three coordinates.

    Returns:
        The value and the estimated absolute error.
    """
    return tplquad(
        lambda inner_z, middle_x, outer_y: function(middle_x, outer_y, inner_z),
        0.0,
        4.0,
        lambda outer_y: -math.sqrt(max(4.0 - outer_y, 0.0)),
        lambda outer_y: math.sqrt(max(4.0 - outer_y, 0.0)),
        lambda outer_y, middle_x: -math.sqrt(max(4.0 - outer_y - middle_x**2, 0.0)) / 2.0,
        lambda outer_y, middle_x: math.sqrt(max(4.0 - outer_y - middle_x**2, 0.0)) / 2.0,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=QUADRATURE_RELATIVE_TOLERANCE,
    )


def evaluate_dx_dz_dy(function: Integrand) -> tuple[float, float]:
    """Evaluate the form with the inner integral in x, then z, then y.

    The integral is the iterated integral of f over
    0 <= y <= 4, -sqrt(4 - y)/2 <= z <= sqrt(4 - y)/2,
    -sqrt(4 - y - 4*z**2) <= x <= sqrt(4 - y - 4*z**2).

    Args:
        function: Integrand of the three coordinates.

    Returns:
        The value and the estimated absolute error.
    """
    return tplquad(
        lambda inner_x, middle_z, outer_y: function(inner_x, outer_y, middle_z),
        0.0,
        4.0,
        lambda outer_y: -math.sqrt(max(4.0 - outer_y, 0.0)) / 2.0,
        lambda outer_y: math.sqrt(max(4.0 - outer_y, 0.0)) / 2.0,
        lambda outer_y, middle_z: -math.sqrt(max(4.0 - outer_y - 4.0 * middle_z**2, 0.0)),
        lambda outer_y, middle_z: math.sqrt(max(4.0 - outer_y - 4.0 * middle_z**2, 0.0)),
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=QUADRATURE_RELATIVE_TOLERANCE,
    )


def evaluate_dx_dy_dz(function: Integrand) -> tuple[float, float]:
    """Evaluate the form with the inner integral in x, then y, then z.

    The integral is the iterated integral of f over
    -1 <= z <= 1, 0 <= y <= 4 - 4*z**2,
    -sqrt(4 - 4*z**2 - y) <= x <= sqrt(4 - 4*z**2 - y).

    Args:
        function: Integrand of the three coordinates.

    Returns:
        The value and the estimated absolute error.
    """
    return tplquad(
        lambda inner_x, middle_y, outer_z: function(inner_x, middle_y, outer_z),
        -1.0,
        1.0,
        lambda outer_z: 0.0,
        lambda outer_z: max(4.0 - 4.0 * outer_z**2, 0.0),
        lambda outer_z, middle_y: -math.sqrt(max(4.0 - 4.0 * outer_z**2 - middle_y, 0.0)),
        lambda outer_z, middle_y: math.sqrt(max(4.0 - 4.0 * outer_z**2 - middle_y, 0.0)),
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=QUADRATURE_RELATIVE_TOLERANCE,
    )


def integrators() -> dict[str, Callable[[Integrand], tuple[float, float]]]:
    """Return the six integrators, keyed by the name of the form.

    Returns:
        A dictionary from the form name to the function that evaluates that form.
    """
    return {
        "dy_dz_dx": evaluate_dy_dz_dx,
        "dy_dx_dz": evaluate_dy_dx_dz,
        "dz_dy_dx": evaluate_dz_dy_dx,
        "dz_dx_dy": evaluate_dz_dx_dy,
        "dx_dz_dy": evaluate_dx_dz_dy,
        "dx_dy_dz": evaluate_dx_dy_dz,
    }


def limits_are_met(form_name: str, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> NDArray[np.bool_]:
    """Return True where a point satisfies the three limit conditions of one form.

    The test reads the limits from the docstring of the matching integrator and applies them
    as inequalities, so a sampling check can compare these limits with the defining
    inequalities of the solid.

    Args:
        form_name: Name of the form, one of the keys of ORDER_LABELS.
        x: Coordinate along the axis x.
        y: Coordinate along the axis y.
        z: Coordinate along the axis z.

    Returns:
        A Boolean array with the result of the three tests, combined by "and".
    """
    x_array, y_array, z_array = np.broadcast_arrays(
        np.asarray(x, dtype=float), np.asarray(y, dtype=float), np.asarray(z, dtype=float)
    )
    if form_name == "dy_dz_dx":
        outer = np.abs(x_array) <= 2.0
        middle = np.abs(z_array) <= np.sqrt(np.maximum(4.0 - x_array**2, 0.0)) / 2.0
        inner = (y_array >= 0.0) & (y_array <= 4.0 - x_array**2 - 4.0 * z_array**2)
    elif form_name == "dy_dx_dz":
        outer = np.abs(z_array) <= 1.0
        middle = np.abs(x_array) <= 2.0 * np.sqrt(np.maximum(1.0 - z_array**2, 0.0))
        inner = (y_array >= 0.0) & (y_array <= 4.0 - x_array**2 - 4.0 * z_array**2)
    elif form_name == "dz_dy_dx":
        outer = np.abs(x_array) <= 2.0
        middle = (y_array >= 0.0) & (y_array <= 4.0 - x_array**2)
        inner = np.abs(z_array) <= np.sqrt(np.maximum(4.0 - x_array**2 - y_array, 0.0)) / 2.0
    elif form_name == "dz_dx_dy":
        outer = (y_array >= 0.0) & (y_array <= 4.0)
        middle = np.abs(x_array) <= np.sqrt(np.maximum(4.0 - y_array, 0.0))
        inner = np.abs(z_array) <= np.sqrt(
            np.maximum(4.0 - y_array - x_array**2, 0.0)
        ) / 2.0
    elif form_name == "dx_dz_dy":
        outer = (y_array >= 0.0) & (y_array <= 4.0)
        middle = np.abs(z_array) <= np.sqrt(np.maximum(4.0 - y_array, 0.0)) / 2.0
        inner = np.abs(x_array) <= np.sqrt(np.maximum(4.0 - y_array - 4.0 * z_array**2, 0.0))
    elif form_name == "dx_dy_dz":
        outer = np.abs(z_array) <= 1.0
        middle = (y_array >= 0.0) & (y_array <= 4.0 - 4.0 * z_array**2)
        inner = np.abs(x_array) <= np.sqrt(np.maximum(4.0 - 4.0 * z_array**2 - y_array, 0.0))
    else:
        raise ValueError(f"unknown form name: {form_name}")
    return np.asarray(outer & middle & inner)
