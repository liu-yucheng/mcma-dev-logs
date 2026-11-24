"""Draw the integrand and the antiderivative of the outer integral of Part 3.

Panel one shows the integrand with the filled area under it.  Panel two shows the antiderivative,
whose change from zero to three is the value of that area.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from figure_support import assert_texts_inside_axes, save_figure
from geometry_anchors import CYLINDER_RADIUS, FIGURE_DPI, PLANE_SLOPE

FIGURE_DIRECTORY = Path(__file__).resolve().parent / "figures"
"""Directory that holds every rendered figure."""

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"
"""Directory that holds the JSON record of every part."""

CURVE_STEPS = 401
"""Number of sample points of each curve."""

LABEL_FONT_SIZE = 11
"""Font size of every panel label."""


def load_answer() -> dict[str, str]:
    """Return the answer strings that the verification script of Part 3 writes."""
    record = json.loads((OUTPUT_DIRECTORY / "part3_values.json").read_text(encoding="utf-8"))
    return {
        "answer_latex": record["p3_answer_latex"],
        "answer_decimal": record["p3_answer_decimal"],
        "antiderivative_latex": record["p3_antiderivative_latex"],
    }


def outer_integrand(values: np.ndarray) -> np.ndarray:
    """Return the outer integrand at the given values.

    Args:
        values: Array of the value of y.
    """
    return (CYLINDER_RADIUS**2 * values - values**3) / (2.0 * PLANE_SLOPE)


def outer_antiderivative(values: np.ndarray) -> np.ndarray:
    """Return the antiderivative of the outer integrand at the given values.

    Args:
        values: Array of the value of y.
    """
    return 3.0 * values**2 / 4.0 - values**4 / 24.0


def main() -> None:
    """Draw the figure and write it to the figure directory."""
    answer = load_answer()
    heights = np.linspace(0.0, CYLINDER_RADIUS, CURVE_STEPS)
    figure, panels = plt.subplots(1, 2, figsize=(10.0, 4.2), dpi=FIGURE_DPI)

    panels[0].fill_between(heights, 0.0, outer_integrand(heights), color="#F58518", alpha=0.3)
    panels[0].plot(heights, outer_integrand(heights), color="#B8540A", linewidth=2.0)
    panels[0].set_xlabel(r"$y$")
    panels[0].set_ylabel(r"$\dfrac{9y - y^{3}}{6}$")
    panels[0].set_title(r"the outer integrand", fontsize=LABEL_FONT_SIZE)
    text_first = panels[0].text(
        1.15,
        2.35,
        "area $" + answer["answer_latex"] + " = " + answer["answer_decimal"] + "$",
        fontsize=LABEL_FONT_SIZE - 1,
    )

    antiderivative_values = outer_antiderivative(heights)
    panels[1].plot(heights, antiderivative_values, color="#4C78A8", linewidth=2.0)
    panels[1].plot([CYLINDER_RADIUS], [float(antiderivative_values[-1])], marker="o", color="#2C4E6E")
    panels[1].plot([0.0], [0.0], marker="o", color="#2C4E6E")
    panels[1].set_xlabel(r"$y$")
    panels[1].set_ylabel(r"$\dfrac{3y^{2}}{4} - \dfrac{y^{4}}{24}$")
    panels[1].set_title(r"the antiderivative", fontsize=LABEL_FONT_SIZE)
    text_second = panels[1].text(
        0.20,
        3.05,
        "change from $" + "0$ to $" + f"{CYLINDER_RADIUS:.0f}" + "$ equals $" + answer["answer_latex"] + "$",
        fontsize=LABEL_FONT_SIZE - 1,
    )

    for panel in panels:
        panel.set_xlim(-0.15, 3.35)
        panel.set_ylim(-0.25, 4.1)
        panel.grid(alpha=0.25)
    assert_texts_inside_axes(figure, panels[0], [text_first], "part3_figure1 panel one")
    assert_texts_inside_axes(figure, panels[1], [text_second], "part3_figure1 panel two")
    figure.tight_layout()
    save_figure(figure, FIGURE_DIRECTORY / "part3_figure1.png")
    plt.close(figure)
    print(f"the antiderivative rises from 0 to {float(antiderivative_values[-1]):.9f} on the interval")


if __name__ == "__main__":
    main()
