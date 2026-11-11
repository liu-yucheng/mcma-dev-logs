"""Draw the two flat shadows that the six orders of integration read.

Panel (a) is the projection of E on the xy-plane.  Panel (b) is the base ellipse on the
xz-plane.  Each panel carries one sample strip with the limits that the strip defines.
The script writes part1_figure2.png and part1_figure2.b64.txt.

Usage:
    python part1_figure2.py
"""

import base64
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "stix",
    "axes.labelsize": 13,
    "font.size": 11.5,
})


def save(figure: plt.Figure, name: str) -> None:
    """Write the PNG file and its Base64 sidecar file.

    Args:
        figure: The matplotlib figure to save.
        name: The file name without extension.
    """
    png = Path(name + ".png")
    figure.savefig(png, dpi=170, bbox_inches="tight")
    text = base64.b64encode(png.read_bytes()).decode("ascii")
    Path(name + ".b64.txt").write_text(text, encoding="ascii")
    print(f"{png}: {png.stat().st_size} bytes, base64 length {len(text)}")


def main() -> None:
    """Build the figure and save it."""
    figure, (top_axes, bottom_axes) = plt.subplots(2, 1, figsize=(6.9, 7.6))

    x_values = np.linspace(-2.0, 2.0, 400)
    top = 4.0 - x_values**2
    top_axes.fill_between(x_values, 0.0, top, color="#b8cce0", alpha=0.75, zorder=1)
    top_axes.plot(x_values, top, color="#1f3b57", linewidth=2.0, zorder=2)
    top_axes.axhline(0.0, color="#1f3b57", linewidth=1.4)
    top_axes.axvline(0.0, color="0.55", linewidth=0.9, linestyle=":")

    strip_y = 1.5
    strip_x = np.sqrt(4.0 - strip_y)
    top_axes.annotate("", xy=(strip_x, strip_y), xytext=(-strip_x, strip_y),
                      arrowprops=dict(arrowstyle="<->", color="#a93226", linewidth=1.8))
    top_axes.plot([-strip_x, -strip_x], [0.0, strip_y], color="#a93226", linewidth=1.2, linestyle="--")
    top_axes.plot([strip_x, strip_x], [0.0, strip_y], color="#a93226", linewidth=1.2, linestyle="--")
    top_axes.text(0.0, strip_y + 0.60, r"strip at $y = 1.5$", ha="center", va="bottom",
                  color="#7b241c", fontsize=11)
    top_axes.text(0.0, strip_y + 0.34, r"$-\sqrt{4-y} \leq x \leq \sqrt{4-y}$", ha="center", va="bottom",
                  color="#7b241c", fontsize=11)
    top_axes.text(-1.92, 3.40, r"$0 \leq y \leq 4 - x^{2}$", color="#1f3b57", fontsize=11)
    top_axes.set_xlim(-2.35, 2.35)
    top_axes.set_ylim(-0.3, 4.9)
    top_axes.set_xlabel(r"$x$")
    top_axes.set_ylabel(r"$y$")
    top_axes.set_title(r"(a) projection of $E$ on the $xy$-plane", fontsize=12.5)
    top_axes.grid(True, color="0.9", linewidth=0.7)
    top_axes.set_axisbelow(True)

    angle = np.linspace(0.0, 2.0 * np.pi, 400)
    ellipse_x = 2.0 * np.cos(angle)
    ellipse_z = np.sin(angle)
    bottom_axes.fill(ellipse_x, ellipse_z, color="#cfe0c3", alpha=0.85, zorder=1)
    bottom_axes.plot(ellipse_x, ellipse_z, color="#2f5233", linewidth=2.0, zorder=2)
    bottom_axes.axhline(0.0, color="0.55", linewidth=0.9, linestyle=":")
    bottom_axes.axvline(0.0, color="0.55", linewidth=0.9, linestyle=":")

    fixed_z = 0.5
    half_x = 2.0 * np.sqrt(1.0 - fixed_z**2)
    bottom_axes.annotate("", xy=(half_x, fixed_z), xytext=(-half_x, fixed_z),
                         arrowprops=dict(arrowstyle="<->", color="#a93226", linewidth=1.8))
    bottom_axes.text(-0.85, 0.42, r"strip at $z = 0.5$", ha="center", va="top", color="#7b241c",
                     fontsize=10.5)
    bottom_axes.text(-0.85, 0.24, r"$|x| \leq 2\sqrt{1-z^{2}}$", ha="center", va="top", color="#7b241c",
                     fontsize=10.5)

    fixed_x = 1.2
    half_z = 0.5 * np.sqrt(4.0 - fixed_x**2)
    bottom_axes.annotate("", xy=(fixed_x, half_z), xytext=(fixed_x, -half_z),
                         arrowprops=dict(arrowstyle="<->", color="#1f4e79", linewidth=1.8))
    bottom_axes.text(1.38, -0.88, r"strip at $x = 1.2$", ha="left", va="top", color="#1f4e79",
                     fontsize=10.5)
    bottom_axes.text(1.38, -1.07, r"$|z| \leq \sqrt{4-x^{2}}/2$", ha="left", va="top", color="#1f4e79",
                     fontsize=10.5)

    bottom_axes.set_xlim(-2.55, 2.95)
    bottom_axes.set_ylim(-1.65, 1.62)
    bottom_axes.set_aspect("equal", adjustable="datalim")
    bottom_axes.set_xlabel(r"$x$")
    bottom_axes.set_ylabel(r"$z$")
    bottom_axes.set_title(r"(b) base ellipse $x^{2} + 4z^{2} \leq 4$", fontsize=12.5)
    bottom_axes.grid(True, color="0.9", linewidth=0.7)
    bottom_axes.set_axisbelow(True)

    figure.tight_layout(h_pad=1.6)
    save(figure, "part1_figure2")
    plt.close(figure)


if __name__ == "__main__":
    main()
