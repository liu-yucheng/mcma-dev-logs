"""Draw Figure 3: one horizontal slice divided into rings, and the slice moment as a curve.

The left panel shows the slice at height z0 with one highlighted ring of radius r and width
dr. The right panel shows the second moment pi*z^4/2 of the slice at height z. The shaded
area under the curve is the integral that gives the moment of inertia about the z axis. The
script asserts that each text box and each legend lie inside its axes box before it writes
the PNG file.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import importlib.metadata
import platform

HEIGHT = 1.0
"""The height h of the cone."""

SLICE_HEIGHT = 0.62
"""The height z0 of the slice that the left panel draws."""

RING_RADIUS = 0.36
"""The inner radius r of the highlighted ring."""

RING_WIDTH = 0.07
"""The width dr of the highlighted ring."""

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part4_figure1.png"
"""The output path of the figure."""


def slice_second_moment(height: np.ndarray) -> np.ndarray:
    """Return the second moment of the disk at the given heights.

    Args:
        height: The array of heights z.

    Returns:
        The array of second moments pi*z^4/2 of the disk of radius z.
    """
    return np.pi * height ** 4 / 2.0


def inside_axes(axes: plt.Axes, artist: object, renderer: object) -> bool:
    """Return True when the drawn box of an artist lies inside the axes box.

    Args:
        axes: The axes that holds the artist.
        artist: The artist, such as a text or a legend.
        renderer: The renderer of the canvas.

    Returns:
        True when the drawn box lies fully inside the axes box.
    """
    box = artist.get_window_extent(renderer=renderer)
    return bool(
        box.x0 >= axes.bbox.x0
        and box.y0 >= axes.bbox.y0
        and box.x1 <= axes.bbox.x1
        and box.y1 <= axes.bbox.y1
    )


def draw_slice_panel(axes: plt.Axes, label_box: dict[str, object]) -> list[plt.Text]:
    """Draw the slice at height z0 with one highlighted ring.

    Args:
        axes: The axes of the left panel.
        label_box: The style of the white box behind each label.

    Returns:
        The list of the text objects of the panel.
    """
    angle = np.linspace(0.0, 2.0 * np.pi, 361)
    axes.fill(SLICE_HEIGHT * np.cos(angle), SLICE_HEIGHT * np.sin(angle), color="#f0c9b4",
              alpha=0.75, zorder=1)
    for radius in (0.15, 0.30, 0.48, 0.54):
        axes.plot(SLICE_HEIGHT * radius / 0.62 * np.cos(angle),
                  SLICE_HEIGHT * radius / 0.62 * np.sin(angle),
                  color="#c58a72", linewidth=0.7, linestyle=":", zorder=2)
    ring_angle = np.linspace(0.0, 2.0 * np.pi, 361)
    inner_x, inner_y = RING_RADIUS * np.cos(ring_angle), RING_RADIUS * np.sin(ring_angle)
    outer_radius = RING_RADIUS + RING_WIDTH
    outer_x, outer_y = outer_radius * np.cos(ring_angle), outer_radius * np.sin(ring_angle)
    ring_x = np.concatenate([inner_x, outer_x[::-1]])
    ring_y = np.concatenate([inner_y, outer_y[::-1]])
    axes.fill(ring_x, ring_y, color="#1f4e79", alpha=0.45, zorder=3)
    axes.plot(inner_x, inner_y, color="#1f4e79", linewidth=0.9, zorder=4)
    axes.plot(outer_x, outer_y, color="#1f4e79", linewidth=0.9, zorder=4)
    axes.plot(SLICE_HEIGHT * np.cos(angle), SLICE_HEIGHT * np.sin(angle), color="#8c2f1e",
              linewidth=2.2, zorder=4)
    axes.annotate("", xy=(RING_RADIUS, 0.0), xytext=(0.0, 0.0),
                  arrowprops={"arrowstyle": "->", "color": "#1f4e79", "shrinkA": 0.0,
                              "shrinkB": 3.0, "linewidth": 1.2}, zorder=7)
    axes.plot([0.0, SLICE_HEIGHT], [0.0, 0.0], color="#8c8c8c", linewidth=0.9,
              linestyle=":", zorder=2)

    axes.plot([0.60 * SLICE_HEIGHT, 0.86 * SLICE_HEIGHT],
              [0.42 * SLICE_HEIGHT, 0.62 * SLICE_HEIGHT], color="#5a6b7d", linewidth=0.8,
              zorder=9)
    axes.plot([RING_RADIUS + 0.24, 0.80 * SLICE_HEIGHT],
              [-0.52 * SLICE_HEIGHT, -0.62 * SLICE_HEIGHT], color="#5a6b7d", linewidth=0.8,
              zorder=9)

    axes.set_xlim(-1.12 * SLICE_HEIGHT, 1.32 * SLICE_HEIGHT)
    axes.set_ylim(-1.12 * SLICE_HEIGHT, 1.18 * SLICE_HEIGHT)
    axes.set_aspect("equal")
    axes.set_xticks([-SLICE_HEIGHT, 0.0, SLICE_HEIGHT])
    axes.set_yticks([-SLICE_HEIGHT, 0.0, SLICE_HEIGHT])
    axes.set_xticklabels([r"$-z_0$", r"$0$", r"$z_0$"], fontsize=9.5)
    axes.set_yticklabels([r"$-z_0$", r"$0$", r"$z_0$"], fontsize=9.5)
    axes.set_xlabel("$x$", fontsize=11)
    axes.set_ylabel("$y$", fontsize=11)
    axes.set_title(r"The slice at $z=z_0$, cut into rings", fontsize=11)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)

    return [
        axes.text(0.90 * SLICE_HEIGHT, 0.70 * SLICE_HEIGHT, "the slice\n" r"$z=z_0$",
                  fontsize=9.0, color="#8c2f1e", ha="center", va="center", bbox=label_box,
                  zorder=10),
        axes.text(0.68 * SLICE_HEIGHT, -0.78 * SLICE_HEIGHT,
                  "one ring: radius $r$,\nwidth $dr$", fontsize=9.0, color="#1f4e79",
                  ha="center", va="center", bbox=label_box, zorder=10),
        axes.text(0.0, 0.10 * SLICE_HEIGHT, r"$r$", fontsize=9.5, color="#1f4e79",
                  ha="center", va="bottom", zorder=10),
    ]


def report_environment() -> None:
    """Print the version of each tool, so that the figure repeats."""
    package_names = ("numpy", "matplotlib")
    versions = ", ".join(
        f"{name} {importlib.metadata.version(name)}" for name in package_names
    )
    print(f"Python {platform.python_version()}, {versions}")


def main() -> None:
    """Draw the figure, check the label positions, and write the PNG file."""
    report_environment()
    figure, (left, right) = plt.subplots(1, 2, figsize=(11.0, 5.2))
    label_box = {"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "#c8ccd2",
                 "alpha": 0.94}

    annotations_left = draw_slice_panel(left, label_box)

    height_values = np.linspace(0.0, HEIGHT, 400)
    moment_values = slice_second_moment(height_values)
    maximum_moment = float(slice_second_moment(np.array(HEIGHT)))
    slice_moment = float(slice_second_moment(np.array(SLICE_HEIGHT)))
    right.fill_between(height_values, 0.0, moment_values, color="#a9cbe8", alpha=0.6,
                       zorder=1)
    right.plot(height_values, moment_values, color="#1f4e79", linewidth=2.2, zorder=3,
               label=r"$J(z)=\frac{\pi z^{4}}{2}$")
    right.plot([SLICE_HEIGHT, SLICE_HEIGHT], [0.0, slice_moment], color="#b5432f",
               linewidth=1.4, linestyle="--", zorder=4)
    right.plot([SLICE_HEIGHT], [slice_moment], marker="o", markersize=5.5, color="#b5432f",
               zorder=6, label=r"$J(z_0)=\frac{\pi z_0^{4}}{2}$")
    right.set_xlim(0.0, 1.05 * HEIGHT)
    right.set_ylim(0.0, 1.05 * maximum_moment)
    right.set_xticks([0.0, SLICE_HEIGHT, HEIGHT])
    right.set_xticklabels([r"$0$", r"$z_0$", r"$h$"], fontsize=9.5)
    right.set_yticks([0.0, 0.5 * maximum_moment, maximum_moment])
    right.set_yticklabels([r"$0$", r"$\frac{\pi h^{4}}{4}$", r"$\frac{\pi h^{4}}{2}$"],
                          fontsize=9.5)
    right.set_xlabel("$z$, the height of the slice", fontsize=11)
    right.set_ylabel("second moment of the slice", fontsize=11)
    right.set_title(r"Stack the slices: $I_z=\int_0^{h} k\,J(z)\,dz$", fontsize=11)
    right.grid(True, color="#dfe3e8", linewidth=0.7, zorder=0)
    right.set_axisbelow(True)
    right.spines["top"].set_visible(False)
    right.spines["right"].set_visible(False)
    right.legend(loc="upper left", fontsize=9.2, framealpha=0.95)

    annotations_right = [
        right.text(0.46 * HEIGHT, 0.62 * maximum_moment,
                   "area $=\\int_0^{h} k\\,J(z)\\,dz$", fontsize=9.5, color="#1f4e79",
                   ha="left", va="center", bbox=label_box, zorder=10),
    ]
    right.annotate("", xy=(0.82 * HEIGHT, 0.36 * maximum_moment),
                   xytext=(0.82 * HEIGHT, 0.50 * maximum_moment),
                   arrowprops={"arrowstyle": "-|>", "color": "#1f4e79", "shrinkA": 2.0,
                               "shrinkB": 2.0, "linewidth": 1.0}, zorder=9)

    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    for axes, annotations in ((left, annotations_left), (right, annotations_right)):
        for index, text in enumerate(annotations, start=1):
            inside = inside_axes(axes, text, renderer)
            print(f"annotation {index} inside its axes box: computed = {inside}, "
                  f"expected = True")
            assert inside, f"the annotation {index} leaves its axes box"
        legend = axes.get_legend()
        if legend is not None:
            inside_legend = inside_axes(axes, legend, renderer)
            print(f"legend inside its axes box: computed = {inside_legend}, expected = True")
            assert inside_legend, "the legend leaves its axes box"

    print(f"ring area formula: 2*pi*r*dr = "
          f"{2.0 * np.pi * RING_RADIUS * RING_WIDTH:.6f}, "
          f"drawn area = {np.pi * ((RING_RADIUS + RING_WIDTH) ** 2 - RING_RADIUS ** 2):.6f}")
    print(f"slice second moment at z = {SLICE_HEIGHT:.4f}: {slice_moment:.6f}")
    print(f"slice second moment at z = {HEIGHT:.4f}: {maximum_moment:.6f}")

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=200, bbox_inches="tight")
    print(f"figure written: {FIGURE_PATH}")


if __name__ == "__main__":
    main()
