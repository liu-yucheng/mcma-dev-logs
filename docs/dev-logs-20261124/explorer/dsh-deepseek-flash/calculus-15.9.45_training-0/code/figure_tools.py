"""Tools that close a figure: the label layout checks, the PNG file, and the layout record.

A label that leaves the axes box, that covers another label, or that sits on the stroke that it
names is a defect of the figure and not a matter of taste.  The functions here measure the window
extent of every text box, the display position of every anchor point, and the pixel distance of a
text box from the curve that carries the value that the text prints.
"""

import json
import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.axes
import matplotlib.figure
import matplotlib.text
import numpy as np
from mpl_toolkits.mplot3d import proj3d

FIGURE_DIRECTORY = pathlib.Path(__file__).resolve().parent / "figures"
"""Directory that holds the PNG file of each figure."""

OUTPUT_DIRECTORY = pathlib.Path(__file__).resolve().parent / "outputs"
"""Directory that holds the layout record of each figure."""

MINIMUM_MARGIN_PIXELS = 2.0
"""Smallest accepted distance between a text box and the edge of the axes box."""

MINIMUM_LEADER_GAP_PIXELS = 5.0
"""Smallest accepted distance between a text box and the anchor point that it names."""

TextBox = tuple[float, float, float, float]
"""Window extent of one text, as ``(x0, y0, x1, y1)`` in pixels."""


def text_boxes(
    figure: matplotlib.figure.Figure,
    texts: list[matplotlib.text.Text],
) -> list[tuple[matplotlib.text.Text, TextBox]]:
    """Return the window box of every text of a figure, after one draw.

    Args:
        figure: Figure that holds the texts.
        texts: Texts to measure.

    Returns:
        One pair of a text and its window extent for each text.
    """
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    boxes = []
    for text in texts:
        box = text.get_window_extent(renderer)
        boxes.append((text, (box.x0, box.y0, box.x1, box.y1)))
    return boxes


def overlap_area(first: TextBox, second: TextBox) -> float:
    """Return the area of the intersection of two window boxes.

    Args:
        first: First window extent.
        second: Second window extent.
    """
    width = min(first[2], second[2]) - max(first[0], second[0])
    height = min(first[3], second[3]) - max(first[1], second[1])
    if width <= 0.0 or height <= 0.0:
        return 0.0
    return float(width * height)


def box_distance(box: TextBox, point: tuple[float, float]) -> float:
    """Return the distance in pixels from one window box to one display point.

    Args:
        box: Window extent of a text.
        point: Display position of a point.
    """
    horizontal = max(box[0] - point[0], 0.0, point[0] - box[2])
    vertical = max(box[1] - point[1], 0.0, point[1] - box[3])
    return float(np.hypot(horizontal, vertical))


def project_point_3d(
    axes: matplotlib.axes.Axes,
    figure: matplotlib.figure.Figure,
    point: tuple[float, float, float],
) -> tuple[float, float]:
    """Return the display position of one point of a three dimensional axes.

    Args:
        axes: Three dimensional axes of the figure.
        figure: Figure that holds the axes.
        point: Data coordinates of the point.
    """
    figure.canvas.draw()
    projected = proj3d.proj_transform(point[0], point[1], point[2], axes.get_proj())
    display = axes.transData.transform((projected[0], projected[1]))
    return float(display[0]), float(display[1])


def axes_fraction(
    axes: matplotlib.axes.Axes,
    display_point: tuple[float, float],
) -> tuple[float, float]:
    """Return the axes fraction position of one display point.

    Args:
        axes: Axes that holds the point.
        display_point: Position of the point in display pixels.
    """
    return tuple(float(value) for value in axes.transAxes.inverted().transform(display_point))


def finish_figure(
    figure: matplotlib.figure.Figure,
    axes_list: list[matplotlib.axes.Axes],
    texts: list[matplotlib.text.Text],
    output_name: str,
    anchors: list[tuple[matplotlib.text.Text, tuple[float, float]]] | None = None,
    dpi: int = 200,
) -> dict[str, object]:
    """Check the label layout, write the PNG file, and write the layout record.

    Args:
        figure: Figure to close.
        axes_list: Every axes of the figure, each with its own box.
        texts: Every text of the figure that must stay readable.
        output_name: Name of the PNG file, without the extension.
        anchors: One pair of a text and the display point that its leader names.
        dpi: Resolution of the written PNG file.

    Returns:
        The layout record that the function also writes as a JSON file.

    Raises:
        ValueError: When a text box leaves the axes box, when two text boxes overlap, or when a
            text box sits closer than five pixels to the anchor point that it names.
    """
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    boxes = text_boxes(figure, texts)
    margins = []
    for text, box in boxes:
        best = -1.0e9
        for axes in axes_list:
            axes_box = axes.get_window_extent(renderer)
            best = max(best, min(
                box[0] - axes_box.x0,
                box[1] - axes_box.y0,
                axes_box.x1 - box[2],
                axes_box.y1 - box[3],
            ))
        margins.append(best)
        if best < MINIMUM_MARGIN_PIXELS:
            raise ValueError(f"label {text.get_text()!r} leaves the axes box: margin {best:.1f}")
    overlaps = []
    for index, (text, box) in enumerate(boxes):
        for other_text, other_box in boxes[index + 1:]:
            area = overlap_area(box, other_box)
            if area > 0.0:
                raise ValueError(
                    f"labels {text.get_text()!r} and {other_text.get_text()!r} overlap "
                    f"by {area:.1f} square pixels"
                )
            overlaps.append(area)
    gaps = []
    for text, point in anchors or []:
        box = dict((item.get_text(), item_box) for item, item_box in boxes)[text.get_text()]
        gap = box_distance(box, point)
        gaps.append(gap)
        if gap < MINIMUM_LEADER_GAP_PIXELS:
            raise ValueError(
                f"label {text.get_text()!r} sits {gap:.1f} pixels from the point that it names"
            )
    FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    png_path = FIGURE_DIRECTORY / f"{output_name}.png"
    figure.savefig(png_path, dpi=dpi, bbox_inches="tight", pad_inches=0.15)
    record = {
        "figure": output_name,
        "text_count": len(boxes),
        "minimum_margin_pixels": float(min(margins)),
        "maximum_overlap_square_pixels": float(max(overlaps)) if overlaps else 0.0,
        "minimum_leader_gap_pixels": float(min(gaps)) if gaps else None,
        "labels": [text.get_text() for text, _box in boxes],
        "png_path": str(png_path),
    }
    record_path = OUTPUT_DIRECTORY / f"layout_{output_name}.json"
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"{output_name}: {len(boxes)} labels, minimum margin "
          f"{record['minimum_margin_pixels']:.1f} px, maximum overlap "
          f"{record['maximum_overlap_square_pixels']:.1f} square px, minimum leader gap "
          f"{record['minimum_leader_gap_pixels']}", flush=True)
    return record
