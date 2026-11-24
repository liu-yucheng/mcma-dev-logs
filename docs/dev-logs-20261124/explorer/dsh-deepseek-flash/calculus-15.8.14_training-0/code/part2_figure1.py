r"""Draw Figure 2: the area of the horizontal section at each height of the body.

The left panel shows the area of the section, $A(z) = \pi \min(z, 5 - z)$, over
the full height of the body and marks the three heights that the verification
script samples.  The right panel shows the three sections as filled disks.  The
script checks that every text of the figure lies inside its axes box.
"""

from __future__ import annotations

import math
import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

from drawing_frame import assert_annotation_inside_axes, assert_legend_inside_axes

FIGURE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "part2_figure1.png")
SAMPLED_HEIGHTS = (0.5, 2.5, 4.5)
TOP_HEIGHT = 5.0
RIM_SQUARED_RADIUS = 2.5
CURVE_COLOR = "#1f4e79"
MARKER_COLOR = "#b03a2e"


def section_area(height: float) -> float:
    """Return the area of the horizontal section of the body at one height."""
    return math.pi * min(height, TOP_HEIGHT - height)


def section_radius(height: float) -> float:
    """Return the radius of the horizontal section of the body at one height."""
    return math.sqrt(min(height, TOP_HEIGHT - height))


def draw_figure() -> plt.Figure:
    """Build the two panels of Figure 2 and return the figure."""
    figure, (area_axes, section_axes) = plt.subplots(1, 2, figsize=(10.4, 4.4), dpi=170)
    heights = np.linspace(0.0, TOP_HEIGHT, 501)
    areas = np.array([section_area(float(height)) for height in heights])
    curve, = area_axes.plot(heights, areas, color=CURVE_COLOR, linewidth=2.0)
    for height in SAMPLED_HEIGHTS:
        area_axes.plot(
            [height], [section_area(height)], marker="o", markersize=7.0, color=MARKER_COLOR,
            linestyle="none",
        )
        offset_points = (6.0, 10.0) if height < 4.0 else (-112.0, 12.0)
        area_axes.annotate(
            f"$z = {height:g}$, $A = {section_area(height):.6f}$",
            xy=(height, section_area(height)),
            xytext=offset_points,
            textcoords="offset points",
            fontsize=8.5,
            color="#20262e",
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.78, "pad": 1.2},
        )
    area_axes.axvline(RIM_SQUARED_RADIUS, color="#6b6b6b", linewidth=1.0, linestyle="--")
    peak_annotation = area_axes.annotate(
        f"widest section at $z = {RIM_SQUARED_RADIUS:g}$",
        xy=(RIM_SQUARED_RADIUS, section_area(RIM_SQUARED_RADIUS)),
        xytext=(-118.0, -34.0),
        textcoords="offset points",
        fontsize=9.0,
        color="#20262e",
        arrowprops={"arrowstyle": "-", "color": "#6b6b6b", "linewidth": 0.9},
    )
    area_axes.set_xlabel("height $z$ of the section")
    area_axes.set_ylabel("area $A(z)$ of the section")
    area_axes.set_title("Area of the horizontal section against its height", fontsize=10.5)
    area_axes.set_xlim(-0.15, 5.15)
    area_axes.set_ylim(0.0, 9.2)
    area_axes.grid(True, color="#d5d5d5", linewidth=0.6)
    area_axes.legend(
        [curve], [r"$A(z) = \pi \min(z, 5 - z)$"],
        loc="upper left", fontsize=9.0, frameon=True,
    )

    disk_handles = []
    for height in SAMPLED_HEIGHTS:
        radius = section_radius(height)
        disk = Circle((0.0, 0.0), radius, facecolor="#8fb4d9", edgecolor="#1f4e79", linewidth=1.4, alpha=0.55)
        section_axes.add_patch(disk)
        disk_handles.append(disk)
    rim_radius = math.sqrt(RIM_SQUARED_RADIUS)
    rim_circle = Circle(
        (0.0, 0.0), rim_radius, facecolor="none", edgecolor="#101010", linewidth=1.2, linestyle="--"
    )
    section_axes.add_patch(rim_circle)
    rim_annotation = section_axes.annotate(
        r"$x^{2} + y^{2} = \frac{5}{2}$",
        xy=(rim_radius * math.cos(math.radians(58.0)), rim_radius * math.sin(math.radians(58.0))),
        xytext=(10.0, 10.0),
        textcoords="offset points",
        fontsize=9.0,
        color="#101010",
    )
    section_axes.set_aspect("equal")
    section_axes.set_xlim(-2.05, 2.05)
    section_axes.set_ylim(-2.05, 2.05)
    section_axes.set_xlabel("$x$")
    section_axes.set_ylabel("$y$")
    section_axes.set_title("Three sections of the body, seen from above", fontsize=10.5)
    section_axes.grid(True, color="#e0e0e0", linewidth=0.6)
    section_legend = section_axes.legend(
        disk_handles,
        [
            f"$z = {height:g}$: $r = {section_radius(height):.4f}$, $A = {section_area(height):.4f}$"
            for height in SAMPLED_HEIGHTS
        ],
        loc="lower left",
        fontsize=8.0,
        frameon=True,
    )

    figure.tight_layout()
    assert_legend_inside_axes(figure, area_axes, area_axes.get_legend())
    assert_legend_inside_axes(figure, section_axes, section_legend)
    for annotation in list(area_axes.texts) + list(section_axes.texts):
        assert_annotation_inside_axes(figure, annotation.axes, annotation)
    assert_annotation_inside_axes(figure, area_axes, peak_annotation)
    assert_annotation_inside_axes(figure, section_axes, rim_annotation)
    print(f"annotations checked inside their axes boxes: {len(area_axes.texts) + len(section_axes.texts)}")
    return figure


def main() -> None:
    """Write Figure 2 to the figures directory."""
    os.makedirs(os.path.dirname(FIGURE_PATH), exist_ok=True)
    figure = draw_figure()
    figure.savefig(FIGURE_PATH, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
