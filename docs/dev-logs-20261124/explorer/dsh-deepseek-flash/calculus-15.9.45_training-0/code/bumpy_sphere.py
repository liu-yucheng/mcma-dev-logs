"""Geometry and exact algebra of the bumpy sphere of Section 15.9, Exercise 45.

The surface is ``rho(theta, phi) = 1 + amplitude * sin(theta_wave * theta) * sin(phi_wave * phi)``
with ``amplitude = 1/5``, ``theta_wave = 6``, and ``phi_wave = 5``.  This module holds three kinds
of object:

* the constants of the surface, which every figure and every check reads from this one place;
* an exact trigonometric polynomial with rational coefficients, which integrates the surface
  without a floating point number;
* two numeric estimators of the volume, which share no code with the exact route.

An exact value is a :class:`PiValue`, that is a rational number plus a rational multiple of
``pi``.  The product of two ``PiValue`` objects is refused when both carry a ``pi`` part, because
such a product would hold ``pi`` squared and no quantity of this problem needs it.
"""

from __future__ import annotations

import dataclasses
import math
from fractions import Fraction

import numpy as np
import scipy.integrate

AMPLITUDE = Fraction(1, 5)
"""Coefficient of the bump term of the surface."""

THETA_WAVE = 6
"""Number of bumps around the vertical axis, that is the integer ``m`` of the statement."""

PHI_WAVE = 5
"""Number of bump bands from pole to pole, that is the integer ``n`` of the statement."""

RADIUS_MAXIMUM = Fraction(6, 5)
"""Largest radial distance of the surface, reached where both sine factors equal one."""

RADIUS_MINIMUM = Fraction(4, 5)
"""Smallest radial distance of the surface, reached where both sine factors equal minus one."""

BOX_HALF_WIDTH = 1.3
"""Half width of the cube that contains the surface, used by the sampling estimators."""

LOBE_THETA = math.pi / 12.0
"""Polar angle of the marked bump peak, where ``sin(6 theta) = 1``."""

LOBE_PHI = math.pi / 10.0
"""Azimuthal angle of the marked bump peak, where ``sin(5 varphi) = 1``."""

VALLEY_THETA = 5.0 * math.pi / 12.0
"""Polar angle of the marked valley, where ``sin(6 theta) = 1`` and ``sin(5 varphi) = -1``."""

VALLEY_PHI = 3.0 * math.pi / 10.0
"""Azimuthal angle of the marked valley, where ``sin(5 varphi) = -1``."""

VIEW_ELEVATION = 22.0
"""Elevation in degrees of the camera of Figure 1."""

VIEW_AZIMUTH = 34.0
"""Azimuth in degrees of the camera of Figure 1."""

COLOR_MAP = "viridis"
"""Colour map of the drawn surface."""


def radius(theta: float, phi: float) -> float:
    """Return the radial distance of the surface at one pair of angles.

    Args:
        theta: Azimuthal angle in radians.
        phi: Polar angle in radians, measured from the positive ``z`` axis.

    Returns:
        The radial distance ``1 + (1/5) sin(6 theta) sin(5 phi)``.
    """
    return float(1.0 + float(AMPLITUDE) * math.sin(THETA_WAVE * theta)
                 * math.sin(PHI_WAVE * phi))


