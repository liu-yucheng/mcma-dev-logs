"""Verification of Part 2, the orders with z innermost.

This script checks the projection on the plane z = 0, the two orders dz dx dy and dz dy dx,
and one wrong reading of each projection bound.

Run: code/.venv/Scripts/python.exe code/part2_verify.py
"""

import os
import sys

import numpy as np
import sympy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import orders
import set_compare
import solid
from verify_common import as_text, check, record

INTEGER_VERTICES = [(2, 2, 0), (2, 2, 1), (2, 0, 0), (0, 2, 0)]
GAUSS_POINTS = 12


def main():
    """Check the two orders with z innermost and write the record of Part 2."""
    checks = []
    values = {}

    volume_reference = float(solid.determinant_volume(INTEGER_VERTICES))
    values["volume_reference"] = as_text(volume_reference)

    projection_area = float(solid.shoelace_area([(2, 0), (0, 2), (2, 2)]))
    strip_integral = float(sympy.integrate(2 - (2 - sympy.Symbol("y")), (sympy.Symbol("y"), 0, 2)))
    checks.append(
        check(
            "projection on z = 0: length of the vertical strips against the corner list",
            strip_integral,
            projection_area,
            1e-12,
        )
    )
    values["projection_area"] = as_text(projection_area)

    for order_name in ("dz dx dy", "dz dy dx"):
        agree, total = set_compare.agreement(order_name)
        checks.append(
            check("the limits of %s describe the same points as E" % order_name, agree, total)
        )
        exact_value = orders.symbolic_value(order_name, sympy.Integer(1))
        exact_float = float(exact_value)
        numeric_value = orders.nested_gauss_value(order_name, lambda env: 1.0, GAUSS_POINTS)
        checks.append(
            check(
                "%s: exact value against the volume by determinant" % order_name,
                exact_float,
                volume_reference,
                1e-12,
            )
        )
        checks.append(
            check(
                "%s: nested quadrature against the exact value" % order_name,
                numeric_value,
                exact_float,
                1e-12,
            )
        )
        key = order_name.replace(" ", "")
        values["value_%s" % key] = as_text(numeric_value)
        values["latex_%s" % key] = orders.ORDERS[order_name]["latex"]

    wrong_full_square = float(
        sympy.integrate(
            (sympy.Symbol("x") + sympy.Symbol("y") - 2) / 2,
            (sympy.Symbol("x"), 0, 2),
            (sympy.Symbol("y"), 0, 2),
        )
    )
    values["wrong_full_square"] = as_text(wrong_full_square)
    checks.append(
        check(
            "full square [0, 2] x [0, 2] as the projection: its signed integral differs from the volume",
            wrong_full_square,
            volume_reference,
            comparison="differ",
        )
    )

    values["gauss_points"] = GAUSS_POINTS
    values["random_count"] = set_compare.RANDOM_COUNT
    record(2, values, checks)


if __name__ == "__main__":
    main()
