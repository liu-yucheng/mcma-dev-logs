"""Support the figures: a check that each text stays inside its axes, and a save helper."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Text

MINIMUM_TEXT_GAP_PIXELS = 2.0
"""Smallest accepted distance in pixels between two text boxes of one axes."""


def assert_texts_inside_axes(
    figure: Figure, axes: Axes, texts: Sequence[Text], figure_name: str
) -> None:
    """Check that every text box lies inside the axes box and clears its neighbours.

    Args:
        figure: Figure that holds the axes.
        axes: Axes that hold the texts.
        texts: Text artists to check.
        figure_name: Name of the figure, used in the error message.
    """
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    axes_box = axes.get_window_extent(renderer)
    boxes = [text.get_window_extent(renderer) for text in texts]
    for text, box in zip(texts, boxes):
        if not (
            box.x0 >= axes_box.x0 - 0.5
            and box.x1 <= axes_box.x1 + 0.5
            and box.y0 >= axes_box.y0 - 0.5
            and box.y1 <= axes_box.y1 + 0.5
        ):
            raise AssertionError(f"{figure_name}: text {text.get_text()!r} leaves the axes box")
    for first_index in range(len(boxes)):
        for second_index in range(first_index + 1, len(boxes)):
            first = boxes[first_index]
            second = boxes[second_index]
            horizontal_gap = max(second.x0 - first.x1, first.x0 - second.x1)
            vertical_gap = max(second.y0 - first.y1, first.y0 - second.y1)
            if horizontal_gap < MINIMUM_TEXT_GAP_PIXELS and vertical_gap < MINIMUM_TEXT_GAP_PIXELS:
                raise AssertionError(
                    f"{figure_name}: texts {texts[first_index].get_text()!r} and "
                    f"{texts[second_index].get_text()!r} touch each other"
                )
    print(f"[PASS] {figure_name}: {len(texts)} text boxes lie inside the axes and clear each other")


def save_figure(figure: Figure, path: Path) -> None:
    """Write one figure to one PNG file and print its size.

    Args:
        figure: Figure to write.
        path: Target PNG file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=figure.dpi, bbox_inches="tight", pad_inches=0.08)
    print(f"wrote {path} ({path.stat().st_size} bytes)")
