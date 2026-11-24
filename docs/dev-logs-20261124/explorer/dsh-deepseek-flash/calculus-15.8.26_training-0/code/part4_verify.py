"""Check the angle integral and the final closed form of part 4.

Run with ``code/.venv/Scripts/python.exe code/part4_verify.py``.
"""

from __future__ import annotations

import math

from scipy import integrate

import solid_geometry as geometry

RADIUS = geometry.REFERENCE_RADIUS


def angle_antiderivative(angle: float) -> float:
    """Return the antiderivative theta + cos(theta) - cos(theta)^3 / 3 of 1 - sin^3.

    Args:
        angle: Angle in radians, inside the first quadrant.

    Returns:
        The value of the antiderivative.
    """
    return angle + math.cos(angle) - math.cos(angle) ** 3 / 3.0


def check_angle_integral() -> None:
    """Check the closed form pi - 4/3 against adaptive quadrature."""
    numeric_value, _ = integrate.quad(
        lambda angle: 1.0 - abs(math.sin(angle)) ** 3,
        -math.pi / 2.0,
        math.pi / 2.0,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
    )
    geometry.report_check(
        "angle_integral_matches_quadrature",
        numeric_value,
        geometry.theta_integral_closed_form(),
        1.0e-12,
        "adaptive quadrature of 1 - |sin|^3 against pi - 4/3",
    )
    print(
        f"FACT angle_integral_value={numeric_value:.12f} "
        f"pi_minus_four_thirds={geometry.theta_integral_closed_form():.12f}"
    )


def sin_cubed_antiderivative(angle: float) -> float:
    """Return the antiderivative -cos(theta) + cos(theta)^3 / 3 of sin(theta)^3.

    Args:
        angle: Angle in radians.

    Returns:
        The value of the antiderivative.
    """
    return -math.cos(angle) + math.cos(angle) ** 3 / 3.0


def check_sin_cubed() -> None:
    """Check the integral of sin^3 on the first quadrant against its antiderivative."""
    numeric_value, _ = integrate.quad(
        lambda angle: math.sin(angle) ** 3,
        0.0,
        math.pi / 2.0,
        epsabs=1.0e-14,
        epsrel=1.0e-14,
    )
    antiderivative_value = sin_cubed_antiderivative(math.pi / 2.0) - sin_cubed_antiderivative(0.0)
    geometry.report_check(
        "sin_cubed_matches_quadrature",
        numeric_value,
        antiderivative_value,
        1.0e-13,
        "adaptive quadrature of sin^3 against the difference of -cos + cos^3/3",
    )
    geometry.report_check(
        "sin_cubed_matches_two_thirds",
        antiderivative_value,
        2.0 / 3.0,
        1.0e-13,
        "the antiderivative difference against the exact fraction two thirds",
    )
    print(f"FACT sin_cubed_value={numeric_value:.12f}")


def check_antiderivative_slope() -> None:
    """Check the derivative of the angle antiderivative against the integrand."""
    step = 1.0e-6
    for angle_value in (0.1, 0.5, 0.9, 1.3):
        slope = (angle_antiderivative(angle_value + step) - angle_antiderivative(angle_value - step)) / (
            2.0 * step
        )
        geometry.report_check(
            f"angle_antiderivative_slope_at_{angle_value:.1f}",
            slope,
            1.0 - math.sin(angle_value) ** 3,
            1.0e-7,
            "central difference of the antiderivative against 1 - sin^3",
        )


def check_symmetry() -> None:
    """Check that the half interval doubles to the full interval."""
    half_value, _ = integrate.quad(
        lambda angle: 1.0 - math.sin(angle) ** 3,
        0.0,
        math.pi / 2.0,
        epsabs=1.0e-14,
        epsrel=1.0e-14,
    )
    full_value, _ = integrate.quad(
        lambda angle: 1.0 - abs(math.sin(angle)) ** 3,
        -math.pi / 2.0,
        math.pi / 2.0,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
    )
    geometry.report_check(
        "symmetry_doubles_half_interval",
        2.0 * half_value,
        full_value,
        1.0e-13,
        "twice the quadrature on [0, pi/2] against the quadrature on [-pi/2, pi/2]",
    )


