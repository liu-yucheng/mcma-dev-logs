"""Draw the two plane descriptions of the solid of Exercise 15.7.31.

The left panel shows the projection of the solid on the xy-plane: the
region x**2 <= y <= 4. The right panel shows the cross-section at a fixed
value of x: the triangle 0 <= z <= 2 - y/2 with x**2 <= y <= 4. The script
writes part1_figure2.png and its Base64 copy.
"""

import base64
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Cambria", "STIX Two Text", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "axes.labelsize": 13,
    "xtick.labelsize": 11.5,
    "ytick.labelsize": 11.5,
})

OUT = Path(__file__).resolve().parent


def draw_projection(ax):
    """Fill the region x**2 <= y <= 4 and mark two slices."""
    curve_x = np.linspace(-2.0, 2.0, 241)
    ax.fill_between(curve_x, curve_x**2, 4.0, color="#cfe3ee", edgecolor="none")
    ax.plot(curve_x, curve_x**2, color="#123c5a", lw=1.8)
    ax.plot([-2.0, 2.0], [4.0, 4.0], color="#123c5a", lw=1.8)
    for x_edge in (-2.0, 2.0):
        ax.plot([x_edge, x_edge], [x_edge**2, 4.0], color="#123c5a", lw=1.8)

    fixed_y = 2.2
    half = np.sqrt(fixed_y)
    ax.plot([-half, half], [fixed_y, fixed_y], color="#1f7a3d", lw=2.2)
    ax.annotate(r"fixed $y$", xy=(-half, fixed_y), xytext=(-2.95, 2.30),
                fontsize=11.5, color="#1f7a3d", ha="left",
                bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none", "pad": 1.5},
                arrowprops={"arrowstyle": "-", "color": "#1f7a3d", "lw": 0.9})

    fixed_x = 1.3
    ax.plot([fixed_x, fixed_x], [fixed_x**2, 4.0], color="#a8322a", lw=2.2)
    ax.annotate(r"fixed $x$", xy=(fixed_x, 3.05), xytext=(1.62, 3.30),
                fontsize=11.5, color="#a8322a", ha="left",
                bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none", "pad": 1.5},
                arrowprops={"arrowstyle": "-", "color": "#a8322a", "lw": 0.9})

    ax.set_xlim(-3.9, 3.0)
    ax.set_ylim(-0.4, 4.9)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.grid(color="#dddddd", lw=0.6)
    ax.set_axisbelow(True)
    ax.set_aspect("equal")
    ax.set_title(r"Projection on the $xy$-plane: $x^{2}\leq y\leq 4$", fontsize=12.5)


def draw_cross_section(ax):
    """Fill the trapezoid at x = 1 and mark two slices."""
    sample_x = 1.0
    left_y = sample_x**2
    ys = np.array([left_y, 4.0])
    ax.fill_between(ys, 0.0, 2.0 - ys / 2.0, color="#f0dcc0", edgecolor="none")
    ax.plot([left_y, 4.0], [2.0 - left_y / 2.0, 0.0], color="#6b3d0d", lw=1.8)
    ax.plot([left_y, 4.0], [0.0, 0.0], color="#123c5a", lw=1.8)
    ax.plot([left_y, left_y], [0.0, 2.0 - left_y / 2.0], color="#123c5a", lw=1.8)

    fixed_z = 0.5
    y_stop = 4.0 - 2.0 * fixed_z
    ax.plot([left_y, y_stop], [fixed_z, fixed_z], color="#1f7a3d", lw=2.2)
    ax.annotate(r"fixed $z$", xy=(y_stop, fixed_z), xytext=(3.22, 0.72),
                fontsize=11.5, color="#1f7a3d", ha="left",
                bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none", "pad": 1.5},
                arrowprops={"arrowstyle": "-", "color": "#1f7a3d", "lw": 0.9})

    fixed_y = 2.0
    ax.plot([fixed_y, fixed_y], [0.0, 2.0 - fixed_y / 2.0], color="#a8322a", lw=2.2)
    ax.annotate(r"fixed $y$", xy=(fixed_y, 1.0), xytext=(2.32, 1.12),
                fontsize=11.5, color="#a8322a", ha="left",
                bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none", "pad": 1.5},
                arrowprops={"arrowstyle": "-", "color": "#a8322a", "lw": 0.9})

    ax.annotate(r"$y=x^{2}=1$", xy=(left_y, 0.05), xytext=(0.15, -0.34),
                fontsize=11.5, color="#123c5a", ha="left",
                arrowprops={"arrowstyle": "-", "color": "#123c5a", "lw": 0.9})

    ax.set_xlim(-0.35, 5.0)
    ax.set_ylim(-0.75, 2.35)
    ax.set_xlabel(r"$y$")
    ax.set_ylabel(r"$z$")
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_yticks([0, 1, 2])
    ax.grid(color="#dddddd", lw=0.6)
    ax.set_axisbelow(True)
    ax.set_title(r"Cross-section at $x=1$: $1\leq y\leq 4$, $0\leq z\leq 2-y/2$",
                 fontsize=12.5)


def main():
    """Draw both panels and save the figure with its Base64 copy."""
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4))
    draw_projection(axes[0])
    draw_cross_section(axes[1])
    fig.tight_layout(pad=1.4)

    png_path = OUT / "part1_figure2.png"
    fig.savefig(png_path, dpi=170, bbox_inches="tight", facecolor="white")
    payload = write_base64(png_path)
    print(png_path)
    print(f"base64 length {len(payload)}")
    plt.close(fig)


def write_base64(path):
    """Write the Base64 text of the image and return it."""
    text = base64.b64encode(path.read_bytes()).decode("ascii")
    path.with_suffix(".b64.txt").write_text(text, encoding="ascii")
    return text


if __name__ == "__main__":
    main()