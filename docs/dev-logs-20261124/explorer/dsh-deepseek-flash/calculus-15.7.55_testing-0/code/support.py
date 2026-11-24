"""Support module for the tutorial of Problem 15.7.55.

The module describes the integrand $f = 1 - x^2 - 2y^2 - 3z^2$, the solid ellipsoid
$P = {x^2 + 2y^2 + 3z^2 <= 1}$, several independent integration routes, and a check ledger.
Each part script compares a value from one route with a value from a different route, so that no
comparison holds the same expression on both sides.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Sequence

import numpy as np
from scipy import integrate

SQUARE_ROOT_OF_SIX = math.sqrt(6.0)
COEFFICIENT_X_SQUARED = 1.0
COEFFICIENT_Y_SQUARED = 2.0
COEFFICIENT_Z_SQUARED = 3.0
GEOMETRY_TOLERANCE = 1.0e-9
QUADRATURE_ABSOLUTE_TOLERANCE = 1.0e-12
QUADRATURE_RELATIVE_TOLERANCE = 1.0e-12
RELATIVE_DIFFERENCE_LIMIT = 1.0e-6
MONTE_CARLO_STANDARD_ERROR_FACTOR = 4.0
BOUNDING_BOX_HALF_WIDTH = 1.0
BOUNDING_BOX_VOLUME = (2.0 * BOUNDING_BOX_HALF_WIDTH) ** 3

ScalarField = Callable[[float, float, float], float]


def quadratic_form(x: float, y: float, z: float) -> float:
    """Return the value of $Q = x^2 + 2y^2 + 3z^2$ at one point."""
    return (COEFFICIENT_X_SQUARED * x * x
            + COEFFICIENT_Y_SQUARED * y * y
            + COEFFICIENT_Z_SQUARED * z * z)


def integrand(x: float, y: float, z: float) -> float:
    """Return the value of $f = 1 - x^2 - 2y^2 - 3z^2$ at one point."""
    return 1.0 - quadratic_form(x, y, z)


def quadratic_form_array(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return $Q$ on three arrays of coordinates."""
    return (COEFFICIENT_X_SQUARED * x * x
            + COEFFICIENT_Y_SQUARED * y * y
            + COEFFICIENT_Z_SQUARED * z * z)


