"""Draw a vertical cross-section of the solid through the z axis.

The cross-section shows the two parabolic curves and the lens-shaped region
between them. The script saves the PNG and its Base64 copy.
"""

import base64
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_NAME = "part1_figure2"


def main():
    """Render the radial cross-section and write the two output files."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Cambria", "STIX Two Text", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "axes.linewidth": 0.7,
        }
    )

    rim = np.sqrt(5.0 / 2.0)
    radius = np.linspace(0.0, rim, 400)

    figure, axes = plt.subplots(figsize=(6.6, 4.6))
    axes.fill_between(
        radius, radius**2, 5.0 - radius**2, color="#cfddea", label="the solid $E$"
    )
    axes.plot(radius, radius**2, color="#3f6fa8", linewidth=1.9,
              label=r"$z = x^{2} + y^{2}$")
    axes.plot(radius, 5.0 - radius**2, color="#c0703f", linewidth=1.9,
              label=r"$z = 5 - x^{2} - y^{2}$")

    axes.plot([rim, rim], [0.0, 2.5], color="#1c1c1e", linewidth=1.0,
              linestyle="--")
    axes.plot([0.0, rim], [2.5, 2.5], color="#8a6d3b", linewidth=0.9,
              linestyle=":")
    axes.annotate(
        r"$r = \sqrt{5/2} \approx 1.581$",
        xy=(rim, 1.25), xytext=(rim - 0.62, 0.55),
        fontsize=9.5,
        arrowprops={"arrowstyle": "->", "linewidth": 0.8, "color": "#1c1c1e"},
    )
    axes.annotate(
        r"$z = 5$",
        xy=(0.0, 5.0), xytext=(0.18, 4.72), fontsize=9.5,
        arrowprops={"arrowstyle": "->", "linewidth": 0.8, "color": "#1c1c1e"},
    )
    axes.annotate(
        r"$z = 0$",
        xy=(0.0, 0.0), xytext=(0.18, 0.30), fontsize=9.5,
        arrowprops={"arrowstyle": "->", "linewidth": 0.8, "color": "#1c1c1e"},
    )
    axes.text(0.55, 2.62, r"rim height $z = 2.5$", fontsize=9.0, color="#6b5330")

    axes.set_xlim(0.0, 1.95)
    axes.set_ylim(0.0, 5.6)
    axes.set_xlabel(r"$r$ (distance from the $z$ axis)")
    axes.set_ylabel(r"$z$")
    axes.set_title("Vertical cross-section through the $z$ axis")
    axes.grid(True, linewidth=0.4, alpha=0.45)
    axes.legend(loc="upper right", fontsize=9, frameon=False)

    figure.tight_layout()
    output = Path(__file__).with_name(FIGURE_NAME + ".png")
    figure.savefig(output, dpi=170)
    plt.close(figure)

    encoded = base64.b64encode(output.read_bytes()).decode("ascii")
    Path(__file__).with_name(FIGURE_NAME + ".b64.txt").write_text(encoded, encoding="ascii")
    print(f"saved {output.name} and {FIGURE_NAME}.b64.txt ({len(encoded)} base64 characters)")


if __name__ == "__main__":
    main()
