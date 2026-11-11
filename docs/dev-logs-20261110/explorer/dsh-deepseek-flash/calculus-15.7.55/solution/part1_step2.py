"""Compute the exact volume and the exact maximum with symbolic algebra.

The substitution u = x, v = sqrt(2)*y, w = sqrt(3)*z maps the ellipsoid onto the
unit ball. The Jacobian of the inverse map is 1/sqrt(6), so every integral over
the ellipsoid is 1/sqrt(6) times the corresponding integral over the unit ball.
"""

from sympy import Rational, integrate, pi, simplify, sin, sqrt, symbols

radius, polar_angle, azimuth = symbols("radius polar_angle azimuth", real=True)

# Volume of the unit ball in spherical coordinates, with the factor sin(polar_angle).
ball_volume = integrate(
    integrate(
        integrate(radius**2 * sin(polar_angle), (radius, 0, 1)),
        (polar_angle, 0, pi),
    ),
    (azimuth, 0, 2 * pi),
)
print(f"volume of the unit ball: {simplify(ball_volume)}")

jacobian = 1 / sqrt(6)
print(f"Jacobian factor of the substitution: {simplify(jacobian)}")

ellipsoid_volume = simplify(ball_volume * jacobian)
print(f"volume of the ellipsoid: {ellipsoid_volume} = {float(ellipsoid_volume.evalf(15)):.10f}")

# On the unit ball the integrand 1 - (u**2 + v**2 + w**2) is 1 - radius**2.
ball_moment = integrate(
    integrate(
        integrate(radius**4 * sin(polar_angle), (radius, 0, 1)),
        (polar_angle, 0, pi),
    ),
    (azimuth, 0, 2 * pi),
)
print(f"integral of radius^2 over the unit ball: {simplify(ball_moment)}")
ball_integral = simplify(ball_volume - ball_moment)
print(f"integral of 1 - radius^2 over the unit ball: {ball_integral}")

maximum_value = simplify(ball_integral * jacobian)
print(f"maximum value over the ellipsoid: {maximum_value} = {float(maximum_value.evalf(15)):.10f}")

average_value = simplify(maximum_value / ellipsoid_volume)
print(f"average value of the integrand over the ellipsoid: {average_value}")
print(f"decimal value: {float(average_value.evalf(15)):.12f}")

assert simplify(ball_volume) == 4 * pi / 3
assert simplify(ball_moment) == 4 * pi / 5
assert simplify(maximum_value) == 4 * pi * sqrt(6) / 45
assert average_value == Rational(2, 5)
print("the exact maximum is 4*pi*sqrt(6)/45 and the mean value of g on E is 2/5")
