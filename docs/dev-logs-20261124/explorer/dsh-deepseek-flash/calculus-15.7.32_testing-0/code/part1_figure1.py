"""Figure 1 of Part 1: the solid E drawn as a tetrahedron.

The figure draws the four faces with an opacity above one half, names each face at a point
that its own equation satisfies, and names each vertex at a point outside the solid that a
short leader joins to the vertex.

Constants:
    VERTICES: The four vertices of E with their names.
    FACES: The four faces, each with its three vertices, its equation, and its shade.
    AXES_LIMIT: The extent of each horizontal axis of the drawing.
    HEIGHT_LIMIT: The extent of the vertical axis of the drawing.
    VIEW_ELEVATION: The elevation of the camera in degrees.
    VIEW_AZIMUTH: The azimuth of the camera in degrees.
    VERTEX_OFFSET: The distance of a vertex label from its vertex.
    VERTEX_DIRECTIONS: The direction of each vertex label, away from the solid.
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import figure_common

VERTICES = {
    "A": (2.0, 2.0, 0.0),
    "B": (2.0, 2.0, 1.0),
    "C": (2.0, 0.0, 0.0),
    "D": (0.0, 2.0, 0.0),
}

FACES = [
    (("A", "C", "D"), "$z = 0$", "#7fa8d0"),
    (("A", "B", "C"), "$x = 2$", "#e8a95c"),
    (("A", "B", "D"), "$y = 2$", "#7fbf7b"),
    (("B", "C", "D"), "$x + y - 2z = 2$", "#c48bb4"),
]

AXES_LIMIT = 2.9
HEIGHT_LIMIT = 1.8
VIEW_ELEVATION = 17.0
VIEW_AZIMUTH = -122.0
VERTEX_OFFSET = 0.34
VERTEX_DIRECTIONS = {
    "A": (0.55, 0.55, 0.25),
    "B": (0.30, 0.30, 0.60),
    "C": (0.55, 0.20, 0.35),
    "D": (0.15, 0.55, 0.40),
}

CENTROID = np.mean(np.array(list(VERTICES.values())), axis=0)


def face_centroid(names):
    """Return the centroid of one face.

    Args:
        names: The names of the three vertices of the face.

    Returns:
        The centroid as a numpy array of three coordinates.
    """
    return np.mean(np.array([VERTICES[name] for name in names]), axis=0)


def equation_left_side(point, equation_index):
    """Return the left side of one face equation at a point.

    Args:
        point: The point as a numpy array of three coordinates.
        equation_index: The index of the face in FACES.

    Returns:
        The value of the left side of the equation of that face.
    """
    x_value, y_value, z_value = float(point[0]), float(point[1]), float(point[2])
    left_sides = [z_value, x_value, y_value, x_value + y_value - 2.0 * z_value]
    return left_sides[equation_index]


def main():
    """Draw the solid, check every label point, and write the PNG file."""
    figure = plt.figure(figsize=(7.0, 6.2))
    axes = figure.add_subplot(projection="3d")

    triangles = [np.array([VERTICES[name] for name in names]) for names, _, _ in FACES]
    collection = Poly3DCollection(
        triangles,
        facecolors=[shade for _, _, shade in FACES],
        edgecolors="black",
        linewidths=1.0,
        alpha=figure_common.SURFACE_ALPHA,
    )
    axes.add_collection3d(collection)

    label_points = []
    for index, (names, equation, _) in enumerate(FACES):
        point = face_centroid(names)
        target = [0.0, 2.0, 2.0, 2.0][index]
        assert abs(equation_left_side(point, index) - target) < 1e-12, "face label leaves its own plane"
        label_points.append(point)
        axes.text(
            point[0],
            point[1],
            point[2],
            equation,
            fontsize=10.5,
            ha="center",
            va="center",
            zorder=10,
            bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "alpha": 0.88, "edgecolor": "none"},
        )

    for name, point in VERTICES.items():
        vertex = np.array(point)
        raw = np.array(VERTEX_DIRECTIONS[name], dtype=float)
        direction = raw / float(np.linalg.norm(raw))
        axes.scatter([vertex[0]], [vertex[1]], [vertex[2]], color="black", s=18, depthshade=False, zorder=12)
        leader_start = vertex + 0.05 * direction
        leader_end = vertex + (VERTEX_OFFSET - 0.10) * direction
        axes.plot(
            [leader_start[0], leader_end[0]],
            [leader_start[1], leader_end[1]],
            [leader_start[2], leader_end[2]],
            color="black",
            linewidth=0.7,
        )
        text_point = vertex + VERTEX_OFFSET * direction
        label_points.append(text_point)
        axes.text(
            text_point[0],
            text_point[1],
            text_point[2],
            "$%s$" % name,
            fontsize=11.0,
            ha="center",
            va="center",
            zorder=12,
        )

    axes.set_xlabel("$x$", fontsize=12)
    axes.set_ylabel("$y$", fontsize=12)
    axes.set_zlabel("$z$", fontsize=12)
    axes.set_xlim(0.0, AXES_LIMIT)
    axes.set_ylim(0.0, AXES_LIMIT)
    axes.set_zlim(0.0, HEIGHT_LIMIT)
    axes.set_xticks([0.0, 1.0, 2.0])
    axes.set_yticks([0.0, 1.0, 2.0])
    axes.set_zticks([0.0, 1.0])
    axes.grid(False)
    axes.view_init(elev=VIEW_ELEVATION, azim=VIEW_AZIMUTH)
    axes.set_box_aspect((AXES_LIMIT, AXES_LIMIT, HEIGHT_LIMIT))
    for axis in (axes.xaxis, axes.yaxis, axes.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((0.55, 0.55, 0.55, 0.6))

    figure.canvas.draw()
    figure_common.assert_points_inside(axes, figure, label_points, "labels of the solid", margin=34.0)
    path = figure_common.save_figure(figure, "part1_figure1.png")
    print("figure written: %s" % path)


if __name__ == "__main__":
    main()
