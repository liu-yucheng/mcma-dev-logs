"""Draw the four contributions of the binomial expansion as one bar chart.

The chart shows that the constant term gives the unit ball, that the linear and the cubic term
give zero, and that the quadratic term gives the excess of the body over the unit ball.
"""

from __future__ import annotations

import math
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

import bumpy_sphere
import figure_tools

TEXT_COLOUR = "#1a1a1a"
"""Colour of the bar labels."""

BAR_COLOUR = "#1d4f7a"
"""Colour of the bars of the two terms that do not vanish."""

ZERO_COLOUR = "#b0b0b0"
"""Colour of the bars of the two terms that vanish."""


def contribution_rows() -> list[tuple[str, float, str]]:
    """Return one row for each term of the binomial expansion.

    Returns:
        One tuple of a bar label, the value of the term, and the explanation of that term.
    """
    return [
        ("constant term", bumpy_sphere.exact_volume_of_term(0, 0).as_float(),
         r"$4\pi/3$, the unit ball"),
        ("linear term", bumpy_sphere.exact_volume_of_term(1, 1).as_float(),
         r"$0$, the azimuthal factor vanishes"),
        ("quadratic term", bumpy_sphere.exact_volume_of_term(2, 2).as_float(),
         r"$4\pi/99$, the excess"),
        ("cubic term", bumpy_sphere.exact_volume_of_term(3, 3).as_float(),
         r"$0$, the cubic azimuthal factor vanishes"),
    ]


def draw_contributions(axes: matplotlib.axes.Axes) -> list:
    """Draw the four terms as horizontal bars and label each bar with its value.

    Args:
        axes: Axes that holds the chart.

    Returns:
        The nine texts that the layout check measures.
    """
    rows = contribution_rows()
    positions = list(range(len(rows)))
    values = [row[1] for row in rows]
    colours = [BAR_COLOUR if abs(value) > 1.0e-12 else ZERO_COLOUR for value in values]
    axes.barh(positions, values, height=0.52, color=colours, edgecolor="white", linewidth=0.8)
    axes.set_yticks(positions)
    axes.set_yticklabels([row[0] + "\n" + row[2] for row in rows], fontsize=8.6)
    axes.invert_yaxis()
    axes.set_xlim(0.0, 6.2)
    axes.set_xlabel("volume of the term in cubic length units", fontsize=10)
    axes.set_title("(a) the four terms of $(1+t)^{3}$, with $t=\\frac{1}{5}\\sin 6\\theta\\,\\sin 5\\varphi$",
                   fontsize=10.5, color=TEXT_COLOUR)
    axes.grid(axis="x", color="#dcdcdc", linewidth=0.6)
    axes.set_axisbelow(True)
    texts = []
    for position, (_label, value, _explanation) in zip(positions, rows):
        gap = 0.09
        texts.append(axes.annotate(
            f"{value:.9f}",
            xy=(max(value, 0.0) + gap, position), xycoords="data",
            xytext=(max(value, 0.0) + gap, position), textcoords="data",
            fontsize=8.8, va="center", ha="left", color=TEXT_COLOUR,
        ))
    return texts


def draw_total(axes: matplotlib.axes.Axes) -> list:
    """Draw the sum of the four terms as one bar with its value.

    Args:
        axes: Axes that holds the chart.

    Returns:
        The one text that the layout check measures.
    """
    total = bumpy_sphere.exact_volume().as_float()
    axes.barh([0], [total], height=0.52, color="#4a8fb5", edgecolor="white", linewidth=0.8)
    axes.set_yticks([0])
    axes.set_yticklabels(["sum", "of the four terms"][:1], fontsize=9.5)
    axes.set_xlim(0.0, 6.2)
    axes.set_xlabel("volume of the body in cubic length units", fontsize=10)
    axes.set_title("(b) the sum of the four terms", fontsize=10.5, color=TEXT_COLOUR)
    axes.grid(axis="x", color="#dcdcdc", linewidth=0.6)
    axes.set_axisbelow(True)
    text = axes.annotate(
        f"{total:.9f}",
        xy=(total + 0.09, 0), xycoords="data",
        xytext=(total + 0.09, 0), textcoords="data",
        fontsize=8.8, va="center", ha="left", color=TEXT_COLOUR,
    )
    return [text]


def main() -> int:
    """Draw the figure and write the PNG file.

    Returns:
        Zero when the script writes the figure.
    """
    figure, (axes_left, axes_right) = plt.subplots(
        1, 2, figsize=(12.4, 3.9), gridspec_kw={"width_ratios": [2.05, 1.0]})
    texts = draw_contributions(axes_left)
    texts = texts + draw_total(axes_right)
    figure.tight_layout()
    figure_tools.finish_figure(figure, [axes_left, axes_right], texts, "part2_figure1")
    plt.close(figure)
    print(f"check: the four terms sum to {sum(row[1] for row in contribution_rows()):.12f}",
          flush=True)
    print(f"check: the exact volume is {bumpy_sphere.exact_volume().as_float():.12f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
