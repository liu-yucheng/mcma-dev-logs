"""Part 3: evaluate the iterated integral exactly and check every antiderivative.

The inner integral gives y, so the slice area is y^2 / 2 at y = sqrt(1 - z^2), which is
(1 - z^2) / 2.  The outer integral gives 1 / 3.  The checks do three things.  They compare the
exact fraction with adaptive quadrature.  They compare each antiderivative with a central
difference of the function that it integrates.  They compare the exact value with a value that
the substitution z = sin(t) produces, which is a different computation.
"""

from __future__ import annotations

import math
from fractions import Fraction

import mcma_support as support

STEP = 1.0e-6
"""Step of the central difference of an antiderivative."""

POINTS = [0.1, 0.4, 0.7, 0.95]
"""Points at which the central difference checks the antiderivative of the slice area."""


def inner_antiderivative(y: float) -> float:
    """Return the antiderivative y^2 / 2 of the inner integral of the function y."""
    return y * y / 2.0


def outer_antiderivative(z: float) -> float:
    """Return the antiderivative z / 2 - z^3 / 6 of the slice area (1 - z^2) / 2."""
    return z / 2.0 - z ** 3 / 6.0


def central_difference(function, point: float, step: float) -> float:
    """Return the central difference of one function at one point."""
    return (function(point + step) - function(point - step)) / (2.0 * step)


def main() -> None:
    """Run the checks of Part 3 and write its record."""
    recorder = support.Recorder(3)

    for z in POINTS:
        recorder.record(f"antiderivative at z = {z:.2f}: derivative against the slice area",
                        central_difference(outer_antiderivative, z, STEP),
                        support.slice_area_exact(z), tolerance=1.0e-6)

    for y in POINTS:
        recorder.record(f"inner antiderivative at y = {y:.2f}: derivative against y",
                        central_difference(inner_antiderivative, y, STEP), y,
                        tolerance=1.0e-6)

    exact = Fraction(1, 2) - Fraction(1, 6)
    recorder.record_text("exact outer integral as a fraction", str(exact), "1/3")
    recorder.record("exact fraction against quadrature of the slice area",
                    float(exact), support.integrate(support.slice_area_exact, 0.0, 1.0),
                    tolerance=1.0e-12)

    substituted, _ = support.integrate(lambda t: support.slice_area_exact(math.sin(t))
                                       * math.cos(t), 0.0, math.pi / 2.0), None
    recorder.record("substitution z = sin(t) against one third", substituted, 1.0 / 3.0)
    recorder.publish("p3_exact_fraction", str(exact))
    recorder.publish("p3_exact_decimal", f"{float(exact):.12f}")
    recorder.publish("p3_substituted", f"{substituted:.12f}")
    recorder.publish("p3_quadrature", f"{support.integrate(support.slice_area_exact, 0.0, 1.0):.12f}")
    recorder.publish("p3_point_count", str(len(POINTS)))
    recorder.write()


if __name__ == "__main__":
    main()
