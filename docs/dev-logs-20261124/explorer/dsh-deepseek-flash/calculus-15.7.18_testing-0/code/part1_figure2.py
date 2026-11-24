"""Draw the three projections of the solid of Part 1.

Each panel keeps two coordinates and drops the third one, and each panel takes its area from the
record that `part1_verify.py` writes.
"""

from __future__ import annotations

import json
import math
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
"""Number of parameter steps of each boundary curve."""

FILL_ALPHA = 0.35
"""Opacity of the filled projection."""

LABEL_FONT_SIZE = 11
"""Font size of every panel label."""


def load_areas() -> dict[str, str]:
    """Return the area strings that the verification script of Part 1 writes."""
    record = json.loads((OUTPUT_DIRECTORY / "part1_values.json").read_text(encoding="utf-8"))
    return {
        "plane_x_zero": record["p1_yz_area_latex"],
        "plane_y_zero": record["p1_xz_area_latex"],
        "plane_z_zero": record["p1_xy_area_latex"],
    }


def draw_quarter_disk(axes: plt.Axes) -> None:
    """Draw the projection on the plane x = 0, which is the quarter disk of radius three.

    Args:
        axes: Axes of the panel.
    """
    angle = np.linspace(0.0, math.pi / 2.0, CURVE_STEPS)
    first = np.concatenate([[0.0], CYLINDER_RADIUS * np.cos(angle)])
    second = np.concatenate([[0.0], CYLINDER_RADIUS * np.sin(angle)])
    axes.fill(first, second, color="#F58518", alpha=FILL_ALPHA)
    axes.plot(first, second, color="#B8540A", linewidth=1.8)


def draw_height_region(axes: plt.Axes) -> None:
    """Draw the projection on the plane y = 0, which is the region under one cubic root.

    Args:
        axes: Axes of the panel.
    """
    height = np.linspace(0.0, CYLINDER_RADIUS, CURVE_STEPS)
    width = np.sqrt(CYLINDER_RADIUS**2 - height**2) / PLANE_SLOPE
    axes.fill_between(height, 0.0, width, color="#4C78A8", alpha=FILL_ALPHA)
    axes.plot(height, width, color="#2C4E6E", linewidth=1.8)


def draw_triangle(axes: plt.Axes) -> None:
    """Draw the projection on the plane z = 0, which is the triangle of the three corners.

    Args:
        axes: Axes of the panel.
    """
    corners = np.array([[0.0, 0.0], [0.0, CYLINDER_RADIUS], [1.0, CYLINDER_RADIUS]])
    axes.fill(corners[:, 0], corners[:, 1], color="#54A24B", alpha=FILL_ALPHA)
    axes.plot(
        np.append(corners[:, 0], corners[0, 0]),
        np.append(corners[:, 1], corners[0, 1]),
        color="#2F6B2A",
        linewidth=1.8,
    )


def main() -> None:
    """Draw the figure and write it to the figure directory."""
    areas = load_areas()
    figure, panels = plt.subplots(1, 3, figsize=(11.6, 4.0), dpi=FIGURE_DPI)

    draw_quarter_disk(panels[0])
    panels[0].set_xlabel(r"$y$")
    panels[0].set_ylabel(r"$z$")
    panels[0].set_title(r"projection on the plane $x = 0$", fontsize=LABEL_FONT_SIZE)
    label_first = panels[0].text(1.55, 1.55, "area $" + areas["plane_x_zero"] + "$", fontsize=LABEL_FONT_SIZE)

    draw_height_region(panels[1])
    panels[1].set_xlabel(r"$z$")
    panels[1].set_ylabel(r"$x$")
    panels[1].set_title(r"projection on the plane $y = 0$", fontsize=LABEL_FONT_SIZE)
    label_second = panels[1].text(1.45, 1.45, "area $" + areas["plane_y_zero"] + "$", fontsize=LABEL_FONT_SIZE)

    draw_triangle(panels[2])
    panels[2].set_xlabel(r"$x$")
    panels[2].set_ylabel(r"$y$")
    panels[2].set_title(r"projection on the plane $z = 0$", fontsize=LABEL_FONT_SIZE)
    label_third = panels[2].text(1.25, 1.35, "area $" + areas["plane_z_zero"] + "$", fontsize=LABEL_FONT_SIZE)

    for panel in panels:
        panel.set_aspect("equal")
        panel.grid(alpha=0.25)
        panel.set_xlim(-0.15, 3.35)
        panel.set_ylim(-0.15, 3.35)
    assert_texts_inside_axes(figure, panels[0], [label_first], "part1_figure2 panel one")
    assert_texts_inside_axes(figure, panels[1], [label_second], "part1_figure2 panel two")
    assert_texts_inside_axes(figure, panels[2], [label_third], "part1_figure2 panel three")
    figure.tight_layout()
    save_figure(figure, FIGURE_DIRECTORY / "part1_figure2.png")
    plt.close(figure)
    print(f"the three panels carry the areas {areas}")


if __name__ == "__main__":
    main()
