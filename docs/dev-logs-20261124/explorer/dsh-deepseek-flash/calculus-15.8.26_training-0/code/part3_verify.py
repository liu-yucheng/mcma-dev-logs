"""Check the radial integral of part 3, including the absolute value of the power.

Run with ``code/.venv/Scripts/python.exe code/part3_verify.py``.
"""

from __future__ import annotations

import math

import numpy as np

import solid_geometry as geometry

RADIUS = geometry.REFERENCE_RADIUS


def check_antiderivative() -> None:
    """Check the derivative of the antiderivative against the integrand."""
    step = 1.0e-6
    for radius_value in (0.2, 0.5, 0.85):
        antiderivative = lambda value: -(2.0 / 3.0) * (RADIUS**2 - value**2) ** 1.5
        slope = (antiderivative(radius_value + step) - antiderivative(radius_value - step)) / (
            2.0 * step
        )
        integrand = 2.0 * radius_value * math.sqrt(RADIUS**2 - radius_value**2)
        geometry.report_check(
            f"antiderivative_slope_at_r_{radius_value:.2f}",
            slope,
            integrand,
            1.0e-7,
            "central difference of -(2/3)(a^2 - r^2)^(3/2) against 2 r sqrt(a^2 - r^2)",
        )


def check_radial_integral() -> None:
    """Check the closed form of the radial integral against quadrature at eleven angles."""
    angles = np.linspace(-math.pi / 2.0 + 1.0e-3, math.pi / 2.0 - 1.0e-3, 11)
    worst = 0.0
    for angle_value in angles:
        closed = geometry.radial_integral_closed_form(float(angle_value), RADIUS)
        numeric_value = geometry.radial_integral_numeric(float(angle_value), RADIUS)
        worst = max(worst, abs(closed - numeric_value))
        geometry.report_check(
            f"radial_integral_theta_{angle_value:+.3f}",
            numeric_value,
            closed,
            1.0e-12,
            "adaptive quadrature of 2 r sqrt(a^2 - r^2) against (2/3) a^3 (1 - |sin|^3)",
        )
    print(f"FACT radial_integral_worst_error={worst:.3e}")


def check_absolute_value() -> None:
    """Show that the signed power breaks the symmetry of the geometry."""
    angle = -math.pi / 4.0
    signed_power = math.sin(angle) ** 3
    unsigned_power = abs(math.sin(angle)) ** 3
    geometry.report_check(
        "nonzero_signed_power_at_negative_angle",
        signed_power,
        -unsigned_power,
        1.0e-15,
        "sin(-pi/4)^3 against minus |sin(-pi/4)|^3",
    )
    numeric_left = geometry.radial_integral_numeric(angle, RADIUS)
    numeric_right = geometry.radial_integral_numeric(-angle, RADIUS)
    geometry.report_check(
        "radial_integral_symmetry",
        numeric_left,
        numeric_right,
        1.0e-13,
        "quadrature at -pi/4 against quadrature at +pi/4",
    )
    wrong_value = (2.0 / 3.0) * RADIUS**3 * (1.0 - signed_power)
    print(
        f"FACT radial_integral_at_minus_pi_over_4={numeric_left:.12f} "
        f"signed_power_value={wrong_value:.12f}"
    )
    geometry.report_falsification(
        "signed_power_control",
        wrong_value,
        numeric_left,
        0.1,
        "the formula with sin^3 in place of |sin|^3 against the quadrature value",
    )
    from scipy import integrate

    substituted, _ = integrate.quad(
        lambda value: math.sqrt(max(RADIUS**2 - value, 0.0)),
        0.0,
        (RADIUS * math.cos(angle)) ** 2,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
    )
    geometry.report_check(
        "substituted_radial_integral",
        substituted,
        numeric_left,
        1.0e-11,
        "the substitution u = r^2 against the direct quadrature at theta = -pi/4",
    )


def check_upper_bound() -> None:
    """Check that the radial upper bound stays inside the sphere."""
    angles = np.linspace(-math.pi / 2.0, math.pi / 2.0, 20001)
    upper = RADIUS * np.cos(angles)
    geometry.report_check(
        "upper_bound_maximum",
        float(np.max(upper)),
        RADIUS,
        1.0e-12,
        "maximum of a cos(theta) over the closed angle range against a",
    )
    geometry.report_check(
        "upper_bound_minimum",
        float(np.min(upper)),
        -0.0,
        0.0 + 1.0e-12,
        "minimum of a cos(theta) over the closed angle range against zero",
    )
    remainder = RADIUS**2 - upper**2
    geometry.report_check(
        "upper_bound_keeps_height_real",
        float(np.min(remainder)),
        0.0,
        1.0e-12,
        "minimum of a^2 - r_max^2 against zero",
    )
    print(f"FACT radial_integral_at_theta_zero={geometry.radial_integral_closed_form(0.0, RADIUS):.12f}")


def main() -> None:
    """Run every check of part 3 and print the summary."""
    check_antiderivative()
    check_radial_integral()
    check_absolute_value()
    check_upper_bound()
    geometry.summarize("part3")


if __name__ == "__main__":
    main()