def check_closed_forms() -> None:
    """Check the two algebraic forms of the volume and the fraction of the sphere."""
    for radius_value in (1.0, 2.0, 3.0):
        geometry.report_check(
            f"two_forms_at_a_{radius_value:.0f}",
            geometry.exact_volume(radius_value),
            geometry.exact_volume_factored(radius_value),
            1.0e-12,
            "(2/3) pi a^3 - (8/9) a^3 against a^3 (6 pi - 8)/9",
        )
    numeric_value = geometry.volume_by_triple_quadrature(1.0)
    geometry.report_check(
        "closed_form_matches_triple_integral_a_1",
        numeric_value,
        geometry.exact_volume(1.0),
        1.0e-8,
        "adaptive triple quadrature against the closed form at a = 1",
    )
    numeric_two = geometry.volume_by_triple_quadrature(2.0)
    geometry.report_check(
        "closed_form_matches_triple_integral_a_2",
        numeric_two,
        geometry.exact_volume(2.0),
        2.0e-8,
        "adaptive triple quadrature against the closed form at a = 2",
    )
    fraction = geometry.exact_volume(1.0) / (4.0 * math.pi / 3.0)
    geometry.report_check(
        "fraction_of_sphere",
        fraction,
        (6.0 * math.pi - 8.0) / (12.0 * math.pi),
        1.0e-12,
        "V divided by the sphere volume against (6 pi - 8)/(12 pi)",
    )
    print(f"FACT volume_at_a_1={geometry.exact_volume(1.0):.12f}")
    print(f"FACT volume_at_a_2={geometry.exact_volume(2.0):.12f}")
    print(
        f"FACT volume_two_thirds_pi={2.0 * math.pi / 3.0:.12f} "
        f"volume_eight_ninths={8.0 / 9.0:.12f}"
    )
    print(f"FACT fraction_of_sphere={fraction:.12f}")


def check_positive() -> None:
    """Check that the solid and its complement fill the ball, and that both are positive."""
    sphere = 4.0 * math.pi / 3.0

    def inside_shell(angle: float) -> float:
        """Return the full height of the ball for the first angle range."""
        return integrate.quad(
            lambda radius_value: 2.0 * radius_value
            * math.sqrt(max(1.0 - radius_value**2, 0.0)),
            0.0,
            1.0,
            epsabs=1.0e-12,
            epsrel=1.0e-12,
        )[0]

    def outside_shell(angle: float) -> float:
        """Return the height of the ball outside the cylinder for one angle."""
        return integrate.quad(
            lambda radius_value: 2.0 * radius_value
            * math.sqrt(max(1.0 - radius_value**2, 0.0)),
            math.cos(angle),
            1.0,
            epsabs=1.0e-12,
            epsrel=1.0e-12,
        )[0]

    complement_side, _ = integrate.quad(
        outside_shell, -math.pi / 2.0, math.pi / 2.0, epsabs=1.0e-11, epsrel=1.0e-11
    )
    far_side, _ = integrate.quad(
        inside_shell, math.pi / 2.0, 3.0 * math.pi / 2.0, epsabs=1.0e-11, epsrel=1.0e-11
    )
    complement = complement_side + far_side
    geometry.report_check(
        "solid_plus_complement_is_ball",
        geometry.exact_volume(1.0) + complement,
        sphere,
        1.0e-9,
        "the solid plus the complement by quadrature against 4 pi / 3",
    )
    assert geometry.exact_volume(1.0) > 0.0, "the volume must be positive"
    print(f"FACT gap_to_sphere={complement:.12f}")


def main() -> None:
    """Run every check of part 4 and print the summary."""
    check_angle_integral()
    check_sin_cubed()
    check_antiderivative_slope()
    check_symmetry()
    check_closed_forms()
    check_positive()
    geometry.summarize("part4")


if __name__ == "__main__":
    main()
