"""Draw one section of E at a fixed value of each coordinate, and the area of the section.

Each panel derives its shape from the defining inequalities of E.  A horizontal slice at a fixed
value of x keeps the coordinates y and z, and its boundaries follow from x squared <= y <= 4 and
0 <= z <= (4 - y)/2.  A slice at a fixed value of y keeps the coordinates x and z.  A slice at a
fixed value of z keeps the coordinates x and y.  Panel (d) plots the area of each section against
the parameter of the family, and marks the three heights that ``code/part2_verify.py`` samples.

Run this script with the interpreter of ``code/.venv``.  It writes ``code/figures/part2_figure1.png``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_DIRECTORY = Path(__file__).resolve().parent / "figures"
"""Directory of the figure files."""

OUTPUT_PATH = FIGURE_DIRECTORY / "part2_figure1.png"
"""Path of the figure of this part."""

EDGE_COLOR = "#1f2933"
"""Color of the boundary of a section."""

SECTION_X_COLOR = "#7aa6c2"
"""Color of a section at a fixed value of x."""

SECTION_Y_COLOR = "#e3b778"
"""Color of a section at a fixed value of y."""

SECTION_Z_COLOR = "#9dc0a8"
"""Color of a section at a fixed value of z."""


def section_area_x(x_value: float) -> float:
    """Return the area of the section of E at a fixed value of x.

    Args:
        x_value: The fixed value of x.

    Returns:
        The area of the triangle (4 - x_value ** 2) ** 2 / 4.
    """
    return (4.0 - x_value * x_value) ** 2 / 4.0


def section_area_y(y_value: float) -> float:
    """Return the area of the section of E at a fixed value of y.

    Args:
        y_value: The fixed value of y.

    Returns:
        The area of the rectangle sqrt(y_value) * (4 - y_value).
    """
    return np.sqrt(max(y_value, 0.0)) * (4.0 - y_value)


def section_area_z(z_value: float) -> float:
    """Return the area of the section of E at a fixed value of z.

    Args:
        z_value: The fixed value of z.

    Returns:
        The area of the parabolic segment (4 / 3) * (4 - 2 * z_value) ** 1.5.
    """
    return (4.0 / 3.0) * (4.0 - 2.0 * z_value) ** 1.5


def draw_section_x(axes: plt.Axes) -> None:
    """Draw the section at x = 0, which keeps the coordinates y and z.

    Args:
        axes: The axes of the upper left panel.
    """
    y_values = np.linspace(0.0, 4.0, 300)
    axes.fill_between(y_values, 0.0, (4.0 - y_values) / 2.0, color=SECTION_X_COLOR, alpha=0.5,
                      linewidth=0.0)
    axes.plot([0.0, 4.0, 0.0, 0.0], [0.0, 0.0, 2.0, 0.0], color=EDGE_COLOR, linewidth=1.4)
    axes.set_xlim(-0.5, 4.6)
    axes.set_ylim(-0.32, 2.4)
    axes.set_xticks([0, 1, 2, 3, 4])
    axes.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
    axes.set_xlabel("y", fontsize=10)
    axes.set_ylabel("z", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Section at $x = 0$\n$0 \\leq z \\leq (4 - y)/2$, area $= 4$", fontsize=9.5, pad=6)


def draw_section_y(axes: plt.Axes) -> None:
    """Draw the section at y = 2, which keeps the coordinates x and z.

    Args:
        axes: The axes of the upper right panel.
    """
    axes.fill([-np.sqrt(2.0), np.sqrt(2.0), np.sqrt(2.0), -np.sqrt(2.0)], [0.0, 0.0, 1.0, 1.0],
              color=SECTION_Y_COLOR, alpha=0.55, linewidth=0.0)
    axes.plot([-np.sqrt(2.0), np.sqrt(2.0), np.sqrt(2.0), -np.sqrt(2.0), -np.sqrt(2.0)],
              [0.0, 0.0, 1.0, 1.0, 0.0], color=EDGE_COLOR, linewidth=1.4)
    axes.set_xlim(-2.6, 2.6)
    axes.set_ylim(-0.2, 1.4)
    axes.set_xticks([-2, -1, 0, 1, 2])
    axes.set_yticks([0, 0.5, 1.0])
    axes.set_xlabel("x", fontsize=10)
    axes.set_ylabel("z", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Section at $y = 2$\n$|x| \\leq \\sqrt{2}$, $0 \\leq z \\leq 1$, area $\\approx 2.828$",
                   fontsize=9.5, pad=6)


def draw_section_z(axes: plt.Axes) -> None:
    """Draw the section at z = 0.5, which keeps the coordinates x and y.

    Args:
        axes: The axes of the lower left panel.
    """
    x_values = np.linspace(-np.sqrt(3.0), np.sqrt(3.0), 400)
    axes.fill_between(x_values, x_values ** 2, 3.0, color=SECTION_Z_COLOR, alpha=0.55,
                      linewidth=0.0)
    axes.plot(x_values, x_values ** 2, color=EDGE_COLOR, linewidth=1.4)
    axes.plot([-np.sqrt(3.0), np.sqrt(3.0)], [3.0, 3.0], color=EDGE_COLOR, linewidth=1.4)
    axes.set_xlim(-2.6, 2.6)
    axes.set_ylim(-0.35, 3.55)
    axes.set_xticks([-2, -1, 0, 1, 2])
    axes.set_yticks([0, 1, 2, 3])
    axes.set_xlabel("x", fontsize=10)
    axes.set_ylabel("y", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Section at $z = 0.5$\n$x^2 \\leq y \\leq 3$, area $\\approx 6.928$", fontsize=9.5,
                   pad=6)


def draw_area_curves(axes: plt.Axes) -> None:
    """Draw the area of each section family against its parameter, with the sampled heights.

    Args:
        axes: The axes of the lower right panel.
    """
    x_parameter = np.linspace(-2.0, 2.0, 400)
    y_parameter = np.linspace(0.0, 4.0, 400)
    z_parameter = np.linspace(0.0, 2.0, 400)
    axes.plot(x_parameter, [section_area_x(value) for value in x_parameter], color=SECTION_X_COLOR,
              linewidth=1.8, label="section at fixed $x$")
    axes.plot(y_parameter, [section_area_y(value) for value in y_parameter], color=SECTION_Y_COLOR,
              linewidth=1.8, label="section at fixed $y$")
    axes.plot(z_parameter, [section_area_z(value) for value in z_parameter], color=SECTION_Z_COLOR,
              linewidth=1.8, label="section at fixed $z$")

    sampled_x = [0.0, 1.0, 1.9]
    sampled_y = [0.5, 2.0, 3.5]
    sampled_z = [0.0, 1.0, 1.5]
    axes.plot(sampled_x, [section_area_x(value) for value in sampled_x], linestyle="none",
              marker="o", markersize=5.0, color=EDGE_COLOR, label="heights checked in the script")
    axes.plot(sampled_y, [section_area_y(value) for value in sampled_y], linestyle="none",
              marker="o", markersize=5.0, color=EDGE_COLOR)
    axes.plot(sampled_z, [section_area_z(value) for value in sampled_z], linestyle="none",
              marker="o", markersize=5.0, color=EDGE_COLOR)
    axes.set_xlim(-2.4, 4.4)
    axes.set_ylim(-0.6, 12.4)
    axes.set_xlabel("parameter of the family", fontsize=10)
    axes.set_ylabel("area of the section", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Area of the section against its parameter", fontsize=9.5, pad=6)
    axes.legend(fontsize=7.5, frameon=False, loc="upper left", handlelength=1.4,
                labelspacing=0.25, borderpad=0.2)


def main() -> None:
    """Draw the four panels and write the figure."""
    FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    figure = plt.figure(figsize=(10.2, 8.2), dpi=170)
    draw_section_x(figure.add_subplot(2, 2, 1))
    draw_section_y(figure.add_subplot(2, 2, 2))
    draw_section_z(figure.add_subplot(2, 2, 3))
    draw_area_curves(figure.add_subplot(2, 2, 4))
    figure.tight_layout(pad=1.5)
    figure.savefig(OUTPUT_PATH, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {OUTPUT_PATH}")
    print(f"sampled areas: x {[round(section_area_x(v), 6) for v in (0.0, 1.0, 1.9)]}")
    print(f"sampled areas: y {[round(float(section_area_y(v)), 6) for v in (0.5, 2.0, 3.5)]}")
    print(f"sampled areas: z {[round(float(section_area_z(v)), 6) for v in (0.0, 1.0, 1.5)]}")


if __name__ == "__main__":
    main()
