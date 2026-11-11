"""Draw the pyramid whose volume the given iterated integral measures.

The solid has the rectangular base [0, 1] x [0, 2] in the plane z = 0 and the apex
(0, 0, 1). The script drops the faces that turn away from the camera, marks the hidden
edge with dashes, and writes a PNG file with its Base64 copy.
"""

import base64

import matplotlib
import numpy as np
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Cambria", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 11,
    "axes.labelsize": 12,
})

ORIGIN = (0.0, 0.0, 0.0)
FRONT_RIGHT = (1.0, 0.0, 0.0)
BACK_RIGHT = (1.0, 2.0, 0.0)
BACK_LEFT = (0.0, 2.0, 0.0)
APEX = (0.0, 0.0, 1.0)

FACES = [
    ("base", [ORIGIN, FRONT_RIGHT, BACK_RIGHT, BACK_LEFT], "#cfbf9a"),
    ("wall", [ORIGIN, BACK_LEFT, APEX], "#8fb0c9"),
    ("front", [ORIGIN, FRONT_RIGHT, APEX], "#9dbb85"),
    ("slant", [FRONT_RIGHT, BACK_RIGHT, APEX], "#d79a72"),
    ("roof", [BACK_LEFT, BACK_RIGHT, APEX], "#b09ec9"),
]

ELEVATION = 32.0
AZIMUTH = -58.0
VIEW = np.array([
    np.cos(np.radians(ELEVATION)) * np.cos(np.radians(AZIMUTH)),
    np.cos(np.radians(ELEVATION)) * np.sin(np.radians(AZIMUTH)),
    np.sin(np.radians(ELEVATION)),
])
CENTER = np.mean([ORIGIN, FRONT_RIGHT, BACK_RIGHT, BACK_LEFT, APEX], axis=0)


def outward_normal(corners):
    """Return the unit normal of a face that points away from the center of the solid.

    Args:
        corners: The corner points of one face.

    Returns:
        Unit normal as a numpy array.
    """
    first, second, third = (np.array(corner) for corner in corners[:3])
    normal = np.cross(second - first, third - first)
    if np.dot(normal, first - CENTER) < 0.0:
        normal = -normal
    return normal / np.linalg.norm(normal)


figure = plt.figure(figsize=(7.4, 5.8))
axes = figure.add_axes([0.02, 0.02, 0.96, 0.92], projection="3d")
axes.computed_zorder = False

for name, corners, color in FACES:
    if np.dot(outward_normal(corners), VIEW) <= 0.0:
        continue
    patch = Poly3DCollection([corners], facecolors=[color], edgecolors="#2f3a44", linewidths=1.6)
    patch.set_zorder(2)
    axes.add_collection3d(patch)

axes.plot([BACK_LEFT[0], ORIGIN[0]], [BACK_LEFT[1], ORIGIN[1]], [BACK_LEFT[2], ORIGIN[2]],
          linestyle=(0, (4, 3)), color="#8a8a8a", linewidth=1.0, zorder=6)

label_box = {"facecolor": "white", "alpha": 0.9, "edgecolor": "none", "pad": 2.0}
axes.text(-0.20, -0.16, 1.02, r"$(0,0,1)$", color="#333333", fontsize=11, ha="center",
          bbox=label_box, zorder=20)

axes.set_xlabel(r"$x$", labelpad=2)
axes.set_ylabel(r"$y$", labelpad=2)
axes.set_zlabel(r"$z$", labelpad=0)
axes.set_xlim(-0.25, 1.30)
axes.set_ylim(-0.35, 2.45)
axes.set_zlim(-0.20, 1.35)
axes.set_box_aspect((1.05, 1.85, 1.15))
axes.view_init(elev=ELEVATION, azim=AZIMUTH)

axes.legend(
    handles=[
        Patch(facecolor="#cfbf9a", edgecolor="#5b7f94", label=r"base $z=0$, $0 \leq x \leq 1$, $0 \leq y \leq 2$"),
        Patch(facecolor="#9dbb85", edgecolor="#4d6b3c", label=r"face $y=0$"),
        Patch(facecolor="#d79a72", edgecolor="#8c4a24", label=r"face $x+z=1$"),
        Patch(facecolor="#b09ec9", edgecolor="#4a3f6b", label=r"face $y=2-2z$"),
    ],
    loc="upper left", framealpha=0.95, handlelength=1.4, borderpad=0.45, fontsize=10,
)

for axis in (axes.xaxis, axes.yaxis, axes.zaxis):
    axis.set_pane_color((0.97, 0.97, 0.95, 1.0))
    axis._axinfo["grid"]["color"] = (0.80, 0.80, 0.78, 1.0)

output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", pad_inches=0.06, facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")
