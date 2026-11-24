"""Part 2: derive the slice at a fixed height z and the iterated integral from the inequalities.

The slice at height z is derived from the four inequalities, not read from a drawing.  Its
area is computed three ways: the closed form (1 - z^2) / 2, adaptive quadrature of the inner
integral, and a Monte Carlo count of points inside the slice.  The same three ways must agree
at every sampled height.
"""

from __future__ import annotations

import random

import mcma_support as support

SEED = 20261123
"""Seed of the Monte Carlo count of the slice area."""

SLICE_SAMPLES = 400000
"""Number of random points per slice of the Monte Carlo area."""

HEIGHTS = [0.0, 0.25, 0.5, 0.75]
"""Heights at which the three descriptions of the slice area are compared."""


def monte_carlo_slice_area(z: float, seed: int) -> float:
    """Return the area of the slice at height z by a count of points in the unit square.

    The square is 0 <= x <= 1 and 0 <= y <= 1.  A point counts when y <= sqrt(1 - z^2) and
    x <= y.  The count does not use the closed form of the area.
    """
    generator = random.Random(seed)
    height = support.cylinder_height(z)
    hits = 0
    for _ in range(SLICE_SAMPLES):
        x = generator.random()
        y = generator.random()
        if y <= height and x <= y:
            hits += 1
    return hits / SLICE_SAMPLES


def main() -> None:
    """Run the checks of Part 2 and write its record."""
    recorder = support.Recorder(2)
    random.seed(SEED)

    samples: list[tuple[float, float, float, float]] = []
    for index, z in enumerate(HEIGHTS):
        exact = support.slice_area_exact(z)
        quadrature = support.slice_area_quadrature(z)
        sampled = monte_carlo_slice_area(z, SEED + index)
        standard_error = max((sampled * (1.0 - sampled) / SLICE_SAMPLES) ** 0.5, 1.0e-12)
        recorder.record(f"slice at z = {z:.2f}: quadrature against the closed form",
                        quadrature, exact)
        recorder.record(f"slice at z = {z:.2f}: Monte Carlo against the closed form, "
                        f"in standard errors",
                        abs(sampled - exact) / standard_error, 0.0, tolerance=4.0)
        samples.append((z, exact, quadrature, sampled))
        print(f"slice summary z = {z:.2f}: closed form {exact:.9f} quadrature {quadrature:.9f} "
              f"Monte Carlo {sampled:.6f} length along y {support.slice_length_at_height(z):.9f}")

    widths = [support.slice_length_at_height(z) for z in HEIGHTS]
    recorder.record_text("width along y falls from z = 0 to z = 1",
                         "decreasing" if all(a > b for a, b in zip(widths, widths[1:]))
                         else "not decreasing", "decreasing")
    recorder.publish("p2_widths", ", ".join(f"{value:.6f}" for value in widths))
    recorder.publish("p2_height_count", str(len(HEIGHTS)))
    empty_slice = support.slice_area_exact(1.0)
    recorder.record("slice at z = 1: closed form against the quadrature of an empty interval",
                    empty_slice, support.slice_area_quadrature(1.0))

    integral = support.integrate(support.slice_area_exact, 0.0, 1.0)
    recorder.record("sum of the slice areas: quadrature against 1 / 3", integral, 1.0 / 3.0)
    recorder.publish("p2_slice_integral", f"{integral:.12f}")

    table_rows = []
    for z, exact, quadrature, sampled in samples:
        table_rows.append({"z": f"{z:.2f}", "closed": f"{exact:.9f}",
                           "quadrature": f"{quadrature:.9f}", "monte": f"{sampled:.6f}"})
    recorder.publish("p2_table", str(table_rows))
    recorder.publish("p2_heights", ", ".join(f"{z:.2f}" for z in HEIGHTS))
    recorder.publish("p2_table_areas", ", ".join(f"{exact:.9f}" for _, exact, _, _ in samples))
    recorder.write()


if __name__ == "__main__":
    main()
