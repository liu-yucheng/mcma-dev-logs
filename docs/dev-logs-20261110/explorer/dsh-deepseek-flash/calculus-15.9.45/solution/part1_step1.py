"""Find the volume inside the bumpy sphere rho = 1 + sin(m theta) sin(n phi)/5.

The script expands rho cubed, integrates every term over the sphere of
directions, and prints which terms vanish and which survive.
"""

from sympy import Rational, Symbol, cos, integrate, pi, simplify, sin


def main():
    """Integrate rho cubed over the unit sphere of directions."""
    theta = Symbol("theta", positive=True)
    phi = Symbol("phi", positive=True)
    amplitude = Rational(1, 5)
    m, n = 6, 5

    bump = amplitude * sin(m * theta) * sin(n * phi)
    rho = 1 + bump

    print("surface: rho = 1 + sin(6 theta) sin(5 phi) / 5")
    print("volume = (1/3) integral rho^3 sin(phi) dphi dtheta over 0 <= theta <= 2 pi,")
    print("         0 <= phi <= pi")
    print()

    expansion = rho**3
    print(f"rho^3 = {expansion}")

    linear_theta = integrate(sin(m * theta), (theta, 0, 2 * pi))
    linear_phi = integrate(sin(n * phi) * sin(phi), (phi, 0, pi))
    print()
    print(f"integral of sin(6 theta) over one period: {linear_theta}")
    print(f"integral of sin(5 phi) sin(phi): {simplify(linear_phi)}")
    print("so the term linear in the bump contributes nothing")

    cubic_theta = integrate(sin(m * theta) ** 3, (theta, 0, 2 * pi))
    cubic_phi = integrate(sin(n * phi) ** 3 * sin(phi), (phi, 0, pi))
    print(f"integral of sin^3(6 theta): {cubic_theta}")
    print(f"integral of sin^3(5 phi) sin(phi): {simplify(cubic_phi)}")
    print("so the cubic term contributes nothing either")

    squared_theta = integrate(sin(m * theta) ** 2, (theta, 0, 2 * pi))
    squared_phi = integrate(sin(n * phi) ** 2 * sin(phi), (phi, 0, pi))
    print()
    print(f"integral of sin^2(6 theta): {simplify(squared_theta)}")
    print(f"integral of sin^2(5 phi) sin(phi): {simplify(squared_phi)}")
    print("the square term does not vanish, because sin^2 has period pi")

    constant = integrate(integrate(sin(phi), (phi, 0, pi)), (theta, 0, 2 * pi))
    square_term = 3 * amplitude**2 * squared_theta * squared_phi
    print()
    print(f"constant term: {constant}")
    print(f"square term: 3 * (1/25) * {simplify(squared_theta)} * {simplify(squared_phi)}"
          f" = {simplify(square_term)}")

    total = simplify(constant + square_term)
    volume = simplify(total / 3)
    print(f"triple integral before the factor 1/3: {total}")
    print(f"volume: {volume}")
    print(f"volume as a multiple of pi: {simplify(volume / pi)} pi")
    print(f"numeric value: {float(volume):.6f}")

    sphere = Rational(4, 3) * pi
    print(f"sphere of radius 1: {sphere} = {float(sphere):.6f}")
    print(f"ratio to the sphere: {simplify(volume / sphere)} = {float(volume / sphere):.6f}")
    print(f"mean of rho^3 over the directions: {simplify(3 * volume / (4 * pi))}")

    wrong = integrate(integrate(rho**3 * sin(phi), (phi, 0, pi)), (theta, 0, 2 * pi)) / 3
    print(f"direct sympy integration agrees: {simplify(wrong - volume)}")


if __name__ == "__main__":
    main()
