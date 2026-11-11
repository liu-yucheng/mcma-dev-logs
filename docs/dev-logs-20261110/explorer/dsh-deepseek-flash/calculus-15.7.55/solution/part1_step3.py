"""Test that the ellipsoid really maximizes the integral.

The script studies the family of similar ellipsoids x**2 + 2*y**2 + 3*z**2 <= s**2,
confirms that the integral grows up to s = 1 and decreases after it, integrates
the exact maximum with mpmath quadrature, and shows by Monte Carlo sampling that
any shift of the ellipsoid lowers the value.
"""

import mpmath
import numpy as np
from sympy import Rational, diff, integrate, pi, simplify, sin, solve, sqrt, symbols

mpmath.mp.dps = 25

scale = symbols("s", positive=True)
radius, polar_angle, azimuth = symbols("radius polar_angle azimuth", real=True)

# Integral of 1 - s**2 * radius**2 over the unit ball, then scaled by s**3 / sqrt(6).
ball_shape = integrate(
    integrate(
        integrate(radius**2 * sin(polar_angle), (radius, 0, 1)),
        (polar_angle, 0, pi),
    ),
    (azimuth, 0, 2 * pi),
)
scaled_integral = simplify(scale**3 / sqrt(6) * (ball_shape - scale**2 * ball_shape * Rational(3, 5)))
print(f"volume of the unit ball: {simplify(ball_shape)}")
print(f"I(s) = {scaled_integral}")

derivative = simplify(diff(scaled_integral, scale))
print(f"I'(s) = {derivative}")
print(f"critical points in (0, infinity): {solve(diff(scaled_integral, scale), scale)}")

second_derivative_at_one = simplify(diff(scaled_integral, scale, 2).subs(scale, 1))
print(f"I''(1) = {second_derivative_at_one}")

print()
print("  s      I(s)")
for index in range(9):
    s_value = Rational(2, 5) + Rational(index, 5)
    print(f"{float(s_value):4.1f}   {float(scaled_integral.subs(scale, s_value).evalf(12)):.9f}")

print()
print(f"I(1) = {simplify(scaled_integral.subs(scale, 1))}")
print(f"I(1) as a decimal: {float(simplify(scaled_integral.subs(scale, 1)).evalf(15)):.10f}")

# Independent quadrature of the maximum in scaled spherical coordinates.
integrand_ball = lambda r_value, phi_value, theta_value: (1 - r_value**2) * r_value**2 * mpmath.sin(phi_value)
quadrature_value = mpmath.quad(
    integrand_ball,
    [0, 1],
    [0, mpmath.pi],
    [0, 2 * mpmath.pi],
) / mpmath.sqrt(6)
closed_form = 4 * mpmath.pi * mpmath.sqrt(6) / 45
print()
print(f"mpmath quadrature of the maximum: {mpmath.nstr(quadrature_value, 20)}")
print(f"closed form 4*pi*sqrt(6)/45:       {mpmath.nstr(closed_form, 20)}")
print(f"difference: {mpmath.nstr(abs(quadrature_value - closed_form), 5)}")

# Monte Carlo check that a shifted copy of the ellipsoid gives a smaller integral.
random_generator = np.random.default_rng(55)
sample_count = 1_500_000
radius_random = np.cbrt(random_generator.uniform(0.0, 1.0, sample_count))
cos_polar = random_generator.uniform(-1.0, 1.0, sample_count)
azimuth_random = random_generator.uniform(0.0, 2.0 * np.pi, sample_count)
sin_polar = np.sqrt(1.0 - cos_polar**2)
point_x = radius_random * sin_polar * np.cos(azimuth_random)
point_y = radius_random * sin_polar * np.sin(azimuth_random) / np.sqrt(2.0)
point_z = radius_random * cos_polar / np.sqrt(3.0)

ellipsoid_volume = 4.0 * np.pi / (3.0 * np.sqrt(6.0))
print()
print("shift of the centre along the x-axis   Monte Carlo integral")
for shift in (0.0, 0.1, 0.2, 0.3, 0.4):
    shifted_values = 1.0 - (point_x + shift)**2 - 2.0 * point_y**2 - 3.0 * point_z**2
    estimate = ellipsoid_volume * float(np.mean(shifted_values))
    standard_error = ellipsoid_volume * float(np.std(shifted_values)) / np.sqrt(sample_count)
    print(f"  {shift:4.1f}                                  {estimate:.5f} +/- {standard_error:.5f}")