def integrand_array(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return $f$ on three arrays of coordinates."""
    return 1.0 - quadratic_form_array(x, y, z)


def ellipsoid_semi_axes() -> tuple[float, float, float]:
    """Return the three semi-axes of $P$, taken from the coefficients of $Q$."""
    return (1.0 / math.sqrt(COEFFICIENT_X_SQUARED),
            1.0 / math.sqrt(COEFFICIENT_Y_SQUARED),
            1.0 / math.sqrt(COEFFICIENT_Z_SQUARED))


def ellipsoid_volume_closed_form() -> float:
    """Return $4\\pi a b c / 3$ for the semi-axes of $P$."""
    first, second, third = ellipsoid_semi_axes()
    return 4.0 * math.pi * first * second * third / 3.0


def ellipsoid_volume_from_axes_product() -> float:
    """Return $4\\pi/(3\\sqrt{6})$, the volume written with the product of the coefficients."""
    return 4.0 * math.pi / (3.0 * SQUARE_ROOT_OF_SIX)


def cross_section_semi_axes(height: float) -> tuple[float, float]:
    """Return the two semi-axes of the section of $P$ at the fixed $z$, from the inequality."""
    remaining = 1.0 - COEFFICIENT_Z_SQUARED * height * height
    if remaining <= 0.0:
        return (0.0, 0.0)
    return (math.sqrt(remaining),
            math.sqrt(remaining / COEFFICIENT_Y_SQUARED / COEFFICIENT_X_SQUARED))


def cross_section_half_width_x(height: float, y: float) -> float:
    """Return the half width in $x$ of the section at the fixed $z$ and the fixed $y$."""
    remaining = 1.0 - COEFFICIENT_Z_SQUARED * height * height - COEFFICIENT_Y_SQUARED * y * y
    if remaining <= 0.0:
        return 0.0
    return math.sqrt(remaining / COEFFICIENT_X_SQUARED)


def cross_section_area_formula(height: float) -> float:
    """Return $\\pi a(z) b(z)$ for the section at the fixed $z$."""
    first, second = cross_section_semi_axes(height)
    return math.pi * first * second


def cross_section_area_quadrature(height: float) -> float:
    """Return the area of the section at the fixed $z$ by an integral of its width in $y$."""
    _, half_height = cross_section_semi_axes(height)
    if half_height <= 0.0:
        return 0.0
    value, _ = integrate.quad(
        lambda y: 2.0 * cross_section_half_width_x(height, y), -half_height, half_height,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)
    return value


def cross_section_area_numeric_limit(height: float) -> float:
    """Return the area of the section at the fixed $z$ by a two-dimensional Monte Carlo sample."""
    first, second = cross_section_semi_axes(height)
    generator = np.random.default_rng(20261123 + int(round(1000.0 * height)))
    sample_count = 400000
    x = generator.uniform(-first, first, sample_count)
    y = generator.uniform(-second, second, sample_count)
    inside = quadratic_form_array(x, y, np.full(sample_count, height)) <= 1.0
    return 4.0 * first * second * float(np.mean(inside))


def integrate_cross_section_areas() -> float:
    """Return the volume of $P$ by an integral of the section areas over the height."""
    half_height = 1.0 / math.sqrt(COEFFICIENT_Z_SQUARED)
    value, _ = integrate.quad(
        cross_section_area_formula, -half_height, half_height,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)
    return value


def integrate_cartesian(field: ScalarField) -> float:
    """Integrate a field over $P$ in the order $dz$, then $dy$, then $dx$."""
    def middle(x: float, y: float) -> float:
        remaining = 1.0 - x * x - COEFFICIENT_Y_SQUARED * y * y
        if remaining <= 0.0:
            return 0.0
        half_height = math.sqrt(remaining / COEFFICIENT_Z_SQUARED)
        value, _ = integrate.quad(
            lambda z: field(x, y, z), -half_height, half_height,
            epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)
        return value

    def outer(x: float) -> float:
        half_width = math.sqrt(max(0.0, 1.0 - x * x) / COEFFICIENT_Y_SQUARED)
        value, _ = integrate.quad(
            lambda y: middle(x, y), -half_width, half_width,
            epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)
        return value

    value, _ = integrate.quad(
        outer, -1.0, 1.0,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)
    return value


def integrate_gauss_legendre_scaled(field: ScalarField, order: int) -> float:
    """Integrate a field over $P$ with the Jacobian of the three interval maps included."""
    nodes, weights = np.polynomial.legendre.leggauss(order)
    total = 0.0
    for node_x, weight_x in zip(nodes, weights):
        x = node_x
        half_width = math.sqrt(max(0.0, 1.0 - x * x) / COEFFICIENT_Y_SQUARED)
        for node_y, weight_y in zip(nodes, weights):
            y = half_width * node_y
            remaining = 1.0 - x * x - COEFFICIENT_Y_SQUARED * y * y
            if remaining <= 0.0:
                continue
            half_height = math.sqrt(remaining / COEFFICIENT_Z_SQUARED)
            inner = 0.0
            for node_z, weight_z in zip(nodes, weights):
                inner += weight_z * field(x, y, half_height * node_z)
            total += weight_x * weight_y * half_width * half_height * inner
    return total


def monte_carlo_ellipsoid(field: ScalarField, sample_count: int, seed: int) -> tuple[float, float]:
    """Estimate the integral of a field over $P$ by a uniform sample of the bounding box."""
    generator = np.random.default_rng(seed)
    x = generator.uniform(-BOUNDING_BOX_HALF_WIDTH, BOUNDING_BOX_HALF_WIDTH, sample_count)
    y = generator.uniform(-BOUNDING_BOX_HALF_WIDTH, BOUNDING_BOX_HALF_WIDTH, sample_count)
    z = generator.uniform(-BOUNDING_BOX_HALF_WIDTH, BOUNDING_BOX_HALF_WIDTH, sample_count)
    inside = quadratic_form_array(x, y, z) <= 1.0
    weight = np.where(inside, integrand_array(x, y, z), 0.0)
    estimate = BOUNDING_BOX_VOLUME * float(np.mean(weight))
    error = BOUNDING_BOX_VOLUME * float(np.std(weight, ddof=1)) / math.sqrt(sample_count)
    return estimate, error


def monte_carlo_ellipsoid_mean(field: ScalarField, sample_count: int, seed: int
                               ) -> tuple[float, float]:
    """Estimate the mean of a field over $P$ by rejection sampling of the bounding box."""
    generator = np.random.default_rng(seed)
    collected: list[np.ndarray] = []
    kept = 0
    while kept < sample_count:
        x = generator.uniform(-1.0, 1.0, sample_count)
        y = generator.uniform(-1.0, 1.0, sample_count)
        z = generator.uniform(-1.0, 1.0, sample_count)
        inside = quadratic_form_array(x, y, z) <= 1.0
        values = np.array([field(cx, cy, cz)
                           for cx, cy, cz in zip(x[inside], y[inside], z[inside])])
        collected.append(values)
        kept += int(values.size)
    sample = np.concatenate(collected)[:sample_count]
    return float(np.mean(sample)), float(np.std(sample, ddof=1)) / math.sqrt(sample_count)


def exact_maximum_value() -> float:
    """Return $8\\pi/(15\\sqrt{6})$ from the substitution route."""
    return 8.0 * math.pi / (15.0 * SQUARE_ROOT_OF_SIX)


def exact_maximum_value_rationalized() -> float:
    """Return $4\\pi\\sqrt{6}/45$, the same value with the root moved to the numerator."""
    return 4.0 * math.pi * SQUARE_ROOT_OF_SIX / 45.0


def exact_quadratic_form_moment() -> float:
    """Return $\\int_P Q\\,dV = 4\\pi/(5\\sqrt{6})$ from the substitution route."""
    return 4.0 * math.pi / (5.0 * SQUARE_ROOT_OF_SIX)


def ball_integral_closed_form(radius: float) -> float:
    """Return $4\\pi R^3/3 - 8\\pi R^5/5$, the integral of $f$ over the ball of that radius."""
    return (4.0 * math.pi * radius ** 3 / 3.0
            - 8.0 * math.pi * radius ** 5 / 5.0)


def ball_integral_quadrature(radius: float) -> float:
    """Return the integral of $f$ over the ball of that radius by an iterated quadrature."""
    def middle(x: float, y: float) -> float:
        remaining = radius * radius - x * x - y * y
        if remaining <= 0.0:
            return 0.0
        height = math.sqrt(remaining)
        value, _ = integrate.quad(
            lambda z: integrand(x, y, z), -height, height,
            epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)
        return value

    value, _ = integrate.quad(
        lambda x: integrate.quad(
            lambda y: middle(x, y), -math.sqrt(max(0.0, radius * radius - x * x)),
            math.sqrt(max(0.0, radius * radius - x * x)),
            epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)[0],
        -radius, radius,
        epsabs=QUADRATURE_ABSOLUTE_TOLERANCE, epsrel=QUADRATURE_RELATIVE_TOLERANCE)
    return value


def cube_integral_closed_form(half_side: float) -> float:
    """Return $8h^3 - 16h^5$, the integral of $f$ over the cube of that half side."""
    volume = (2.0 * half_side) ** 3
    moment = (2.0 * half_side) ** 3 * half_side ** 2 / 3.0 * 6.0
    return volume - moment


def cube_integral_quadrature(half_side: float) -> float:
    """Return the integral of $f$ over the cube of that half side by a Gauss-Legendre rule."""
    nodes, weights = np.polynomial.legendre.leggauss(40)
    total = 0.0
    for node_x, weight_x in zip(nodes, weights):
        for node_y, weight_y in zip(nodes, weights):
            for node_z, weight_z in zip(nodes, weights):
                total += (weight_x * weight_y * weight_z * half_side ** 3
                          * integrand(half_side * node_x, half_side * node_y, half_side * node_z))
    return total


def scaled_ellipsoid_integral_closed_form(scale: float) -> float:
    """Return $s^3 V - s^5 J$ for the ellipsoid $P$ scaled by the factor $s$."""
    return (scale ** 3 * ellipsoid_volume_closed_form()
            - scale ** 5 * exact_quadratic_form_moment())


def offset_matrix_determinant() -> float:
    """Return the determinant of the diagonal matrix of the three scale factors."""
    matrix = np.diag([1.0 / math.sqrt(COEFFICIENT_X_SQUARED),
                      1.0 / math.sqrt(COEFFICIENT_Y_SQUARED),
                      1.0 / math.sqrt(COEFFICIENT_Z_SQUARED)])
    return float(abs(np.linalg.det(matrix)))


def spherical_angular_integral() -> float:
    """Return $\\int_0^{2\\pi}\\int_0^{\\pi}\\sin\\theta\\,d\\theta\\,d\\phi$ by quadrature."""
    inner, _ = integrate.quad(lambda theta: math.sin(theta), 0.0, math.pi,
                              epsabs=QUADRATURE_ABSOLUTE_TOLERANCE,
                              epsrel=QUADRATURE_RELATIVE_TOLERANCE)
    outer, _ = integrate.quad(lambda phi: inner, 0.0, 2.0 * math.pi,
                              epsabs=QUADRATURE_ABSOLUTE_TOLERANCE,
                              epsrel=QUADRATURE_RELATIVE_TOLERANCE)
    return outer


def radial_integral_exact() -> float:
    """Return $\\int_0^1 (1 - r^2) r^2\\,dr = 2/15$ from the antiderivative."""
    return 1.0 / 3.0 - 1.0 / 5.0


def radial_integral_quadrature() -> float:
    """Return the same radial integral by a Gauss-Legendre rule on the unit interval."""
    nodes, weights = np.polynomial.legendre.leggauss(40)
    total = 0.0
    for node, weight in zip(nodes, weights):
        radius = 0.5 * (node + 1.0)
        total += weight * 0.5 * (1.0 - radius * radius) * radius * radius
    return total


def cumulative_radial_integral(radii: Sequence[float]) -> list[float]:
    """Return $\\int_0^{R} (1 - r^2) r^2\\,dr$ at each radius by a cumulative quadrature."""
    values: list[float] = []
    for radius in radii:
        value, _ = integrate.quad(lambda r: (1.0 - r * r) * r * r, 0.0, radius,
                                  epsabs=QUADRATURE_ABSOLUTE_TOLERANCE,
                                  epsrel=QUADRATURE_RELATIVE_TOLERANCE)
        values.append(value)
    return values


def transformed_integrand(u: float, v: float, w: float) -> float:
    """Return $1 - u^2 - v^2 - w^2$, the integrand after the change of variable."""
    return 1.0 - (u * u + v * v + w * w)


def boundary_residual(point: tuple[float, float, float]) -> float:
    """Return $Q - 1$ at one point, so that a boundary point gives zero."""
    return quadratic_form(*point) - 1.0


def half_extent_by_root_finding(height: float, direction: str) -> float:
    """Return the half extent of the section at the fixed $z$ along one axis by root finding."""
    from scipy import optimize

    semi_axes = cross_section_semi_axes(height)
    guess = semi_axes[0] if direction == "x" else semi_axes[1]
    if guess <= 0.0:
        return 0.0

    def residual(t: float) -> float:
        if direction == "x":
            return quadratic_form(t, 0.0, height) - 1.0
        return quadratic_form(0.0, t, height) - 1.0

    return float(optimize.brentq(residual, 0.0, 2.0 * guess + 1.0e-3))


def axis_intercept_by_root_finding(axis: str) -> float:
    """Return the positive intercept of $P$ on one coordinate axis by root finding."""
    from scipy import optimize

    index = {"x": 0, "y": 1, "z": 2}[axis]
    coefficient = {0: COEFFICIENT_X_SQUARED, 1: COEFFICIENT_Y_SQUARED,
                   2: COEFFICIENT_Z_SQUARED}[index]

    def residual(t: float) -> float:
        point = [0.0, 0.0, 0.0]
        point[index] = t
        return quadratic_form(*point) - 1.0

    return float(optimize.brentq(residual, 0.0, 2.0 / math.sqrt(coefficient) + 1.0e-3))


@dataclass
class CheckRecord:
    """One comparison of a computed value with an expected value from a different method."""

    name: str
    computed: float
    expected: float
    tolerance: float
    unit: str = ""


@dataclass
class CheckLedger:
    """The collection of checks of one part script."""

    part: str
    records: list[CheckRecord] = field(default_factory=list)

    def add(self, name: str, computed: float, expected: float, tolerance: float,
            unit: str = "") -> None:
        """Record one check and print the two compared values and the verdict."""
        passed = abs(computed - expected) <= tolerance
        self.records.append(CheckRecord(name, computed, expected, tolerance, unit))
        print(f"CHECK {name}")
        print(f"  computed = {computed!r}")
        print(f"  expected = {expected!r}")
        print(f"  difference = {abs(computed - expected):.6e}  tolerance = {tolerance:.6e}"
              f"  {'PASS' if passed else 'FAIL'}")
        if not passed:
            raise AssertionError(f"check failed: {name}")

    def add_gap(self, name: str, larger: float, smaller: float, minimum_gap: float) -> None:
        """Record one check that one computed value exceeds another by a stated gap."""
        gap = larger - smaller
        print(f"CHECK {name}")
        print(f"  larger value = {larger!r}")
        print(f"  smaller value = {smaller!r}")
        print(f"  gap = {gap:.6f}  required gap = {minimum_gap:.6f}"
              f"  {'PASS' if gap >= minimum_gap else 'FAIL'}")
        if gap < minimum_gap:
            raise AssertionError(f"check failed: {name}")
        self.records.append(CheckRecord(name, larger, smaller, minimum_gap))

    def add_text(self, name: str, computed: str, expected: str) -> None:
        """Record one check of a text value, and print the two compared values."""
        passed = computed == expected
        print(f"CHECK {name}")
        print(f"  computed = {computed}")
        print(f"  expected = {expected}")
        print(f"  {'PASS' if passed else 'FAIL'}")
        if not passed:
            raise AssertionError(f"check failed: {name}")

    def summary(self) -> dict[str, object]:
        """Return the pass count and the rows of the ledger for the product page."""
        rows = [
            {
                "name": record.name,
                "computed": record.computed,
                "expected": record.expected,
                "difference": abs(record.computed - record.expected),
                "tolerance": record.tolerance,
            }
            for record in self.records
        ]
        return {"part": self.part, "count": len(rows), "rows": rows}


def write_results(path: Path, payload: dict[str, object]) -> None:
    """Write one JSON result file, so that the composed page reads every number from a print."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relative_difference(first: float, second: float) -> float:
    """Return the relative difference of two values against the larger magnitude."""
    scale = max(abs(first), abs(second))
    if scale == 0.0:
        return 0.0
    return abs(first - second) / scale
