"""Draw the wedge cut from the quarter cylinder by the planes x = y and x = 1.

The solid has five faces. The plane x = 1 and the plane x = y cut the quarter
cylinder y**2 + z**2 <= 1 into two quarter disks; the plane y = 0 and the plane z = 0
close the wedge. The faces are drawn in depth order for the camera of the figure.
The figure is stored as a PNG file and as a Base64 text file.
"""

import base64
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Cambria", "Times New Roman", "DejaVu Serif"]
plt.rcParams["mathtext.fontset"] = "stix"

OUTPUT_DIRECTORY = Path(__file__).resolve().parent
ELEVATION = 24.0
AZIMUTH = 65.0


def build_faces():
    """Return the five boundary faces as coordinate arrays with their colors."""

    angle = np.linspace(0.0, np.pi / 2.0, 120)
    radius = np.linspace(0.0, 1.0, 60)
    angle_grid, radius_grid = np.meshgrid(angle, radius)
    distance = np.linspace(0.0, 1.0, 60)
    angle_cylinder, distance_grid = np.meshgrid(angle, distance)
    cos_angle = np.cos(angle_cylinder)
    return {
        "wall": (np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 0.0, 1.0]]),
                 "#8fb0c9"),
        "base": (np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]]), "#cfbf9a"),
        "cap_right": (np.stack([np.ones_like(angle_grid),
                                radius_grid * np.cos(angle_grid),
                                radius_grid * np.sin(angle_grid)]), "#9dbb85"),
        "cap_slant": (np.stack([radius_grid * np.cos(angle_grid),
                                radius_grid * np.cos(angle_grid),
                                radius_grid * np.sin(angle_grid)]), "#d79a72"),
        "cylinder": (np.stack([cos_angle + distance_grid * (1.0 - cos_angle),
                               cos_angle,
                               np.sin(angle_cylinder)]), "#b09ec9"),
    }


figure = plt.figure(figsize=(7.0, 5.6))
axes = figure.add_axes([0.02, 0.02, 0.96, 0.92], projection="3d")
figure.patch.set_facecolor("white")
axes.computed_zorder = False

view_direction = np.array([
    np.cos(np.radians(ELEVATION)) * np.cos(np.radians(AZIMUTH)),
    np.cos(np.radians(ELEVATION)) * np.sin(np.radians(AZIMUTH)),
    np.sin(np.radians(ELEVATION)),
])
faces = build_faces()
centroids = {name: face[0].reshape(3, -1).mean(axis=1) for name, face in faces.items()}
for depth_rank, name in enumerate(sorted(faces, key=lambda key: float(centroids[key] @ view_direction))):
    coordinates, color = faces[name]
    if coordinates.ndim == 2:
        polygon = Poly3DCollection([coordinates.tolist()], facecolor=color, edgecolor="none",
                                   alpha=1.0, zorder=depth_rank + 1)
        axes.add_collection3d(polygon)
    else:
        axes.plot_surface(coordinates[0], coordinates[1], coordinates[2], color=color,
                          alpha=1.0, linewidth=0.0, antialiased=False, shade=False,
                          zorder=depth_rank + 1)

outline_color = "#1f2a33"
outline_width = 1.6
angle = np.linspace(0.0, np.pi / 2.0, 120)
for edge_x, edge_y, edge_z in [
    ([0.0, 1.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]),
    ([0.0, 0.0], [0.0, 0.0], [0.0, 1.0]),
    ([0.0, 1.0], [0.0, 0.0], [1.0, 1.0]),
    ([1.0, 1.0], [0.0, 0.0], [0.0, 1.0]),
    ([1.0, 1.0], [0.0, 1.0], [0.0, 0.0]),
]:
    axes.plot(edge_x, edge_y, edge_z, color=outline_color, linewidth=outline_width, zorder=20)
axes.plot(np.ones_like(angle), np.cos(angle), np.sin(angle), color=outline_color,
          linewidth=outline_width, zorder=20)
axes.plot(np.cos(angle), np.cos(angle), np.sin(angle), color=outline_color,
          linewidth=outline_width, zorder=20)

label_box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 1.5}
for text, position in [
    ("$x=1$", (1.0, 0.30, 0.28)),
    ("$x=y$", (0.45, 0.45, 0.42)),
    ("$y^2+z^2=1$", (0.44, 0.66, 0.90)),
]:
    axes.text(*position, text, fontsize=11, zorder=30, ha="center", va="center",
              bbox=label_box, color="#1f2a33")

axes.set_xlabel("$x$", fontsize=13, labelpad=9)
axes.set_ylabel("$y$", fontsize=13, labelpad=9)
axes.set_zlabel("$z$", fontsize=13, labelpad=9)
axes.set_xlim(0.0, 1.02)
axes.set_ylim(0.0, 1.02)
axes.set_zlim(0.0, 1.02)
axes.set_box_aspect((1.0, 1.0, 1.0))
axes.view_init(elev=ELEVATION, azim=AZIMUTH)
axes.tick_params(labelsize=10)

output_path = OUTPUT_DIRECTORY / "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
plt.close(figure)

encoded = base64.b64encode(output_path.read_bytes()).decode("ascii")
base64_path = OUTPUT_DIRECTORY / "part1_figure1.b64.txt"
base64_path.write_text(encoded, encoding="ascii")
print(f"saved {output_path.name} and {base64_path.name} ({len(encoded)} base64 characters)")
