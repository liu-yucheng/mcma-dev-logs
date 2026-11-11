"""Draw two meridians of the bumpy sphere against the unit circle.

At theta = pi/12 the factor sin(6 theta) equals 1, so the meridian reaches
rho = 1 + sin(5 phi)/5. At theta = pi/4 it equals minus 1, so the meridian
reaches rho = 1 - sin(5 phi)/5. Both are drawn in the plane y = 0.
"""

import base64
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_NAME = "part1_figure2"


def main():
    """Render the two meridians and write the two output files."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Cambria", "STIX Two Text", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "axes.linewidth": 0.7,
            "font.size": 11.5,
        }
    )

    polar = np.linspace(0.0, np.pi, 600)
    outer = 1.0 + 0.2 * np.sin(5.0 * polar)
    inner = 1.0 - 0.2 * np.sin(5.0 * polar)

    figure, axes = plt.subplots(figsize=(6.0, 5.0))
    axes.plot(np.sin(polar), np.cos(polar), color="#4a4a4a", linewidth=1.2,
              linestyle=(0, (5, 3)), label=r"unit sphere $\rho = 1$")
    axes.plot(outer * np.sin(polar), outer * np.cos(polar), color="#8a1c1c", linewidth=2.0,
              label=r"$\theta = \pi/12$, $\sin 6\theta = 1$")
    axes.plot(inner * np.sin(polar), inner * np.cos(polar), color="#3f6fa8", linewidth=2.0,
              label=r"$\theta = \pi/4$, $\sin 6\theta = -1$")

    axes.axhline(0.0, color="#9a9a9a", linewidth=0.6)
    axes.axvline(0.0, color="#9a9a9a", linewidth=0.6)

    axes.set_aspect("equal")
    axes.set_xlim(-1.4, 1.4)
    axes.set_ylim(-1.35, 1.35)
    axes.set_xlabel(r"$\rho\sin\phi$")
    axes.set_ylabel(r"$\rho\cos\phi$")
    axes.set_title("Two meridians of the bumpy sphere", fontsize=11.5)
    axes.grid(True, linewidth=0.4, alpha=0.45)
    axes.legend(loc="lower left", fontsize=9.0, frameon=False)

    figure.tight_layout()
    output = Path(__file__).with_name(FIGURE_NAME + ".png")
    figure.savefig(output, dpi=170)
    plt.close(figure)

    encoded = base64.b64encode(output.read_bytes()).decode("ascii")
    Path(__file__).with_name(FIGURE_NAME + ".b64.txt").write_text(encoded, encoding="ascii")
    print(f"saved {output.name} and {FIGURE_NAME}.b64.txt ({len(encoded)} base64 characters)")


if __name__ == "__main__":
    main()