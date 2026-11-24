"""Draw the polar element of area in the unit disk.

The figure marks the element between the radii r and r + dr and between the angles theta and
theta + d(theta). The figure shows why the area element is r dr d(theta).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (the backend must be set first)

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part3_figure1.png"
"""Output path of the figure."""

INNER_RADIUS = 0.50
"""Inner radius of the drawn element."""

OUTER_RADIUS = 0.78
"""Outer radius of the drawn element."""

LOW_ANGLE = 0.50
"""Lower angle of the drawn element, in radians."""

HIGH_ANGLE = 1.05
"""Upper angle of the drawn element, in radians."""

LABEL_OFFSET = 0.055
"""Distance between a mark on the lower ray and its label."""


def main() -> None:
    """Build the figure and write it to the figures directory."""
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(figsize=(6.4, 6.4), constrained_layout=True)

    full_circle = np.linspace(0.0, 2.0 * np.pi, 500)
    axes.fill(np.cos(full_circle), np.sin(full_circle), color="#eef3f8", zorder=0)
    axes.plot(np.cos(full_circle), np.sin(full_circle), color="#111", linewidth=1.8, zorder=1)
    for radius in (INNER_RADIUS, OUTER_RADIUS):
        axes.plot(radius * np.cos(full_circle), radius * np.sin(full_circle), color="#8899aa",
                  linestyle="--", linewidth=0.9, zorder=2)

    element_angles = np.linspace(LOW_ANGLE, HIGH_ANGLE, 160)
    element_y = np.concatenate(
        [INNER_RADIUS * np.cos(element_angles), OUTER_RADIUS * np.cos(element_angles[::-1])]
    )
    element_z = np.concatenate(
        [INNER_RADIUS * np.sin(element_angles), OUTER_RADIUS * np.sin(element_angles[::-1])]
    )
    axes.fill(element_y, element_z, color="#f4c15d", alpha=0.95, zorder=4,
              label=r"$dA = r\,dr\,d\theta$")

    for angle in (LOW_ANGLE, HIGH_ANGLE):
        axes.plot([0.0, 1.14 * np.cos(angle)], [0.0, 1.14 * np.sin(angle)], color="#4a4a4a",
                  linewidth=1.1, zorder=3)

    # Tick marks on the lower ray, with a leader line to the name of each radius.
    for radius, label_angle, name in (
        (INNER_RADIUS, 0.24, r"$r$"),
        (OUTER_RADIUS, 0.34, r"$r + dr$"),
    ):
        tick = radius * np.array([np.cos(LOW_ANGLE), np.sin(LOW_ANGLE)])
        axes.plot([tick[0] - 0.028 * np.sin(LOW_ANGLE), tick[0] + 0.028 * np.sin(LOW_ANGLE)],
                  [tick[1] + 0.028 * np.cos(LOW_ANGLE), tick[1] - 0.028 * np.cos(LOW_ANGLE)],
                  color="#111", linewidth=1.4, zorder=5)
        anchor_radius = radius - 0.12
        anchor = anchor_radius * np.array([np.cos(label_angle), np.sin(label_angle)])
        axes.plot([tick[0], anchor[0]], [tick[1], anchor[1]], color="#111", linewidth=0.7,
                  linestyle=":", zorder=5)
        axes.text(anchor[0] + 0.02, anchor[1], name, fontsize=14, va="center", zorder=6)

    # The angle width d(theta), drawn as a small arc near the origin.
    angle_arc = np.linspace(LOW_ANGLE, HIGH_ANGLE, 80)
    axes.plot(0.30 * np.cos(angle_arc), 0.30 * np.sin(angle_arc), color="#8a2b2b", linewidth=1.6,
              zorder=5)
    axes.text(0.255, 0.215, r"$d\theta$", fontsize=14, color="#8a2b2b", zorder=6)

    axes.text(-1.10, -1.38, r"$D:\ y^2 + z^2 \leq 1$", fontsize=14, color="#1f4e79")
    axes.text(-1.10, 1.20, r"$dA = r\,dr\,d\theta$", fontsize=16)
    axes.set_aspect("equal")
    axes.set_xlim(-1.20, 1.30)
    axes.set_ylim(-1.46, 1.34)
    axes.set_xlabel(r"$y$")
    axes.set_ylabel(r"$z$")
    axes.set_title(r"The unit disk $D$ with one polar element")
    axes.grid(True, alpha=0.18)

    figure.savefig(FIGURE_PATH, dpi=170, facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
