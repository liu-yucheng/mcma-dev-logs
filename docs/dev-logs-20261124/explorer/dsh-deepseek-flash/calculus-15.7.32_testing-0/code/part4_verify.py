"""Verification of Part 4, the orders with x innermost.

This script checks the projection that drops x, the two orders dx dy dz and dx dz dy, and
one wrong reading of the middle bound.

Run: code/.venv/Scripts/python.exe code/part4_verify.py
"""

import os
import sys

import sympy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import orders
import set_compare
import solid
from verify_common import as_text, check, record

INTEGER_VERTICES = [(2, 2, 0), (2, 2, 1), (2, 0, 0), (0, 2, 0)]
GAUSS_POINTS = 12


def main():
    """Check the two orders with x innermost and write the record of Part 4."""
    checks = []
    values = {}

    volume_reference = float(solid.determinant_volume(INTEGER_VERTICES))
    projection_area = float(solid.shoelace_area([(0, 0), (2, 0), (2, 1)]))
    y_symbol = sympy.Symbol("y")
    strip_integral = float(sympy.integrate(y_symbol / 2, (y_symbol, 0, 2)))
    checks.append(
        check(
            "projection on the plane x = 0: length of the z strips against the corner list",
            strip_integral,
            projection_area,
            1e-12,
        )
    )
    values["projection_area"] = as_text(projection_area)
    values["volume_reference"] = as_text(volume_reference)

    for order_name in ("dx dy dz", "dx dz dy"):
        agree, total = set_compare.agreement(order_name)
        checks.append(check("the limits of %s describe the same points as E" % order_name, agree, total))
        exact_value = float(orders.symbolic_value(order_name, sympy.Integer(1)))
        numeric_value = orders.nested_gauss_value(order_name, lambda env: 1.0, GAUSS_POINTS)
        checks.append(
            check(
                "%s: exact value against the volume by determinant" % order_name,
                exact_value,
                volume_reference,
                1e-12,
            )
        )
        checks.append(
            check(
                "%s: nested quadrature against the exact value" % order_name,
                numeric_value,
                exact_value,
                1e-12,
            )
        )
        key = order_name.replace(" ", "")
        values["value_%s" % key] = as_text(numeric_value)
        values["latex_%s" % key] = orders.ORDERS[order_name]["latex"]

    z_symbol = sympy.Symbol("z")
    wrong_middle_bound = float(
        sympy.integrate(
            y_symbol - 2 * z_symbol,
            (z_symbol, 0, 1),
            (y_symbol, 0, 2),
        )
    )
    values["wrong_middle_bound"] = as_text(wrong_middle_bound)
    checks.append(
        check(
            "middle bound z from 0 to 1 instead of 0 to y/2: its signed integral differs from the volume",
            wrong_middle_bound,
            volume_reference,
            comparison="differ",
        )
    )

    values["gauss_points"] = GAUSS_POINTS
    values["random_count"] = set_compare.RANDOM_COUNT
    record(4, values, checks)


if __name__ == "__main__":
    main()
