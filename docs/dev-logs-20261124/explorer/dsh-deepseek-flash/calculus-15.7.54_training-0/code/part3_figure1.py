"""Draw Figure 3: the radial integrand of the triple integral.

The inner two integrals of the triple integral reduce the triple integral to the
one dimensional integral of g(r) = r^3 (1 - r^2)^2 / 2 on the unit interval. The
shaded area is 1/48 and the largest value of g is 0.0458 at r^2 = 3/7. The
script computes both numbers before it draws them.
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_NAME = "part3_figure1.png"
LABEL_FONT_SIZE = 11
TICK_FONT_SIZE = 10
TITLE_FONT_SIZE = 12
COLOR_CURVE = "#1f5f8b"
COLOR_FILL = "#9dc3e0"
COLOR_MARK = "#a02828"


def radial_integrand(radius_value: float) -> float:
    """Return g(r) = r^3 (1 - r^2)^2 / 2 for one radius value."""
    return radius_value**3 * (1.0 - radius_value**2) ** 2 / 2.0


def main() -> None:
    """Build the figure and write it beside the other figures of the session."""
    output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
    os.makedirs(output_directory, exist_ok=True)

    radius_values = np.linspace(0.0, 1.0, 600)
    integrand_values = radial_integrand(radius_values)
    trapezoid_area = float(np.trapezoid(integrand_values, radius_values))

    peak_radius_squared = 3.0 / 7.0
    peak_radius = float(np.sqrt(peak_radius_squared))
    peak_value = radial_integrand(peak_radius)
    grid_peak = float(radius_values[int(np.argmax(integrand_values))])

    print(f"computed shaded area = {trapezoid_area:.10f}, expected 1/48 = {1.0 / 48.0:.10f}")
    if abs(trapezoid_area - 1.0 / 48.0) > 5.0e-7:
        raise ValueError("the trapezoid area does not match one forty eighth")
    print(f"computed peak radius = {peak_radius:.10f}, grid peak radius = {grid_peak:.10f}")
    if abs(peak_radius - grid_peak) > 1.0e-2:
        raise ValueError("the closed form peak radius does not match the grid peak radius")
    print(f"computed peak value = {peak_value:.10f}")

    figure, axes = plt.subplots(figsize=(7.2, 4.4))
    axes.fill_between(radius_values, 0.0, integrand_values, color=COLOR_FILL, alpha=0.75)
    axes.plot(radius_values, integrand_values, color=COLOR_CURVE, linewidth=2.4)
    axes.plot(
        [peak_radius, peak_radius],
        [0.0, peak_value],
        color=COLOR_MARK,
        linewidth=1.0,
        linestyle=(0, (4, 3)),
    )
    axes.plot([peak_radius], [peak_value], marker="o", markersize=5.0, color=COLOR_MARK)

    axes.text(
        0.035,
        0.0475,
        "$g(r) = r^3 (1 - r^2)^2 / 2$",
        fontsize=LABEL_FONT_SIZE,
        color="#173a5c",
        ha="left",
    )
    axes.text(
        0.035,
        0.0335,
        "shaded area $= 1/48$",
        fontsize=LABEL_FONT_SIZE,
        color="#173a5c",
        ha="left",
    )
    axes.text(
        peak_radius + 0.035,
        peak_value - 0.0025,
        "$r^2 = 3/7$",
        fontsize=LABEL_FONT_SIZE - 1,
        color=COLOR_MARK,
        ha="left",
    )

    axes.set_xlim(0.0, 1.05)
    axes.set_ylim(0.0, 0.056)
    axes.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    axes.set_yticks([0.0, 0.02, 0.04])
    axes.tick_params(labelsize=TICK_FONT_SIZE)
    axes.set_xlabel("$r$", fontsize=LABEL_FONT_SIZE)
    axes.set_ylabel("$g(r)$", fontsize=LABEL_FONT_SIZE)
    axes.set_title("the radial integrand of the triple integral", fontsize=TITLE_FONT_SIZE, pad=8.0)
    for spine_name in ("top", "right"):
        axes.spines[spine_name].set_visible(False)

    figure.tight_layout(pad=0.8)
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    axes_box = axes.get_window_extent(renderer)
    for label in axes.texts:
        extent = label.get_window_extent(renderer)
        inside = (
            extent.x0 >= axes_box.x0
            and extent.x1 <= axes_box.x1
            and extent.y0 >= axes_box.y0
            and extent.y1 <= axes_box.y1
        )
        if not inside:
            raise ValueError(f"the label {label.get_text()!r} leaves the axes box")

    output_path = os.path.join(output_directory, FIGURE_NAME)
    figure.savefig(output_path, dpi=200)
    plt.close(figure)
    print("wrote", output_path)


if __name__ == "__main__":
    main()
