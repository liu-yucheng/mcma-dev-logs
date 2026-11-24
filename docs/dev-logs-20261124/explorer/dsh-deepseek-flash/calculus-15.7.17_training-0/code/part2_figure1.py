"""Draw the two views that motivate the inner integral of Part 2.

The left panel shows the cross section of E in the plane z = 0.  The curve is
x = 4*r^2, the straight line is x = 4, and the shaded band is E.  A vertical arrow
at r = 0.7 shows the segment that the inner integral covers.

The right panel shows the disk that the plane x = 2 cuts from E.  The disk has
radius sqrt(2)/2.  A small polar element shows the area factor r dr dtheta.

The script writes the figure to code/figures/part2_figure1.png.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

PARABOLOID_COEFFICIENT: float = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_POSITION: float = 4.0
"""Position of the flat boundary plane x = PLANE_POSITION."""

FIGURE_DPI: int = 200
"""Resolution of the written image in dots per inch."""

COLOR_REGION: str = "#2f5d8a"
"""Fill color of the solid region."""

COLOR_ACCENT: str = "#c8863c"
"""Color of the marked segment and the marked element."""

FIGURE_PATH: Path = Path(__file__).resolve().parent / "figures" / "part2_figure1.png"
"""Output path of the figure."""


def apply_style() -> None:
    """Set a consistent style for the figure."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Cambria", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 10,
        "axes.linewidth": 0.8,
        "axes.edgecolor": "#333333",
        "figure.facecolor": "white",
    })


def draw_cross_section(axes: plt.Axes) -> None:
    """Draw the cross section of E in the plane z = 0.

    The vertical arrow marks the segment that the inner integral covers at a fixed
    radius r = 0.6.  The two boundary curves are labelled next to their points.

    Args:
        axes: The axes of the left panel.
    """
    radius_values = np.linspace(0.0, 1.0, 400)
    axes.fill_between(radius_values, PARABOLOID_COEFFICIENT * radius_values**2,
                      PLANE_POSITION, color=COLOR_REGION, alpha=0.20, linewidth=0.0)
    axes.plot(radius_values, PARABOLOID_COEFFICIENT * radius_values**2, color=COLOR_REGION,
              linewidth=2.2, zorder=3)
    axes.axhline(PLANE_POSITION, color="#8a5a1c", linewidth=1.8, zorder=3)
    marked_radius = 0.6
    lower_bound = PARABOLOID_COEFFICIENT * marked_radius**2
    axes.annotate("", xy=(marked_radius, PLANE_POSITION), xytext=(marked_radius, lower_bound),
                  arrowprops={"arrowstyle": "<->", "color": COLOR_ACCENT, "linewidth": 1.8,
                              "shrinkA": 0.0, "shrinkB": 0.0})
    axes.plot([0.0, marked_radius], [lower_bound, lower_bound], color=COLOR_ACCENT,
              linewidth=0.8, linestyle=(0, (2, 2)), zorder=1)
    axes.text(marked_radius + 0.05, 0.5 * (lower_bound + PLANE_POSITION) - 0.05,
              r"$\int_{4r^2}^{4} x\,dx$", color="#8a5a1c", fontsize=12)
    axes.text(0.72, 3.62, r"$x = 4$", color="#8a5a1c", fontsize=10.5)
    axes.text(0.76, 1.42, r"$x = 4r^2$", color=COLOR_REGION, fontsize=10.5)
    axes.text(0.17, 2.35, r"$E \cap \{z = 0\}$", color="#4a5b6b", fontsize=10)
    axes.set_xlim(0.0, 1.12)
    axes.set_ylim(0.0, 4.55)
    axes.set_xlabel(r"$r = \sqrt{y^2 + z^2}$")
    axes.set_ylabel(r"$x$")
    axes.set_title("Cross section at $z = 0$, fixed $(y, z)$", fontsize=10.5)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)


def draw_slice(axes: plt.Axes) -> None:
    """Draw the disk that the plane x = 2 cuts from E.

    Args:
        axes: The axes of the right panel.
    """
    slice_x = 2.0
    slice_radius = math.sqrt(slice_x / PARABOLOID_COEFFICIENT)
    angle_values = np.linspace(0.0, 2.0 * math.pi, 400)
    axes.fill(slice_radius * np.cos(angle_values), slice_radius * np.sin(angle_values),
              color=COLOR_REGION, alpha=0.22, linewidth=0.0)
    axes.plot(slice_radius * np.cos(angle_values), slice_radius * np.sin(angle_values),
              color=COLOR_REGION, linewidth=2.0)
    element_radius = 0.62 * slice_radius
    element_half_width = 0.30
    element_angle = math.radians(38.0)
    element_angles = np.linspace(element_angle - element_half_width, element_angle + element_half_width, 40)
    axes.fill(np.concatenate(([0.0], element_radius * np.cos(element_angles))),
              np.concatenate(([0.0], element_radius * np.sin(element_angles))),
              color=COLOR_ACCENT, alpha=0.45, linewidth=0.0)
    axes.plot([0.0, 0.72 * np.cos(element_angle)], [0.0, 0.72 * np.sin(element_angle)],
              color=COLOR_ACCENT, linewidth=1.2)
    axes.annotate("", xy=(0.40 * np.cos(element_angle + element_half_width),
                          0.40 * np.sin(element_angle + element_half_width)),
                  xytext=(0.34 * np.cos(element_angle - element_half_width),
                          0.34 * np.sin(element_angle - element_half_width)),
                  arrowprops={"arrowstyle": "->", "color": COLOR_ACCENT, "linewidth": 1.0})
    axes.text(-0.52, -0.44, r"$dA = r\,dr\,d\theta$", color="#8a5a1c", fontsize=10)
    axes.text(0.06, 0.30, r"$r$", color=COLOR_ACCENT, fontsize=9)
    axes.axhline(0.0, color="#999999", linewidth=0.7, zorder=0)
    axes.axvline(0.0, color="#999999", linewidth=0.7, zorder=0)
    axes.text(0.74, -0.10, r"$y$", fontsize=9.5)
    axes.text(-0.10, 0.74, r"$z$", fontsize=9.5)
    axes.set_aspect("equal")
    axes.set_xlim(-0.85, 0.85)
    axes.set_ylim(-0.85, 0.85)
    axes.set_title(r"Slice at $x = 2$: disk of radius $\sqrt{2}/2$", fontsize=10.5)
    axes.set_xticks([])
    axes.set_yticks([])
    for spine in axes.spines.values():
        spine.set_visible(False)


def build_figure() -> plt.Figure:
    """Build the complete figure.

    Returns:
        The figure object that holds the two panels.
    """
    figure, (left_axes, right_axes) = plt.subplots(1, 2, figsize=(9.4, 4.1))
    draw_cross_section(left_axes)
    draw_slice(right_axes)
    figure.tight_layout(pad=1.2)
    return figure


def main() -> int:
    """Draw the figure and write it to the figures directory.

    Returns:
        The process exit status: 0 on success.
    """
    apply_style()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure = build_figure()
    figure.savefig(FIGURE_PATH, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
