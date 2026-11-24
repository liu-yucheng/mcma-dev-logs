"""Cross-check the answers of Problem 25 against the prints of Parts 2, 3, and 4.

The script reads the JSON prints of the earlier parts, recomputes each quantity in a different
integration order and by rejection sampling, and compares the three values. It then builds the final
answer table from the checked values.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors
import verification_support as support

OUTPUT_PATH = Path(__file__).resolve().parent / "outputs" / "part5_results.json"
INPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"
SAMPLE_COUNT = 4_000_000


def density(x: float, y: float, z: float) -> float:
    """Return the density rho(x, y, z) = x^2 + y^2."""
    return x * x + y * y


def integrands() -> dict[str, support.Density]:
    """Return the five integrands whose integrals the answer needs."""
    return {
        "mass": density,
        "x rho": lambda x, y, z: x * density(x, y, z),
        "y rho": lambda x, y, z: y * density(x, y, z),
        "z rho": lambda x, y, z: z * density(x, y, z),
        "inertia": lambda x, y, z: density(x, y, z) ** 2,
    }


def load(name: str) -> dict[str, object]:
    """Return one result file of an earlier part."""
    return json.loads((INPUT_DIRECTORY / name).read_text(encoding="utf-8"))


def main() -> None:
    """Run every check of Part 5 and write the JSON result file."""
    print("PART 5: cross-checks and final answers")
    ledger = support.CheckLedger("part5")
    part2 = load("part2_results.json")
    part3 = load("part3_results.json")
    part4 = load("part4_results.json")
    printed = {
        "mass": float(part2["mass"]),
        "x rho": float(part3["numerator_x"]),
        "y rho": float(part3["numerator_y"]),
        "z rho": float(part3["numerator_z"]),
        "inertia": float(part4["iz"]),
    }
    seed = figure_anchors.MONTE_CARLO_SEED + 5
    rows = []
    worst_sigma = 0.0
    worst_relative = 0.0
    for name, function in integrands().items():
        alternate = support.integrate_dz_dy_dx(function)
        estimate, error = support.monte_carlo(function, SAMPLE_COUNT, seed)
        sigma = abs(estimate - printed[name]) / error if error > 0.0 else 0.0
        worst_sigma = max(worst_sigma, sigma)
        relative = abs(alternate - printed[name]) / abs(printed[name])
        worst_relative = max(worst_relative, relative)
        print(f"{name}: printed = {printed[name]:.9f}, dz dy dx = {alternate:.9f},"
              f" Monte Carlo = {estimate:.6f} +- {error:.6f} ({sigma:.2f} sigma),"
              f" relative difference of the orders = {relative:.2e}")
        ledger.add(f"{name}: the printed value against the second order",
                   float(alternate), float(printed[name]), support.RELATIVE_DIFFERENCE_LIMIT)
        ledger.add(f"{name}: the printed value against the sample",
                   float(estimate), float(printed[name]),
                   support.MONTE_CARLO_STANDARD_ERROR_FACTOR * error)
        rows.append({
            "name": name,
            "printed": f"{printed[name]:.6f}",
            "alternate": f"{alternate:.6f}",
            "relative_difference": f"{relative:.2e}",
            "relative_difference_latex": support.scientific_latex(relative),
            "monte_carlo": f"{estimate:.6f}",
            "error": f"{error:.6f}",
            "sigma": f"{sigma:.2f}",
        })

    mass_value = printed["mass"]
    coordinates = {
        "x": printed["x rho"] / mass_value,
        "y": printed["y rho"] / mass_value,
        "z": printed["z rho"] / mass_value,
    }
    final = {
        "mass": support.rounded_three_decimals(mass_value),
        "x": support.rounded_three_decimals(coordinates["x"]),
        "y": support.rounded_three_decimals(coordinates["y"]),
        "z": support.exact_three_decimals(15, 16),
        "iz": support.rounded_three_decimals(printed["inertia"]),
    }
    print(f"final answers: mass = {final['mass']}, center ="
          f" ({final['x']}, {final['y']}, {final['z']}), inertia = {final['iz']}")
    ledger.add_text("mass in three decimals", final["mass"], str(part2["mass_3dp"]))
    ledger.add_text("coordinate x in three decimals", final["x"], str(part3["x_bar_3dp"]))
    ledger.add_text("coordinate y in three decimals", final["y"], str(part3["y_bar_3dp"]))
    ledger.add_text("coordinate z in three decimals", final["z"], str(part3["z_bar_3dp"]))
    ledger.add_text("inertia in three decimals", final["iz"], str(part4["iz_3dp"]))

    counts = [int(load(name)["checks"]["count"]) for name in
              ("part1_results.json", "part2_results.json", "part3_results.json",
               "part4_results.json")]
    earlier_total = sum(counts)
    print(f"checks of the earlier parts: {counts}, total = {earlier_total}")

    inside = (
        3.0 * coordinates["x"] <= coordinates["y"] + 1.0e-12
        and coordinates["y"] ** 2 + coordinates["z"] ** 2 <= 9.0 + 1.0e-12
    )
    ledger.add_text("the center of mass lies inside E, checked again",
                    str(inside), "True")

    results = {
        "rows": rows,
        "final_mass": final["mass"],
        "final_x": final["x"],
        "final_y": final["y"],
        "final_z": final["z"],
        "final_iz": final["iz"],
        "worst_sigma": f"{worst_sigma:.2f}",
        "worst_relative_difference": f"{worst_relative:.2e}",
        "worst_relative_difference_latex": support.scientific_latex(worst_relative),
        "relative_difference_limit": f"{support.RELATIVE_DIFFERENCE_LIMIT:.1e}",
        "relative_difference_limit_latex": (
            f"10^{{-{int(round(-math.log10(support.RELATIVE_DIFFERENCE_LIMIT)))}}}"),
        "relative_difference_limit_denominator": (
            f"{int(round(1.0 / support.RELATIVE_DIFFERENCE_LIMIT)):.0f}"),
        "earlier_check_counts": [str(count) for count in counts],
        "earlier_check_total": str(earlier_total),
        "total_checks": str(earlier_total + len(ledger.records)),
        "checks": ledger.summary(),
    }
    support.write_results(OUTPUT_PATH, results)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