def radius_array(theta: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """Return the radial distance of the surface on a grid of angles.

    Args:
        theta: Array of azimuthal angles in radians.
        phi: Array of polar angles in radians.

    Returns:
        The array of radial distances, with the broadcast shape of the two arguments.
    """
    return 1.0 + float(AMPLITUDE) * np.sin(THETA_WAVE * theta) * np.sin(PHI_WAVE * phi)


def to_cartesian(
    theta: np.ndarray,
    phi: np.ndarray,
    rho: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the Cartesian coordinates of points given in spherical coordinates.

    Args:
        theta: Array of azimuthal angles in radians.
        phi: Array of polar angles in radians.
        rho: Array of radial distances.

    Returns:
        The three arrays ``x``, ``y``, and ``z`` of the Cartesian coordinates.
    """
    return (
        rho * np.sin(phi) * np.cos(theta),
        rho * np.sin(phi) * np.sin(theta),
        rho * np.cos(phi),
    )


@dataclasses.dataclass(frozen=True)
class PiValue:
    """An exact number of the form ``rational + pi_multiple * pi``."""

    rational: Fraction = Fraction(0)
    """Rational part of the number."""

    pi_multiple: Fraction = Fraction(0)
    """Coefficient of ``pi`` in the number."""

    def __add__(self, other: "PiValue") -> "PiValue":
        """Return the exact sum of this number and another number."""
        return PiValue(self.rational + other.rational, self.pi_multiple + other.pi_multiple)

    def scaled(self, factor: Fraction) -> "PiValue":
        """Return this number multiplied by an exact rational factor."""
        return PiValue(self.rational * factor, self.pi_multiple * factor)

    def multiplied(self, other: "PiValue") -> "PiValue":
        """Return the exact product of this number and a number that holds no ``pi`` part."""
        if self.pi_multiple != 0 and other.pi_multiple != 0:
            raise ValueError("the product would hold pi squared")
        return PiValue(
            self.rational * other.rational,
            self.pi_multiple * other.rational + self.rational * other.pi_multiple,
        )

    def as_float(self) -> float:
        """Return the floating point value of this number."""
        return float(self.rational) + float(self.pi_multiple) * math.pi


class TrigPolynomial:
    """A finite trigonometric polynomial with exact rational coefficients.

    A term is a pair of a kind and a frequency.  The three kinds are ``"const"``, ``"cos"``, and
    ``"sin"``.  A frequency is a non-negative integer, and the frequency of a constant term is
    zero.  The class integrates a polynomial over ``[0, 2 pi]`` and over ``[0, pi]`` without a
    floating point number, because the only non-zero integrals of the basis are the constant term
    and the odd sine terms.
    """

    def __init__(self, terms: dict[tuple[str, int], Fraction] | None = None) -> None:
        """Create a polynomial from a dictionary of terms.

        Args:
            terms: Mapping from a term to its exact coefficient.  A missing argument creates the
                zero polynomial.
        """
        self.terms: dict[tuple[str, int], Fraction] = {}
        for key, coefficient in (terms or {}).items():
            self.add_term(key[0], key[1], coefficient)

    def add_term(self, kind: str, frequency: int, coefficient: Fraction) -> None:
        """Add one term to the polynomial and normalize its sign.

        Args:
            kind: One of ``"const"``, ``"cos"``, and ``"sin"``.
            frequency: Non-negative frequency of the term.
            coefficient: Exact coefficient of the term.
        """
        if coefficient == 0:
            return
        if kind == "const" or frequency == 0:
            if kind == "sin":
                return
            key = ("const", 0)
        elif frequency < 0:
            key = ("cos" if kind == "cos" else "sin", -frequency)
            coefficient = coefficient if kind == "cos" else -coefficient
        else:
            key = (kind, frequency)
        total = self.terms.get(key, Fraction(0)) + coefficient
        if total == 0:
            self.terms.pop(key, None)
        else:
            self.terms[key] = total

    @staticmethod
    def sine(harmonic: int) -> "TrigPolynomial":
        """Return the polynomial ``sin(harmonic * x)``.

        Args:
            harmonic: Positive integer frequency of the sine term.
        """
        return TrigPolynomial({("sin", harmonic): Fraction(1)})

    @staticmethod
    def product_terms(
        kind_first: str,
        frequency_first: int,
        kind_second: str,
        frequency_second: int,
    ) -> list[tuple[str, int, Fraction]]:
        """Return the product-to-sum expansion of one pair of basis terms.

        Args:
            kind_first: Kind of the first term.
            frequency_first: Frequency of the first term.
            kind_second: Kind of the second term.
            frequency_second: Frequency of the second term.

        Returns:
            A list of triples ``(kind, frequency, coefficient)`` whose sum equals the product.
        """
        if kind_first == "const":
            return [(kind_second, frequency_second, Fraction(1))]
        if kind_second == "const":
            return [(kind_first, frequency_first, Fraction(1))]
        half = Fraction(1, 2)
        if kind_first == "cos" and kind_second == "cos":
            return [("cos", frequency_first - frequency_second, half),
                    ("cos", frequency_first + frequency_second, half)]
        if kind_first == "sin" and kind_second == "sin":
            return [("cos", frequency_first - frequency_second, half),
                    ("cos", frequency_first + frequency_second, -half)]
        if kind_first == "sin":
            return [("sin", frequency_first + frequency_second, half),
                    ("sin", frequency_first - frequency_second, half)]
        return [("sin", frequency_first + frequency_second, half),
                ("sin", frequency_second - frequency_first, half)]

    def multiplied(self, other: "TrigPolynomial") -> "TrigPolynomial":
        """Return the exact product of this polynomial and another polynomial.

        Args:
            other: The second factor.
        """
        result = TrigPolynomial()
        for (kind_first, frequency_first), coefficient_first in self.terms.items():
            for (kind_second, frequency_second), coefficient_second in other.terms.items():
                for kind, frequency, factor in self.product_terms(
                    kind_first, frequency_first, kind_second, frequency_second
                ):
                    result.add_term(kind, frequency, coefficient_first * coefficient_second * factor)
        return result

    def power(self, exponent: int) -> "TrigPolynomial":
        """Return this polynomial raised to a non-negative integer power.

        Args:
            exponent: Non-negative integer exponent.
        """
        result = TrigPolynomial({("const", 0): Fraction(1)})
        for _ in range(exponent):
            result = result.multiplied(self)
        return result

    def constant_coefficient(self) -> Fraction:
        """Return the exact coefficient of the constant term."""
        return self.terms.get(("const", 0), Fraction(0))

    def integral_over_full_turn(self) -> PiValue:
        """Return the exact integral over ``[0, 2 pi]``."""
        return PiValue(Fraction(0), 2 * self.constant_coefficient())

    def integral_over_half_turn(self) -> PiValue:
        """Return the exact integral over ``[0, pi]``."""
        total = PiValue(self.constant_coefficient(), Fraction(0))
        for (kind, frequency), coefficient in self.terms.items():
            if kind != "sin":
                continue
            if frequency % 2 == 1:
                total = total + PiValue(coefficient * Fraction(2, frequency), Fraction(0))
        return total


def theta_factor(harmonic: int = THETA_WAVE, power: int = 2) -> Fraction:
    """Return the exact coefficient of ``pi`` in the integral of a sine power over one turn.

    Args:
        harmonic: Frequency of the sine term.
        power: Positive integer power.

    Returns:
        The exact number ``c`` with ``integral of sin(harmonic*x)**power over [0, 2 pi] = c * pi``.
    """
    polynomial = TrigPolynomial.sine(harmonic).power(power)
    value = polynomial.integral_over_full_turn()
    if value.rational != 0:
        raise ValueError("the integral over a full turn must be a multiple of pi")
    return value.pi_multiple


def phi_factor(harmonic: int = PHI_WAVE, power: int = 2) -> Fraction:
    """Return the exact value of the integral of a weighted sine power over a half turn.

    Args:
        harmonic: Frequency of the sine term.
        power: Positive integer power.

    Returns:
        The exact value of the integral of ``sin(harmonic*phi)**power * sin(phi)`` over ``[0, pi]``.
    """
    polynomial = TrigPolynomial.sine(harmonic).power(power).multiplied(
        TrigPolynomial.sine(1)
    )
    value = polynomial.integral_over_half_turn()
    if value.pi_multiple != 0:
        raise ValueError("the weighted integral must hold no pi")
    return value.rational


def exact_volume_of_term(theta_power: int, phi_power: int) -> PiValue:
    """Return the exact volume contribution of one term of the expanded cube.

    The term contributes ``binomial coefficient * amplitude**power * sin(6 theta)**power *
    sin(5 varphi)**power * sin(varphi)`` to the integrand, so its volume is one third of the
    product of the two separated integrals.

    Args:
        theta_power: Power of the sine of the azimuthal angle.
        phi_power: Power of the sine of the polar angle.

    Returns:
        The exact volume of the term.
    """
    coefficient = Fraction(math.comb(3, theta_power)) * AMPLITUDE**theta_power
    azimuthal = PiValue(Fraction(0), theta_factor(THETA_WAVE, theta_power))
    polar = PiValue(phi_factor(PHI_WAVE, phi_power), Fraction(0))
    return azimuthal.multiplied(polar).scaled(coefficient / 3)


def exact_volume() -> PiValue:
    """Return the exact enclosed volume through the full expansion of the cube.

    Returns:
        The exact volume, which holds only a multiple of ``pi``.
    """
    total = PiValue()
    for theta_power in range(4):
        total = total + exact_volume_of_term(theta_power, theta_power)
    return total


def exact_volume_over_pi() -> Fraction:
    """Return the exact volume divided by ``pi`` through the full expansion."""
    value = exact_volume()
    if value.rational != 0:
        raise ValueError("the volume must hold only a multiple of pi")
    return value.pi_multiple


def closed_form_volume_over_pi() -> Fraction:
    """Return the exact volume divided by ``pi`` through the single surviving correction.

    This route uses one product-to-sum identity and the general integral of a sine over a half
    turn.  It never expands the cube, so it fails when the vanishing of the linear and the cubic
    terms is wrong.
    """
    doubled = 2 * PHI_WAVE
    cosine_integral = (
        Fraction(1, 2)
        * (Fraction(1 - (-1) ** (doubled + 1), doubled + 1)
           - Fraction(1 - (-1) ** (doubled - 1), doubled - 1))
    )
    half_turn_sine = Fraction(1 - (-1) ** 1, 1)
    mean_square = Fraction(1, 2) * half_turn_sine - Fraction(1, 2) * cosine_integral
    correction = AMPLITUDE**2 * mean_square
    return Fraction(4, 3) + correction


def numeric_volume_quadrature() -> float:
    """Return the enclosed volume from a two dimensional adaptive quadrature."""
    def integrand(phi: float, theta: float) -> float:
        """Return the radial integrand at one pair of angles."""
        return radius(theta, phi) ** 3 * math.sin(phi) / 3.0

    value, _error = scipy.integrate.dblquad(
        integrand, 0.0, 2.0 * math.pi, lambda _theta: 0.0, lambda _theta: math.pi,
        epsabs=1.0e-13, epsrel=1.0e-13,
    )
    return float(value)


def numeric_volume_monte_carlo(sample_count: int, seed: int) -> tuple[float, float]:
    """Return the enclosed volume from uniform sampling of a cube and its standard error.

    Args:
        sample_count: Number of sampled points.
        seed: Seed of the random number generator.

    Returns:
        The estimated volume and the standard error of the estimate.
    """
    generator = np.random.default_rng(seed)
    points = generator.uniform(-BOX_HALF_WIDTH, BOX_HALF_WIDTH, size=(sample_count, 3))
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    distance = np.sqrt(x * x + y * y + z * z)
    polar = np.arccos(np.clip(z / np.maximum(distance, 1.0e-300), -1.0, 1.0))
    azimuthal = np.mod(np.arctan2(y, x), 2.0 * math.pi)
    inside = distance <= radius_array(azimuthal, polar)
    box_volume = (2.0 * BOX_HALF_WIDTH) ** 3
    fraction = inside.mean()
    estimate = box_volume * fraction
    error = box_volume * math.sqrt(max(fraction * (1.0 - fraction), 0.0) / sample_count)
    return float(estimate), float(error)


def numeric_volume_grid(cell_count: int) -> float:
    """Return the enclosed volume from a midpoint sum over a grid of angles.

    Args:
        cell_count: Number of cells along each angle.
    """
    theta_edges = np.linspace(0.0, 2.0 * math.pi, cell_count + 1)
    phi_edges = np.linspace(0.0, math.pi, cell_count + 1)
    theta_centres = 0.5 * (theta_edges[:-1] + theta_edges[1:])
    phi_centres = 0.5 * (phi_edges[:-1] + phi_edges[1:])
    theta_step = theta_edges[1] - theta_edges[0]
    phi_step = phi_edges[1] - phi_edges[0]
    theta_grid, phi_grid = np.meshgrid(theta_centres, phi_centres)
    values = radius_array(theta_grid, phi_grid) ** 3 * np.sin(phi_grid) / 3.0
    return float(values.sum() * theta_step * phi_step)


def numeric_volume_box_count(sample_count_per_axis: int) -> float:
    """Return the enclosed volume by counting the points of a Cartesian grid inside the body.

    Args:
        sample_count_per_axis: Number of grid points along each axis of the enclosing cube.
    """
    axis = np.linspace(-BOX_HALF_WIDTH, BOX_HALF_WIDTH, sample_count_per_axis)
    grid_x, grid_y, grid_z = np.meshgrid(axis, axis, axis, indexing="ij")
    distance = np.sqrt(grid_x**2 + grid_y**2 + grid_z**2)
    polar = np.arccos(np.clip(grid_z / np.maximum(distance, 1.0e-300), -1.0, 1.0))
    azimuthal = np.mod(np.arctan2(grid_y, grid_x), 2.0 * math.pi)
    inside = distance <= radius_array(azimuthal, polar)
    cell_volume = (axis[1] - axis[0]) ** 3
    return float(inside.sum() * cell_volume)


def marked_points() -> dict[str, tuple[float, float, float]]:
    """Return the Cartesian coordinates of the two marked points of Figure 1.

    Returns:
        A mapping from ``"peak"`` and ``"valley"`` to the Cartesian coordinates of the point of
        the surface at the marked direction.
    """
    peak_radius = float(RADIUS_MAXIMUM)
    valley_radius = float(RADIUS_MINIMUM)
    peak = (
        peak_radius * math.sin(LOBE_PHI) * math.cos(LOBE_THETA),
        peak_radius * math.sin(LOBE_PHI) * math.sin(LOBE_THETA),
        peak_radius * math.cos(LOBE_PHI),
    )
    valley = (
        valley_radius * math.sin(VALLEY_PHI) * math.cos(VALLEY_THETA),
        valley_radius * math.sin(VALLEY_PHI) * math.sin(VALLEY_THETA),
        valley_radius * math.cos(VALLEY_PHI),
    )
    return {"peak": peak, "valley": valley}


def peak_directions() -> list[tuple[float, float]]:
    """Return every direction of the surface where the radius reaches its maximum.

    Returns:
        A list of ``(theta, phi)`` pairs inside the natural ranges of the two angles.
    """
    directions = []
    for theta_index in range(THETA_WAVE):
        theta = math.pi / (2 * THETA_WAVE) + theta_index * 2.0 * math.pi / THETA_WAVE
        for phi_index in range(PHI_WAVE):
            phi = math.pi / (2 * PHI_WAVE) + phi_index * 2.0 * math.pi / PHI_WAVE
            if phi <= math.pi:
                directions.append((theta, phi))
    return directions
