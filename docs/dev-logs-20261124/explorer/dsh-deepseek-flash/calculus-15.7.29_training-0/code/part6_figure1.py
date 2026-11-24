"""Draw figure 1 of Part 6: the nesting of the six orders.

The figure is a workspace schematic. Each row is one order. The three columns give the
innermost integral, the middle integral, and the outermost integral, with the interval of the
variable of that integral. Every limit string is copied from the docstring of the matching
function of iteration_forms.py.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Path of the figure that this script writes.
FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part6_figure1.png"

# Resolution of the figure in dots per inch.
FIGURE_RESOLUTION = 150

# One entry for each order: the order label and the three interval strings, innermost first.
ORDER_TABLE = (
    ("$dy\\,dz\\,dx$",
     "$0 \\leq y \\leq 4 - x^{2} - 4z^{2}$",
     "$-\\sqrt{4 - x^{2}}/2 \\leq z \\leq \\sqrt{4 - x^{2}}/2$",
     "$-2 \\leq x \\leq 2$"),
    ("$dy\\,dx\\,dz$",
     "$0 \\leq y \\leq 4 - x^{2} - 4z^{2}$",
     "$-2\\sqrt{1 - z^{2}} \\leq x \\leq 2\\sqrt{1 - z^{2}}$",
     "$-1 \\leq z \\leq 1$"),
    ("$dz\\,dy\\,dx$",
     "$-\\sqrt{4 - x^{2} - y}/2 \\leq z \\leq \\sqrt{4 - x^{2} - y}/2$",
     "$0 \\leq y \\leq 4 - x^{2}$",
     "$-2 \\leq x \\leq 2$"),
    ("$dz\\,dx\\,dy$",
     "$-\\sqrt{4 - y - x^{2}}/2 \\leq z \\leq \\sqrt{4 - y - x^{2}}/2$",
     "$-\\sqrt{4 - y} \\leq x \\leq \\sqrt{4 - y}$",
     "$0 \\leq y \\leq 4$"),
    ("$dx\\,dz\\,dy$",
     "$-\\sqrt{4 - y - 4z^{2}} \\leq x \\leq \\sqrt{4 - y - 4z^{2}}$",
     "$-\\sqrt{4 - y}/2 \\leq z \\leq \\sqrt{4 - y}/2$",
     "$0 \\leq y \\leq 4$"),
    ("$dx\\,dy\\,dz$",
     "$-\\sqrt{4 - 4z^{2} - y} \\leq x \\leq \\sqrt{4 - 4z^{2} - y}$",
     "$0 \\leq y \\leq 4 - 4z^{2}$",
     "$-1 \\leq z \\leq 1$"),
)

# Colors of the three columns, from the innermost integral to the outermost integral.
COLUMN_COLORS = ("#1f3b57", "#4c78a8", "#9ecae1")

# Column headings.
COLUMN_HEADINGS = ("innermost", "middle", "outermost")

# Left edge, width, and font size of each column.
COLUMN_LEFT = (1.35, 5.25, 8.75)
COLUMN_WIDTH = (3.80, 3.40, 2.35)
COLUMN_FONT_SIZE = (7.3, 7.5, 8.6)


def main() -> None:
    """Draw the table and write the figure to the figures directory."""
    figure, axis = plt.subplots(figsize=(11.0, 4.6))
    axis.set_xlim(0.0, 12.0)
    axis.set_ylim(0.0, 7.0)
    axis.axis("off")
    for column_index, heading in enumerate(COLUMN_HEADINGS):
        center = COLUMN_LEFT[column_index] + COLUMN_WIDTH[column_index] / 2.0
        axis.text(center, 6.55, heading, fontsize=10, ha="center",
                  color=COLUMN_COLORS[column_index])
    for row_index, (label, inner, middle, outer) in enumerate(ORDER_TABLE):
        bottom = 5.85 - 0.95 * row_index
        axis.text(0.75, bottom + 0.30, label, fontsize=10, ha="center", va="center")
        for column_index, interval in enumerate((inner, middle, outer)):
            box = FancyBboxPatch(
                (COLUMN_LEFT[column_index], bottom),
                COLUMN_WIDTH[column_index],
                0.60,
                boxstyle="round,pad=0.02",
                linewidth=1.0,
                edgecolor=COLUMN_COLORS[column_index],
                facecolor=COLUMN_COLORS[column_index],
                alpha=0.12 + 0.10 * column_index,
            )
            axis.add_patch(box)
            axis.text(COLUMN_LEFT[column_index] + COLUMN_WIDTH[column_index] / 2.0, bottom + 0.30,
                      interval, fontsize=COLUMN_FONT_SIZE[column_index], ha="center", va="center",
                      color="#1f2933")
    axis.text(6.0, 0.20, "Each row is one iterated integral; each column is one integral of the nesting.",
              fontsize=9, ha="center", color="#52606d")
    figure.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=FIGURE_RESOLUTION, bbox_inches="tight")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")
    print(f"count of orders in the table = {len(ORDER_TABLE)}")


if __name__ == "__main__":
    main()
