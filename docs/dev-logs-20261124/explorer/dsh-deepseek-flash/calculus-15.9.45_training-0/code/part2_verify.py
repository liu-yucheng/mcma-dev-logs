"""Check Part 2: the expansion of the cube, and the vanishing of the odd terms.

Each term of the expanded cube is integrated twice: once with exact rational algebra through
:class:`bumpy_sphere.TrigPolynomial`, and once with an adaptive quadrature over the two angles.
The check of a vanishing term compares the exact zero with the quadrature value, so a term that
does not vanish makes a row fail.
"""

import math
import pathlib
import sys
from fractions import Fraction

import scipy.integrate

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import bumpy_sphere
from verification_report import CheckLog

QUADRATURE_EPSILON = 1.0e-13
"""Requested absolute and relative accuracy of every quadrature below."""


def exact_term_volume(power: int) -> bumpy_sphere.PiValue:
    """Return the exact volume contribution of one power of the bump term.

    Args:
        power: Power of ``sin(6 theta) sin(5 varphi)``.

    Returns:
        The exact volume of the term, with its binomial coefficient and its amplitude.
    """
    return bumpy_sphere.exact_volume_of_term(power, power)


def numeric_term_volume(power: int) -> float:
    """Return the volume contribution of one power of the bump term by quadrature.

    Args:
        power: Power of ``sin(6 theta) sin(5 varphi)``.
    """
    coefficient = math.comb(3, power) * float(bumpy_sphere.AMPLITUDE) ** power

    def integrand(phi: float, theta: float) -> float:
        """Return the integrand of one term at one pair of angles."""
        return (
            coefficient
            * math.sin(bumpy_sphere.THETA_WAVE * theta) ** power
            * math.sin(bumpy_sphere.PHI_WAVE * phi) ** power
            * math.sin(phi) / 3.0
        )

    value, _error = scipy.integrate.dblquad(
        integrand, 0.0, 2.0 * math.pi, lambda _theta: 0.0, lambda _theta: math.pi,
        epsabs=QUADRATURE_EPSILON, epsrel=QUADRATURE_EPSILON,
    )
    return float(value)


def main() -> None:
    """Run the checks of Part 2 and write the summary of the part."""
    log = CheckLog("part2")

    exact_constant = exact_term_volume(0)
    numeric_constant = numeric_term_volume(0)
    log.record("constant term of the cube: exact against quadrature",
               numeric_constant, exact_constant.as_float(),
               abs(numeric_constant - exact_constant.as_float()),
               abs(numeric_constant - exact_constant.as_float()) < 1.0e-11)

    exact_linear = exact_term_volume(1)
    numeric_linear = numeric_term_volume(1)
    log.record("linear term of the cube: exact against quadrature",
               numeric_linear, exact_linear.as_float(),
               abs(numeric_linear - exact_linear.as_float()),
               abs(exact_linear.as_float()) == 0.0
               and abs(numeric_linear - exact_linear.as_float()) < 1.0e-12)

    exact_cubic = exact_term_volume(3)
    numeric_cubic = numeric_term_volume(3)
    log.record("cubic term of the cube: exact against quadrature",
               numeric_cubic, exact_cubic.as_float(),
               abs(numeric_cubic - exact_cubic.as_float()),
               abs(exact_cubic.as_float()) == 0.0
               and abs(numeric_cubic - exact_cubic.as_float()) < 1.0e-12)

    exact_quadratic = exact_term_volume(2)
    numeric_quadratic = numeric_term_volume(2)
    log.record("quadratic term of the cube: exact against quadrature",
               numeric_quadratic, exact_quadratic.as_float(),
               abs(numeric_quadratic - exact_quadratic.as_float()),
               abs(numeric_quadratic - exact_quadratic.as_float()) < 1.0e-11)

    exact_total = bumpy_sphere.exact_volume().as_float()
    numeric_total = sum(numeric_term_volume(power) for power in range(4))
    log.record("sum of the four quadrature terms against the exact volume",
               numeric_total, exact_total, abs(numeric_total - exact_total),
               abs(numeric_total - exact_total) < 1.0e-10)

    exact_share = exact_quadratic.pi_multiple / exact_constant.pi_multiple
    numeric_share = numeric_quadratic / numeric_constant
    log.record("share of the quadratic term: exact against quadrature",
               numeric_share, float(exact_share), abs(numeric_share - float(exact_share)),
               abs(numeric_share - float(exact_share)) < 1.0e-10)

    log.require_all_passed()
    log.write()

    print(f"exact terms: constant {exact_constant.as_float():.12g}, "
          f"linear {exact_linear.as_float():.12g}, "
          f"quadratic {exact_quadratic.as_float():.12g}, "
          f"cubic {exact_cubic.as_float():.12g}", flush=True)
    print(f"quadrature terms: constant {numeric_constant:.12g}, "
          f"linear {numeric_linear:.6e}, quadratic {numeric_quadratic:.12g}, "
          f"cubic {numeric_cubic:.6e}", flush=True)
    print(f"exact quadratic term as a fraction of pi: {exact_quadratic.pi_multiple}", flush=True)
    print(f"exact share of the quadratic term: {exact_share} = {float(exact_share):.12g}",
          flush=True)
    print(f"exact total from the four terms: {exact_total:.12g}", flush=True)


if __name__ == "__main__":
    main()
