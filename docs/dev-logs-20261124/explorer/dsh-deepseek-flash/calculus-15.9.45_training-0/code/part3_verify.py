"""Check Part 3: the azimuthal integral, the polar integral, and the general identity.

The two integrals of the volume are computed three times: once with the exact trigonometric
polynomial of :mod:`bumpy_sphere`, once with the product-to-sum identity of one single cosine
term, and once with adaptive quadrature.  The identity ``1 + 1/(4 n**2 - 1)`` is checked at the
three harmonics 3, 5, and 7, so a formula that holds only at ``n = 5`` fails a row.
"""

import math
import pathlib
import sys
from fractions import Fraction

import scipy.integrate

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import bumpy_sphere
from verification_report import CheckLog

CHECKED_HARMONICS = (3, 5, 7)
"""Harmonics of the polar integral that the identity must satisfy."""

AZIMUTHAL_HARMONICS = (1, 2, 3, 4, 5, 6, 7)
"""Harmonics of the azimuthal integral, whose exact value is always pi."""


def half_turn_sine_integral(frequency: int) -> Fraction:
    """Return the exact integral of ``sin(frequency * x)`` over ``[0, pi]``.

    Args:
        frequency: Positive integer frequency.
    """
    return Fraction(1 - (-1) ** frequency, frequency)


def weighted_mean_square(harmonic: int) -> Fraction:
    """Return the exact integral of ``sin(harmonic*x)**2 * sin(x)`` over ``[0, pi]``.

    The derivation uses one product-to-sum identity on the squared sine and the general integral
    of a sine over a half turn.  It never expands a cube, so it is an independent route.

    Args:
        harmonic: Positive integer frequency of the squared sine.
    """
    doubled = 2 * harmonic
    cosine_integral = Fraction(1, 2) * (
        half_turn_sine_integral(doubled + 1) - half_turn_sine_integral(doubled - 1)
    )
    return Fraction(1, 2) * half_turn_sine_integral(1) - Fraction(1, 2) * cosine_integral


def numeric_weighted_mean_square(harmonic: int) -> float:
    """Return the integral of ``sin(harmonic*x)**2 * sin(x)`` over ``[0, pi]`` by quadrature.

    Args:
        harmonic: Positive integer frequency of the squared sine.
    """
    value, _error = scipy.integrate.quad(
        lambda angle: math.sin(harmonic * angle) ** 2 * math.sin(angle),
        0.0, math.pi, epsabs=1.0e-13, epsrel=1.0e-12,
    )
    return float(value)


def numeric_azimuthal_integral(harmonic: int) -> float:
    """Return the integral of ``sin(harmonic*x)**2`` over ``[0, 2 pi]`` by quadrature.

    Args:
        harmonic: Positive integer frequency of the squared sine.
    """
    value, _error = scipy.integrate.quad(
        lambda angle: math.sin(harmonic * angle) ** 2,
        0.0, 2.0 * math.pi, epsabs=1.0e-13, epsrel=1.0e-12,
    )
    return float(value)


def main() -> None:
    """Run the checks of Part 3 and write the summary of the part."""
    log = CheckLog("part3")

    exact_polar = bumpy_sphere.phi_factor(bumpy_sphere.PHI_WAVE, 2)
    numeric_polar = numeric_weighted_mean_square(bumpy_sphere.PHI_WAVE)
    log.record("polar integral: exact polynomial against quadrature",
               numeric_polar, float(exact_polar), abs(numeric_polar - float(exact_polar)),
               abs(numeric_polar - float(exact_polar)) < 1.0e-12)

    identity_polar = weighted_mean_square(bumpy_sphere.PHI_WAVE)
    log.record("polar integral: polynomial against the product-to-sum identity",
               str(exact_polar), str(identity_polar), str(exact_polar - identity_polar),
               exact_polar == identity_polar)

    exact_azimuthal = bumpy_sphere.theta_factor(bumpy_sphere.THETA_WAVE, 2)
    numeric_azimuthal = numeric_azimuthal_integral(bumpy_sphere.THETA_WAVE)
    log.record("azimuthal integral: pi times the exact factor against quadrature",
               numeric_azimuthal, float(exact_azimuthal) * math.pi,
               abs(numeric_azimuthal - float(exact_azimuthal) * math.pi),
               abs(numeric_azimuthal - float(exact_azimuthal) * math.pi) < 1.0e-12)

    for harmonic in CHECKED_HARMONICS:
        exact_value = bumpy_sphere.phi_factor(harmonic, 2)
        identity_value = weighted_mean_square(harmonic)
        closed_value = 1 + Fraction(1, 4 * harmonic**2 - 1)
        log.record(f"polar integral at harmonic {harmonic}: identity against 1 + 1/(4n^2-1)",
                   str(identity_value), str(closed_value),
                   str(identity_value - closed_value),
                   identity_value == closed_value and identity_value == exact_value)

    worst_azimuthal = 0.0
    for harmonic in AZIMUTHAL_HARMONICS:
        exact_value = bumpy_sphere.theta_factor(harmonic, 2)
        numeric_value = numeric_azimuthal_integral(harmonic) / math.pi
        worst_azimuthal = max(worst_azimuthal, abs(numeric_value - float(exact_value)))
    log.record("azimuthal factor over harmonics 1 to 7: largest departure from 1",
               worst_azimuthal, 0.0, worst_azimuthal, worst_azimuthal < 1.0e-12)

    exact_ball = Fraction(4, 3)
    exact_share = bumpy_sphere.exact_volume_over_pi() / exact_ball - 1
    numeric_volume = bumpy_sphere.numeric_volume_quadrature()
    numeric_share = numeric_volume / (float(exact_ball) * math.pi) - 1.0
    log.record("relative increase of the volume: exact against quadrature",
               numeric_share, float(exact_share), abs(numeric_share - float(exact_share)),
               abs(numeric_share - float(exact_share)) < 1.0e-11)

    log.require_all_passed()
    log.write()

    print(f"polar integral exact {exact_polar} = {float(exact_polar):.12g}, "
          f"quadrature {numeric_polar:.12g}", flush=True)
    print(f"azimuthal integral exact pi = {math.pi:.12g}, "
          f"quadrature {numeric_azimuthal:.12g}", flush=True)
    print("identity values: " + ", ".join(
        f"n={harmonic}: {weighted_mean_square(harmonic)} = "
        f"{float(weighted_mean_square(harmonic)):.12g}" for harmonic in CHECKED_HARMONICS
    ), flush=True)
    print(f"relative increase exact {exact_share} = {float(exact_share):.12g}, "
          f"quadrature {numeric_share:.12g}", flush=True)


if __name__ == "__main__":
    main()
