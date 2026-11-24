"""Draw the two sections that the tutorial uses to bound the integral.

Panel one shows the section at the height y = 1.5, which is a rectangle.  Panel two shows the
section at the height z = 1.5, which is a triangle.  Both shapes come from the corner lists that
`part1_verify.py` prints.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from figure_support import assert_texts_inside_axes, save_figure
from geometry_anchors import DEMO_HEIGHT_Y, FIGURE_DPI, SHAPE_HEIGHTS_Z

FIGURE_DIRECTORY = Path(__file__).resolve().parent / "figures"
"""Directory that holds every rendered figure."""

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"
"""Directory that holds the JSON record of every part."""

FILL_ALPHA = 0.35
"""Opacity of the filled section."""

LABEL_FONT_SIZE = 11
"""Font size of every panel label."""

DEMO_HEIGHT_Z = 1.5
"""Height of the second section, which is the middle entry of the sampled heights of z."""


def load_rows() -> list[dict[str, str]]:
    """Return the six shape rows that the verification script of Part 1 writes."""
    record = json.loads((OUTPUT_DIRECTORY / "part1_values.json").read_text(encoding="utf-8"))
    return record["p1_shape_rows"]


def corners_of(row: dict[str, str]) -> np.ndarray:
    """Return the corner list of one shape row as an array of three coordinates.

    Args:
        row: One shape row of the record.
    """
    points = []
    for item in row["corners"].split(";"):
        triple = item.strip().strip("()").split(",")
        points.append([float(value) for value in triple])
    return np.array(points)


def find_row(rows: list[dict[str, str]], parameter: str, value: str) -> dict[str, str]:
    """Return the row of one parameter at one value.

    Args:
        rows: Every shape row of the record.
        parameter: Name of the parameter, which is y or z.
        value: Printed value of the parameter.
    """
    for row in rows:
        if row["parameter"] == parameter and row["value"] == value:
            return row
    raise KeyError(f"no shape row for {parameter} = {value}")


def main() -> None:
    """Draw the figure and write it to the figure directory."""
    rows = load_rows()
    if DEMO_HEIGHT_Z not in SHAPE_HEIGHTS_Z:
        raise AssertionError("the height of the second section is not a sampled height")
    row_y = find_row(rows, "y", f"{DEMO_HEIGHT_Y:.3f}")
    row_z = find_row(rows, "z", f"{DEMO_HEIGHT_Z:.3f}")
    figure, panels = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=FIGURE_DPI)

    corners_y = corners_of(row_y)
    panels[0].fill(corners_y[:, 0], corners_y[:, 2], color="#F58518", alpha=FILL_ALPHA)
    panels[0].plot(
        np.append(corners_y[:, 0], corners_y[0, 0]),
        np.append(corners_y[:, 2], corners_y[0, 2]),
        color="#B8540A",
        linewidth=1.8,
    )
    panels[0].set_xlabel(r"$x$")
    panels[0].set_ylabel(r"$z$")
    panels[0].set_title(rf"section at $y = {DEMO_HEIGHT_Y:.1f}$: a {row_y['kind']}", fontsize=LABEL_FONT_SIZE)
    text_first = panels[0].text(
        0.62, 1.60, f"area ${row_y['area']}$", fontsize=LABEL_FONT_SIZE
    )

    corners_z = corners_of(row_z)
    panels[1].fill(corners_z[:, 0], corners_z[:, 1], color="#54A24B", alpha=FILL_ALPHA)
    panels[1].plot(
        np.append(corners_z[:, 0], corners_z[0, 0]),
        np.append(corners_z[:, 1], corners_z[0, 1]),
        color="#2F6B2A",
        linewidth=1.8,
    )
    panels[1].set_xlabel(r"$x$")
    panels[1].set_ylabel(r"$y$")
    panels[1].set_title(rf"section at $z = {DEMO_HEIGHT_Z:.1f}$: a {row_z['kind']}", fontsize=LABEL_FONT_SIZE)
    text_second = panels[1].text(
        0.92, 0.45, f"area ${row_z['area']}$", fontsize=LABEL_FONT_SIZE
    )

    for panel in panels:
        panel.set_xlim(-0.12, 1.85)
        panel.set_ylim(-0.12, 3.15)
        panel.grid(alpha=0.25)
    panels[0].set_aspect("auto")
    panels[1].set_aspect("auto")
    assert_texts_inside_axes(figure, panels[0], [text_first], "part1_figure3 panel one")
    assert_texts_inside_axes(figure, panels[1], [text_second], "part1_figure3 panel two")
    figure.tight_layout()
    save_figure(figure, FIGURE_DIRECTORY / "part1_figure3.png")
    plt.close(figure)
    print(f"section at y = {DEMO_HEIGHT_Y:.1f}: {row_y['kind']} with area {row_y['area']}")
    print(f"section at z = {DEMO_HEIGHT_Z:.1f}: {row_z['kind']} with area {row_z['area']}")


if __name__ == "__main__":
    main()
