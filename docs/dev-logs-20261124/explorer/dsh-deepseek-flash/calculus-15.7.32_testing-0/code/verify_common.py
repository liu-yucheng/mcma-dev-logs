"""Shared output helpers for the verification scripts of the tutorial.

Each verification script records one dictionary of named values and one list of checks.
The values feed the placeholders of the composed page. The checks feed the verification
table of the composed page.

Constants:
    OUTPUT_DIRECTORY: The directory of the JSON records, relative to the workspace root.
"""

import json
import os

OUTPUT_DIRECTORY = os.path.join("code", "outputs")


def record(part_number, values, checks):
    """Write one JSON record and restate every check on the standard output.

    Args:
        part_number: The number of the part, as an integer.
        values: A dictionary of named strings and numbers for the composed page.
        checks: A list of dictionaries with the keys name, computed, expected, and passed.

    Returns:
        The path of the written file.
    """
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(workspace, OUTPUT_DIRECTORY)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "part%d_results.json" % part_number)
    payload = {"part": part_number, "values": values, "checks": checks}
    with open(path, "w", encoding="utf-8", newline="\n") as stream:
        json.dump(payload, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    for item in checks:
        mark = "PASS" if item["passed"] else "FAIL"
        print("%s  %-46s computed=%s expected=%s" % (mark, item["name"], item["computed"], item["expected"]))
    print("checks passed: %d of %d" % (sum(1 for item in checks if item["passed"]), len(checks)))
    return path


def check(name, computed, expected, tolerance=0.0, comparison="close"):
    """Build one check record.

    Args:
        name: The name of the check.
        computed: The value that one method computes.
        expected: The value that a different method computes.
        tolerance: The absolute tolerance of the comparison.
        comparison: "close" for a numeric comparison within the tolerance, "equal" for an
            exact comparison, "differ" when the two values must differ, and "above" when
            the computed value must reach the expected bound.

    Returns:
        A dictionary that describes the check.
    """
    if comparison == "equal":
        passed = bool(computed == expected)
    elif comparison == "differ":
        passed = bool(abs(float(computed) - float(expected)) > 1e-12)
    elif comparison == "above":
        passed = bool(float(computed) >= float(expected))
    else:
        passed = bool(abs(float(computed) - float(expected)) <= float(tolerance))
    return {
        "name": name,
        "computed": computed if isinstance(computed, (int, float)) else str(computed),
        "expected": expected if isinstance(expected, (int, float)) else str(expected),
        "tolerance": float(tolerance),
        "passed": passed,
    }


def as_text(value):
    """Return a stable text form of a number for the composed page.

    Args:
        value: A number or a text.

    Returns:
        A text with twelve significant digits for a float, and the unchanged value for a text.
    """
    if isinstance(value, str):
        return value
    if isinstance(value, int):
        return str(value)
    return "%.12g" % float(value)
