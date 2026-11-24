"""Draw the two limits of the chosen order dz dx dy on the two projections.

Panel one is the quarter disk of the (y, z) plane, which holds the limit of z at a fixed y.
Panel two is the triangle of the (x, y) plane, which holds the limit of x at the same fixed y.
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

STRIP_COLOR = "#B279A2"
"""Color of the strip that marks the limits at the demonstration height."""

LABEL_FONT_SIZE = 11
"""Font size of every panel label."""


def load_demo_values() -> dict[str, float]:
    """Return the height and the two limits that the verification script of Part 2 writes."""
    record = json.loads((OUTPUT_DIRECTORY / "part2_values.json").read_text(encoding="utf-8"))
    return {
        "height": float(record["p2_demo_height"]),
        "x_high": float(record["p2_demo_x_high"]),
        "z_high": float(record["p2_demo_z_high"]),
    }


def main() -> None:
    """Draw the figure and write it to the figure directory."""
    demo = load_demo_values()
    figure, panels = plt.subplots(1, 2, figsize=(9.8, 4.3), dpi=FIGURE_DPI)

    angle = np.linspace(0.0, math.pi / 2.0, CURVE_STEPS)
    boundary_y = CYLINDER_RADIUS * np.cos(angle)
    boundary_z = CYLINDER_RADIUS * np.sin(angle)
    panels[0].fill(
        np.concatenate([[0.0], boundary_y]), np.concatenate([[0.0], boundary_z]), color="#4C78A8", alpha=0.25
    )
    panels[0].plot(boundary_y, boundary_z, color="#2C4E6E", linewidth=1.6)
    panels[0].plot(
        [demo["height"], demo["height"]],
        [0.0, demo["z_high"]],
        color=STRIP_COLOR,
        linewidth=3.2,
        solid_capstyle="butt",
    )
    panels[0].set_xlabel(r"$y$")
    panels[0].set_ylabel(r"$z$")
    panels[0].set_title(r"the limit of $z$ at one fixed $y$", fontsize=LABEL_FONT_SIZE)
    text_first = panels[0].text(
        0.10,
        0.30,
        rf"$y = {demo['height']:.3f}$:  $0 \leq z \leq {demo['z_high']:.6f}$",
        fontsize=LABEL_FONT_SIZE - 1,
    )

    corners = np.array([[0.0, 0.0], [0.0, CYLINDER_RADIUS], [1.0, CYLINDER_RADIUS]])
    panels[1].fill(corners[:, 0], corners[:, 1], color="#54A24B", alpha=0.25)
    panels[1].plot(
        np.append(corners[:, 0], corners[0, 0]),
        np.append(corners[:, 1], corners[0, 1]),
        color="#2F6B2A",
        linewidth=1.6,
    )
    panels[1].plot(
        [0.0, demo["x_high"]],
        [demo["height"], demo["height"]],
        color=STRIP_COLOR,
        linewidth=3.2,
        solid_capstyle="butt",
    )
    panels[1].set_xlabel(r"$x$")
    panels[1].set_ylabel(r"$y$")
    panels[1].set_title(r"the limit of $x$ at the same fixed $y$", fontsize=LABEL_FONT_SIZE)
    text_second = panels[1].text(
        0.35,
        0.45,
        rf"$y = {demo['height']:.3f}$:  $0 \leq x \leq {demo['x_high']:.6f}$",
        fontsize=LABEL_FONT_SIZE - 1,
    )

    for panel in panels:
        panel.set_xlim(-0.15, 3.35)
        panel.set_ylim(-0.15, 3.35)
        panel.set_aspect("equal")
        panel.grid(alpha=0.25)
    assert_texts_inside_axes(figure, panels[0], [text_first], "part2_figure1 panel one")
    assert_texts_inside_axes(figure, panels[1], [text_second], "part2_figure1 panel two")
    figure.tight_layout()
    save_figure(figure, FIGURE_DIRECTORY / "part2_figure1.png")
    plt.close(figure)
    print(
        f"the strip of the first panel runs from z = 0 to z = {demo['z_high']:.6f} at y = "
        f"{demo['height']:.3f}, and the strip of the second panel runs from x = 0 to x = "
        f"{demo['x_high']:.6f} at the same y"
    )


if __name__ == "__main__":
    main()
