"""Draw the two dimensional figures of the tutorial and measure their labels.

The module gives every figure the same stroke colors and the same single mechanism
for an axis label: one arrow for the axis, and one letter beyond the arrow tip.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Text

FIGURE_DIRECTORY = Path(__file__).resolve().parent / "figures"

INK = "#35424d"
MUTED = "#57646f"
GUIDE = "#9aa6b1"
SPHERE_FILL = "#8fb3c9"
CYLINDER_FILL = "#d9b071"
SOLID_FILL = "#7e9db4"
CURVE_COLOR = "#b04a3f"
CELL_FILL = "#c0574e"

AXIS_LETTER_SIZE = 13.0
NOTE_SIZE = 9.5
TICK_SIZE = 9.0


def apply_style() -> None:
    """Set the font family and the math font of every figure of the tutorial."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Cambria", "STIXGeneral", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "font.size": 10.5,
            "axes.linewidth": 0.0,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def create_figure(width_inches: float, height_inches: float, title: str = "") -> Figure:
    """Create one empty figure with a white background.

    Args:
        width_inches: Width of the figure in inches.
        height_inches: Height of the figure in inches.
        title: Optional suptitle text.

    Returns:
        The figure.
    """
    apply_style()
    figure = plt.figure(figsize=(width_inches, height_inches))
    if title:
        figure.suptitle(title, fontsize=11.0, color=INK, y=0.985)
    return figure


def make_panel(
    figure: Figure,
    grid: tuple[int, int, int],
    x_limits: tuple[float, float],
    y_limits: tuple[float, float],
    panel_title: str = "",
) -> Axes:
    """Add one panel with equal aspect, hidden spines, and no automatic ticks.

    Args:
        figure: Figure that receives the panel.
        grid: Three values of the subplot grid: rows, columns, and the index.
        x_limits: Lower and upper limit of the horizontal coordinate.
        y_limits: Lower and upper limit of the vertical coordinate.
        panel_title: Title of the panel.

    Returns:
        The new axes.
    """
    axes = figure.add_subplot(grid[0], grid[1], grid[2])
    axes.set_xlim(*x_limits)
    axes.set_ylim(*y_limits)
    axes.set_aspect("equal", adjustable="box")
    for spine in axes.spines.values():
        spine.set_visible(False)
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_facecolor("white")
    if panel_title:
        axes.set_title(panel_title, fontsize=10.5, color=INK, pad=6.0)
    return axes


def draw_axis(axes: Axes, start: Sequence[float], end: Sequence[float]) -> None:
    """Draw one coordinate axis of a plane as an arrow.

    Args:
        axes: Panel that receives the arrow.
        start: Coordinates of the tail.
        end: Coordinates of the tip.
    """
    axes.annotate(
        "",
        xy=(end[0], end[1]),
        xytext=(start[0], start[1]),
        arrowprops={"arrowstyle": "-|>", "color": INK, "linewidth": 1.1, "mutation_scale": 9.0},
        zorder=20,
    )


def axis_letter(axes: Axes, letter: str, position: Sequence[float]) -> Text:
    """Place the one letter of one axis beyond the tip of its arrow.

    Args:
        axes: Panel that receives the letter.
        letter: Letter of the axis, for example ``$x$``.
        position: Coordinates of the letter.

    Returns:
        The text object.
    """
    return axes.text(
        position[0],
        position[1],
        letter,
        fontsize=AXIS_LETTER_SIZE,
        color=INK,
        ha="center",
        va="center",
        zorder=30,
    )


def draw_tick(axes: Axes, position: Sequence[float], offset: Sequence[float], label: str) -> Text:
    """Draw one tick of an axis with its numeric label.

    Args:
        axes: Panel that receives the tick.
        position: Coordinates of the tick on the axis.
        offset: Short vector from the axis to the outer end of the tick.
        label: Label of the tick.

    Returns:
        The text object of the label.
    """
    axes.plot(
        [position[0], position[0] + offset[0]],
        [position[1], position[1] + offset[1]],
        color=MUTED,
        linewidth=0.9,
        zorder=21,
    )
    return axes.text(
        position[0] + 1.9 * offset[0],
        position[1] + 1.9 * offset[1],
        label,
        fontsize=TICK_SIZE,
        color=MUTED,
        ha="center",
        va="center",
        zorder=28,
    )


def draw_note(axes: Axes, position: Sequence[float], text: str, alignment: str = "center") -> Text:
    """Place one explanatory text of a panel.

    Args:
        axes: Panel that receives the text.
        position: Coordinates of the text.
        text: The text.
        alignment: Horizontal alignment of the text.

    Returns:
        The text object.
    """
    return axes.text(
        position[0],
        position[1],
        text,
        fontsize=NOTE_SIZE,
        color=MUTED,
        ha=alignment,
        va="center",
        zorder=29,
    )


def draw_dot(axes: Axes, position: Sequence[float], size: float = 4.2) -> None:
    """Draw one marked point.

    Args:
        axes: Panel that receives the dot.
        position: Coordinates of the point.
        size: Marker size in points.
    """
    axes.plot([position[0]], [position[1]], marker="o", markersize=size, color=INK, zorder=25)


def save_figure(figure: Figure, file_name: str) -> Path:
    """Write one figure to the figure directory and report the path.

    Args:
        figure: Figure to write.
        file_name: Name of the portable network graphics file.

    Returns:
        The path of the written file.
    """
    FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    target = FIGURE_DIRECTORY / file_name
    figure.savefig(target, dpi=220, bbox_inches="tight", pad_inches=0.09)
    plt.close(figure)
    print(f"FIGURE {target}")
    return target


def measure_texts(figure: Figure, axes: Axes, texts: Iterable[Text]) -> list[float]:
    """Report how far each text stays inside its panel.

    Args:
        figure: Figure that holds the panel.
        axes: Panel that must contain the texts.
        texts: Text objects to measure.

    Returns:
        The distance in pixels from each text box to the nearest panel edge.
    """
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    axes_box = axes.get_window_extent(renderer)
    margins: list[float] = []
    for text in texts:
        box = text.get_window_extent(renderer)
        margin = min(
            box.x0 - axes_box.x0,
            axes_box.x1 - box.x1,
            box.y0 - axes_box.y0,
            axes_box.y1 - box.y1,
        )
        margins.append(margin)
        print(f"  label {text.get_text()!r}: margin={margin:.1f}px")
    return margins


def content_margins(figure: Figure, white_threshold: int = 245) -> dict[str, int]:
    """Report the empty band between the drawn content and each edge of the canvas.

    Args:
        figure: Figure to measure.
        white_threshold: A channel value at or above this threshold counts as blank.

    Returns:
        The margin in pixels of the left, right, bottom, and top edge.
    """
    figure.canvas.draw()
    buffer = np.asarray(figure.canvas.buffer_rgba())
    marked = np.any(buffer[:, :, :3] < white_threshold, axis=2)
    rows = np.where(marked.any(axis=1))[0]
    columns = np.where(marked.any(axis=0))[0]
    height, width = marked.shape
    margins = {
        "left": int(columns[0]),
        "right": int(width - 1 - columns[-1]),
        "bottom": int(height - 1 - rows[-1]),
        "top": int(rows[0]),
    }
    print(f"  content margins in pixels: {margins}")
    return margins
