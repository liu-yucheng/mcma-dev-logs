"""Figure 1 of Part 5: the convergence of the indicator quadrature.

The figure plots the error of the midpoint rule with the indicator of E against the number
of cells of one axis, on a logarithmic axis of the cell count. A dashed reference line with
the slope of a second order rule lies above the data with an offset, so the data curve never
reads as the reference line. A shaded band holds the error of the box quadrature.

Constants:
    REFERENCE_FACTOR: The vertical distance of the reference line above the data curve.
    REFERENCE_SLOPE: The slope of the reference line on the log-log axes.
    DATA_COLOR: The color of the data curve.
    REFERENCE_COLOR: The color of the reference line.
    BAND_COLOR: The color of the band of the box quadrature.
"""

import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import figure_common

REFERENCE_FACTOR = 3.0
REFERENCE_SLOPE = -2.0
DATA_COLOR = "#1f5fa8"
REFERENCE_COLOR = "#8c8c8c"
BAND_COLOR = "#f0c674"


def load_record(part_number):
    """Read the JSON record of one part.

    Args:
        part_number: The number of the part.

    Returns:
        The decoded record as a dictionary.
    """
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "outputs", "part%d_results.json" % part_number)
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


def main():
    """Draw the convergence, check each label, and write the PNG file."""
    record = load_record(5)
    values = record["values"]
    resolutions = sorted(int(key.split("_")[-1]) for key in values if key.startswith("riemann_error_"))
    errors = np.array([float(values["riemann_error_%d" % resolution]) for resolution in resolutions])
    counts = np.array(resolutions, dtype=float)

    figure, panel = plt.subplots(figsize=(7.2, 4.6))
    panel.set_xscale("log")
    panel.set_yscale("log")
    panel.set_xlabel("cells on one axis", fontsize=12)
    panel.set_ylabel("absolute error of the quadrature", fontsize=12)
    panel.set_xlim(12.0, 700.0)
    panel.set_xticks(list(counts))
    panel.set_xticklabels(["%d" % count for count in counts])

    reference = REFERENCE_FACTOR * errors[0] * (counts / counts[0]) ** REFERENCE_SLOPE
    reference_line = panel.plot(
        counts,
        reference,
        linestyle=(0, (5, 3)),
        color=REFERENCE_COLOR,
        linewidth=1.2,
        label="reference line with slope $-2$",
    )[0]
    data_line = panel.plot(
        counts,
        errors,
        color=DATA_COLOR,
        linewidth=1.6,
        marker="o",
        markersize=5.0,
        label="midpoint rule with the indicator of $E$",
    )[0]

    box_error = abs(float(values["monte_carlo"]) - float(values["exact_common"]))
    band = panel.axhspan(box_error / 1.6, box_error * 1.6, color=BAND_COLOR, alpha=0.45, linewidth=0.0)
    band_label = panel.text(
        float(counts[-1]),
        box_error * 1.75,
        "error of the box quadrature",
        fontsize=9.5,
        ha="right",
        va="bottom",
    )

    legend = panel.legend(handles=[data_line, reference_line], loc="lower left", fontsize=9.5, frameon=False)
    panel.spines["top"].set_visible(False)
    panel.spines["right"].set_visible(False)

    figure.tight_layout()
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    box = figure_common.axes_box(panel, figure)
    assert figure_common.is_inside(figure_common.extent_of(legend, figure), box, margin=0.5), "legend leaves the axes"
    assert figure_common.is_inside(figure_common.extent_of(band_label, figure), box, margin=0.5), "band label leaves the axes"
    assert figure_common.is_inside(figure_common.extent_of(data_line, figure), box, margin=0.5), "data curve leaves the axes"

    path = figure_common.save_figure(figure, "part5_figure1.png")
    print("figure written: %s" % path)
    print("errors: %s" % ", ".join("%d: %.6g" % (int(count), error) for count, error in zip(counts, errors)))
    print("box quadrature error: %.6g" % box_error)


if __name__ == "__main__":
    main()
