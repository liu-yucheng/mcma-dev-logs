"""Check Part 4: the volume of the bumpy sphere by four routes that share no code.

The exact route integrates an exact trigonometric polynomial.  The other routes are an adaptive
quadrature of the two angles, a midpoint sum over a grid of angles, a uniform sample of the
enclosing cube, and a count of the points of a Cartesian grid.  Each row pairs the exact value
with one numeric value, so a row fails when either route is wrong.
"""

import math
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import bumpy_sphere
from verification_report import CheckLog

GRID_CELL_COUNT = 2000
"""Number of cells along each angle of the midpoint sum."""

SAMPLE_COUNT = 8_000_000
"""Number of random points of the sampling estimator."""

SAMPLE_SEED = 20261123
"""Seed of the random number generator of the sampling estimator."""

BOX_GRID_COUNT = 261
"""Number of grid points along each axis of the enclosing cube."""

STANDARD_ERROR_MULTIPLIER = 3.0
"""Number of standard errors that a sampling estimate must stay inside."""


def main() -> None:
    """Run the checks of Part 4 and write the summary of the part."""
    log = CheckLog("part4")

    exact_volume = bumpy_sphere.exact_volume().as_float()
    exact_over_pi = bumpy_sphere.exact_volume_over_pi()

    quadrature = bumpy_sphere.numeric_volume_quadrature()
    log.record("volume: exact polynomial against adaptive quadrature", quadrature, exact_volume,
               abs(quadrature - exact_volume),
               abs(quadrature - exact_volume) / exact_volume < 1.0e-11)

    midpoint = bumpy_sphere.numeric_volume_grid(GRID_CELL_COUNT)
    log.record(f"volume: exact against a midpoint sum of {GRID_CELL_COUNT} cells per angle",
               midpoint, exact_volume, abs(midpoint - exact_volume),
               abs(midpoint - exact_volume) / exact_volume < 1.0e-6)

    sample, error = bumpy_sphere.numeric_volume_monte_carlo(SAMPLE_COUNT, SAMPLE_SEED)
    distance = abs(sample - exact_volume) / error
    log.record(f"volume: exact against {SAMPLE_COUNT} random points, in standard errors",
               distance, STANDARD_ERROR_MULTIPLIER, distance,
               distance < STANDARD_ERROR_MULTIPLIER)

    box_count = bumpy_sphere.numeric_volume_box_count(BOX_GRID_COUNT)
    log.record(f"volume: exact against a Cartesian grid of {BOX_GRID_COUNT} points per axis",
               box_count, exact_volume, abs(box_count - exact_volume),
               abs(box_count - exact_volume) / exact_volume < 5.0e-3)

    ball_over_pi = Fraction(4, 3)
    factored = ball_over_pi * Fraction(34, 33)
    log.record("volume over pi: expansion against (4/3)(34/33)",
               str(exact_over_pi), str(factored), str(exact_over_pi - factored),
               exact_over_pi == factored)

    closed_form = bumpy_sphere.closed_form_volume_over_pi()
    log.record("volume over pi: full expansion against the single surviving correction",
               str(closed_form), str(exact_over_pi), str(closed_form - exact_over_pi),
               closed_form == exact_over_pi)

    ratio = exact_volume / (float(ball_over_pi) * math.pi)
    log.record("ratio to the unit ball: exact against the quotient of the volumes",
               ratio, float(Fraction(34, 33)), abs(ratio - float(Fraction(34, 33))),
               abs(ratio - float(Fraction(34, 33))) < 1.0e-13)

    log.require_all_passed()
    log.write()

    print(f"exact volume {exact_volume:.12g} = {exact_over_pi} * pi", flush=True)
    print(f"quadrature {quadrature:.12g}, midpoint {midpoint:.12g}, "
          f"random {sample:.12g} with standard error {error:.6g}, "
          f"box count {box_count:.12g}", flush=True)
    print(f"unit ball {float(ball_over_pi) * math.pi:.12g}, "
          f"excess {exact_volume - float(ball_over_pi) * math.pi:.12g}", flush=True)
    print(f"exact volume to twelve significant digits: {exact_volume:.12g}", flush=True)


if __name__ == "__main__":
    main()
