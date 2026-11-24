"""Tools that close a figure: label layout checks, the PNG file, and a layout record."""

import json
import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.figure
import matplotlib.text
import matplotlib.axes

FIGURE_DIRECTORY = pathlib.Path(__file__).resolve().parent / "figures"
"""Directory that holds the PNG file of each figure."""

OUTPUT_DIRECTORY = pathlib.Path(__file__).resolve().parent / "outputs"
"""Directory that holds the layout record of each figure."""

MINIMUM_MARGIN_PIXELS = 2.0
"""Smallest accepted distance between a text box and the edge of the axes box."""


def text_boxes(
    figure: matplotlib.figure.Figure,
    texts: list[matplotlib.text.Text],
) -> list[tuple[matplotlib.text.Text, tuple[float, float, float, float]]]:
    """Return the window box of every text of a figure, after one draw."""
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    boxes = []
    for text in texts:
        box = text.get_window_extent(renderer)
        boxes.append((text, (box.x0, box.y0, box.x1, box.y1)))
    return boxes


def overlap_area(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float],
) -> float:
    """Return the area of the intersection of two window boxes."""
    width = min(first[2], second[2]) - max(first[0], second[0])
    height = min(first[3], second[3]) - max(first[1], second[1])
    if width <= 0.0 or height <= 0.0:
        return 0.0
    return float(width * height)


def finish_figure(
    figure: matplotlib.figure.Figure,
    axes: matplotlib.axes.Axes,
    texts: list[matplotlib.text.Text],
    output_name: str,
    dpi: int = 200,
) -> dict[str, object]:
    """Check the label layout, write the PNG file, and write the layout record.

    The function raises an error when a text box leaves the axes box or when two text boxes
    overlap, because a label that leaves the box or covers another label is a defect of the
    figure and not a matter of taste.
    """
    figure.canvas.draw()
    axes_box = axes.get_window_extent(figure.canvas.get_renderer())
    boxes = text_boxes(figure, texts)
    margins = []
    overlaps = []
    for index, (text, box) in enumerate(boxes):
        margin = min(
            box[0] - axes_box.x0,
            box[1] - axes_box.y0,
            axes_box.x1 - box[2],
            axes_box.y1 - box[3],
        )
        margins.append(margin)
        if margin < MINIMUM_MARGIN_PIXELS:
            raise ValueError(f"label {text.get_text()!r} leaves the axes box: margin {margin:.1f}")
        for other_text, other_box in boxes[index + 1:]:
            area = overlap_area(box, other_box)
            if area > 0.0:
                raise ValueError(
                    f"labels {text.get_text()!r} and {other_text.get_text()!r} overlap "
                    f"by {area:.1f} square pixels"
                )
            overlaps.append(area)
    FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    png_path = FIGURE_DIRECTORY / f"{output_name}.png"
    figure.savefig(png_path, dpi=dpi, bbox_inches="tight", pad_inches=0.15)
    record = {
        "figure": output_name,
        "text_count": len(boxes),
        "minimum_margin_pixels": float(min(margins)),
        "maximum_overlap_square_pixels": float(max(overlaps)) if overlaps else 0.0,
        "labels": [text.get_text() for text, _box in boxes],
        "png_path": str(png_path),
    }
    record_path = OUTPUT_DIRECTORY / f"layout_{output_name}.json"
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"{output_name}: {len(boxes)} labels, minimum margin "
          f"{record['minimum_margin_pixels']:.1f} px, maximum overlap "
          f"{record['maximum_overlap_square_pixels']:.1f} square px")
    return record
