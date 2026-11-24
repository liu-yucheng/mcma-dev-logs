"""Draw Figure 1 of Part 3: the radial integrand and its cumulative integral.

The scaled volume integral reduces to $\\int_0^1 (1 - r^2) r^2 dr$ multiplied by the angular
factor. The left panel shows the integrand and the area under it. The right panel shows the
cumulative integral at the four radii 0.25, 0.5, 0.75, and 1.0. The script measures every
annotation against the drawn curve before the export.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

CODE_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIRECTORY))

import support

FIGURE_PATH = CODE_DIRECTORY / "figures" / "part3_figure1.png"
FILL_COLOUR = "#9dc3e6"
CURVE_COLOUR = "#1f4e79"
REFERENCE_COLOUR = "#808080"
MARKER_COLOUR = "#c0504d"
CLEARANCE = 6.0
SAMPLE_COUNT = 401
MARKER_RADII = (0.25, 0.5, 0.75, 1.0)


def radial_integrand(radius: float) -> float:
    """Return $(1 - r^2) r^2$, the integrand of the radial integral.

    Args:
        radius: Radial coordinate in [0, 1].

    Returns:
        The value of the integrand.
    """
    return (1.0 - radius * radius) * radius * radius


def main() -> None:
    """Draw both panels, check each annotation, and write the PNG."""
    radii = np.linspace(0.0, 1.0, SAMPLE_COUNT)
    values = np.array([radial_integrand(radius) for radius in radii])
    cumulative = np.array(support.cumulative_radial_integral(list(radii)))
    exact_integral = support.radial_integral_exact()
    marker_values = support.cumulative_radial_integral(list(MARKER_RADII))

    figure, panels = plt.subplots(1, 2, figsize=(7.6, 3.4), gridspec_kw={"wspace": 0.36})

    left = panels[0]
    left.fill_between(radii, values, color=FILL_COLOUR, alpha=0.75, linewidth=0.0)
    left.plot(radii, values, color=CURVE_COLOUR, linewidth=1.9)
    left.set_xlabel("$r$", fontsize=10.5)
    left.set_ylabel("$(1-r^2)\\,r^2$", fontsize=10.5)
    left.set_xlim(0.0, 1.0)
    left.set_ylim(0.0, 0.34)
    left.set_title("the radial integrand", fontsize=10.5)
    area_note = left.text(
        0.04,
        0.94,
        r"$\int_0^1(1-r^2)r^2\,dr=" + f"{exact_integral:.6f}$",
        transform=left.transAxes,
        fontsize=10.0,
        ha="left",
        va="top",
    )

    right = panels[1]
    right.plot(radii, cumulative, color=CURVE_COLOUR, linewidth=1.9)
    right.plot(MARKER_RADII, marker_values, linestyle="none", marker="o", markersize=4.5,
               markerfacecolor="white", markeredgecolor=MARKER_COLOUR, markeredgewidth=1.4)
    right.axhline(exact_integral, color=REFERENCE_COLOUR, linewidth=1.0, linestyle=(0, (1, 2)))
    right.set_xlabel("$r$", fontsize=10.5)
    right.set_ylabel(r"$\int_0^{r}(1-s^2)s^2\,ds$", fontsize=10.5)
    right.set_xlim(0.0, 1.12)
    right.set_ylim(0.0, 0.172)
    right.set_title("the cumulative integral", fontsize=10.5)
    label_offsets = ((-12.0, 14.0), (-12.0, 14.0), (-12.0, 14.0))
    marker_labels = [
        right.annotate(
            f"{value:.4f}",
            xy=(radius, value),
            xytext=offset,
            textcoords="offset points",
            fontsize=8.5,
            color=MARKER_COLOUR,
            ha="right",
            va="bottom",
        )
        for radius, value, offset in zip(MARKER_RADII[1:], marker_values[1:], label_offsets)
    ]

    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()

    def clearance(text, panel, curve_values: np.ndarray) -> float:
        """Return the smallest distance in pixels from a text box to a drawn curve."""
        box = text.get_window_extent(renderer)
        drawn = panel.transData.transform(np.column_stack([radii, curve_values]))
        corners = np.array([[box.x0, box.y0], [box.x1, box.y0],
                            [box.x0, box.y1], [box.x1, box.y1]])
        return float(np.min(np.linalg.norm(corners[:, None, :] - drawn[None, :, :], axis=2)))

    area_clearance = clearance(area_note, left, values)
    if area_clearance < CLEARANCE:
        raise AssertionError(f"the area note touches the curve: {area_clearance:.1f} px")
    box_axes = right.get_window_extent(renderer)
    for text in marker_labels:
        label_clearance = clearance(text, right, cumulative)
        if label_clearance < 11.0:
            raise AssertionError(f"the marker label {text.get_text()!r} touches the curve")
        label_box = text.get_window_extent(renderer)
        if (label_box.x0 < box_axes.x0 or label_box.x1 > box_axes.x1
                or label_box.y0 < box_axes.y0 or label_box.y1 > box_axes.y1):
            raise AssertionError(f"the marker label {text.get_text()!r} leaves the axes box")

    print(f"the radial integral from the antiderivative is {exact_integral!r}")
    print(f"the cumulative integral at r = 1 is {cumulative[-1]!r}")
    print("the cumulative values at r = 0.25, 0.5, 0.75, and 1.0 are "
          + ", ".join(f"{value:.6f}" for value in marker_values))
    print(f"the peak of the integrand is {float(values.max())!r} at r = {float(radii[int(np.argmax(values))])!r}")
    print(f"the smallest clearance of the area note is {area_clearance:.1f} pixels")
    if abs(cumulative[-1] - exact_integral) > 1.0e-9:
        raise AssertionError("the cumulative integral misses the exact value")
    if abs(float(values.max()) - 0.25) > 1.0e-6:
        raise AssertionError("the integrand peak is not one quarter")
    if abs(float(radii[int(np.argmax(values))]) - 1.0 / math.sqrt(2.0)) > 2.0e-3:
        raise AssertionError("the integrand peak is not at one over the square root of two")

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=200, bbox_inches="tight", pad_inches=0.04)
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
