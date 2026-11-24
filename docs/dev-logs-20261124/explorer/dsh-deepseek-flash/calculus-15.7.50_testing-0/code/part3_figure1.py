"""Draw a sample of the solid E, coloured by the density, with the center of mass marked.

The sample is uniform on the box 0 <= x <= 1, 0 <= y <= 3, 0 <= z <= 3, and the script keeps the points
that satisfy the three defining inequalities of E. The center of mass comes from the print of
code/part3_verify.py and the script checks that the marker lies inside the extent of the sample.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors

OUTPUT_PATH = Path(__file__).resolve().parent / "figures" / "part3_figure1.png"
RESULTS_PATH = Path(__file__).resolve().parent / "outputs" / "part3_results.json"
SAMPLE_COUNT = 20000
MARKER_BOX = {"facecolor": "white", "edgecolor": "#333333", "linewidth": 0.5, "alpha": 0.92,
              "pad": 2.5}


def main() -> None:
    """Draw the figure, check the marker, and write the PNG file."""
    generator = np.random.default_rng(figure_anchors.MONTE_CARLO_SEED)
    sample = generator.uniform(size=(SAMPLE_COUNT, 3))
    sample[:, 1] *= 3.0
    sample[:, 2] *= 3.0
    inside = (sample[:, 1] <= 3.0) & (sample[:, 2] <= np.sqrt(np.maximum(
        0.0, 9.0 - sample[:, 1] ** 2))) & (sample[:, 0] <= sample[:, 1] / 3.0)
    points = sample[inside]
    density = points[:, 0] ** 2 + points[:, 1] ** 2
    output_directory = Path(__file__).resolve().parent / "outputs"
    output_directory.mkdir(parents=True, exist_ok=True)
    (output_directory / "part3_figure1_results.json").write_text(
        json.dumps({
            "sample_points_attempted": f"{SAMPLE_COUNT:d}",
            "sample_points_kept": f"{points.shape[0]:d}",
        }, indent=2, sort_keys=True) + chr(10), encoding="utf-8")
    print(f"kept {points.shape[0]} of {SAMPLE_COUNT} sample points,"
          f" density from {density.min():.4f} to {density.max():.4f}")
    print(f"sample extent x {points[:, 0].min():.4f} to {points[:, 0].max():.4f},"
          f" y {points[:, 1].min():.4f} to {points[:, 1].max():.4f},"
          f" z {points[:, 2].min():.4f} to {points[:, 2].max():.4f}")

    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    center = (float(results["x_bar"]), float(results["y_bar"]), float(results["z_bar"]))
    print(f"center of mass from code/part3_verify.py: ({center[0]:.6f}, {center[1]:.6f},"
          f" {center[2]:.6f})")

    figure = plt.figure(figsize=(7.6, 6.6))
    axes = figure.add_subplot(111, projection="3d")
    coloured = axes.scatter(points[:, 0], points[:, 1], points[:, 2], c=density, cmap="viridis",
                            s=5, alpha=0.45, linewidth=0.0)
    colour_bar = figure.colorbar(coloured, ax=axes, shrink=0.62, pad=0.10)
    colour_bar.set_label(r"density $\rho = x^{2} + y^{2}$", fontsize=10)
    axes.scatter([center[0]], [center[1]], [center[2]], marker="*", s=340, color="#c44e52",
                 edgecolor="#7d2b2f", linewidth=0.8, zorder=30)
    axes.text(center[0] + 0.06, center[1] - 0.55, center[2] + 0.42,
              r"center of mass" "\n" rf"$({center[0]:.3f},\ {center[1]:.3f},\ {center[2]:.3f})$",
              fontsize=10, color="#111111", bbox=MARKER_BOX, zorder=40)
    axes.set_xlabel(r"$x$", labelpad=8)
    axes.set_ylabel(r"$y$", labelpad=10)
    axes.set_zlabel(r"$z$", labelpad=10)
    axes.set_xlim(0.0, 1.25)
    axes.set_ylim(0.0, 3.2)
    axes.set_zlim(0.0, 3.2)
    axes.set_box_aspect((1.0, 1.0, 1.0), zoom=0.88)
    axes.view_init(elev=20.0, azim=-58.0)
    axes.set_title(r"Points of $E$ coloured by the density, with the center of mass", fontsize=11)

    for axis_name, low, high, value in (
        ("x", 0.0, 1.25, center[0]),
        ("y", 0.0, 3.2, center[1]),
        ("z", 0.0, 3.2, center[2]),
    ):
        inside_limit = low + 0.02 * (high - low) <= value <= high - 0.02 * (high - low)
        print(f"center of mass coordinate {axis_name} = {value:.3f} inside the limits ="
              f" {inside_limit}")
        assert inside_limit, f"the center of mass leaves the axes limits in {axis_name}"

    for index, axis_name in enumerate(("x", "y", "z")):
        low = float(points[:, index].min())
        high = float(points[:, index].max())
        print(f"center of mass {axis_name} = {center[index]:.6f} inside the sample extent"
              f" [{low:.4f}, {high:.4f}] = {low <= center[index] <= high}")
        assert low <= center[index] <= high, f"the center of mass leaves the sample in {axis_name}"

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PATH, dpi=170, bbox_inches="tight")
    image = plt.imread(OUTPUT_PATH)
    border = np.concatenate([image[0, :, :3].ravel(), image[-1, :, :3].ravel(),
                             image[:, 0, :3].ravel(), image[:, -1, :3].ravel()])
    print(f"saved image {image.shape[1]} x {image.shape[0]} pixels,"
          f" smallest border value = {border.min():.3f}")
    assert border.min() >= 0.90, "a drawn element touches the border of the saved image"
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
