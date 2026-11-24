"""Figure of Part 3: the solid of the iterated integral.

The picture is built from `region_tools.face_report`, so each drawn face is the
closed polygon that the six inequalities produce. The legend names the plane of
each face, and one dark dot marks a point of each face; `part3_verify.py` checks
that every such dot satisfies the equation of its own face. The three screen
axes carry one arrow and one letter each.

The plot puts the variable y on the vertical screen axis, and the variables x
and z on the two horizontal screen axes, because the solid rises in y above
the triangle in the xz-plane.
"""

import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import figure_anchors
import region_tools as region

FIGURE_PATH = "code/figures/part4_figure3.png"
"""Path of the figure file, relative to the workspace."""

FACE_STYLE: dict[str, tuple[str, str, tuple]] = {
    "y is not below 0": ("#8fc3e8", r"$y=0$", figure_anchors.BOTTOM_FACE_ANCHOR),
    "y is not above 2 - 2 z": ("#f2c46a", r"$y+2z=2$", figure_anchors.TOP_FACE_ANCHOR),
    "x is not below 0": ("#a3d99a", r"$x=0$", figure_anchors.WALL_X_ZERO_ANCHOR),
    "z is not below 0": ("#c9b6e0", r"$z=0$", figure_anchors.WALL_Z_ZERO_ANCHOR),
    "z is not above 1 - x": ("#f0a9a5", r"$x+z=1$", figure_anchors.WALL_SUM_ONE_ANCHOR),
}
"""For each face, the fill color, the LaTeX label of its plane, and its anchor point."""

LEGEND_ORDER: tuple[str, ...] = (
    "y is not below 0",
    "y is not above 2 - 2 z",
    "x is not below 0",
    "z is not below 0",
    "z is not above 1 - x",
)
"""Order of the legend entries: the two horizontal faces first, then the three walls."""

EDGE_RECORD_NAMES: tuple[str, ...] = ("x is not above 1",)
"""Names of the planes that touch the solid in one edge only, so they carry no face."""

FACE_ALPHA = 0.62
"""Opacity of every face, high enough to read the solid as a closed body."""

AXIS_ARROWS: tuple[tuple[str, tuple[float, float, float], float, str], ...] = (
    ("x", (1.0, 0.0, 0.0), 1.40, "solid"),
    ("z", (0.0, 1.0, 0.0), 1.92, "dashed"),
    ("y", (0.0, 0.0, 1.0), 2.42, "solid"),
)
"""For each screen axis: the letter, the plot direction, the arrow length, and the line style.

The z axis runs inside the solid from the origin to the far side, so it is drawn
dashed, as a hidden line.
"""

CORNER_OFFSETS: dict[str, tuple[float, float, float]] = {
    "P0": (-0.14, -0.02, -0.20),
    "P1": (0.10, -0.24, -0.24),
    "P2": (-0.26, 0.02, -0.20),
    "P3": (-0.24, 0.02, 0.12),
    "P4": (0.06, 0.12, 0.18),
}
"""Offset of the label of each corner in plot coordinates."""


def to_plot(point) -> tuple[float, float, float]:
    """Return a point of the solid in screen coordinates, with y on the vertical axis."""
    return (float(point[0]), float(point[2]), float(point[1]))


def unit(vector: np.ndarray) -> np.ndarray:
    """Return a vector of length one in the direction of the input vector."""
    length = float(np.linalg.norm(vector))
    if length == 0.0:
        return vector
    return vector / length


def draw_faces(axes, vertices: list) -> list[Patch]:
    """Draw every face with its boundary and its anchor dot, and build the legend handles."""
    handles: list[tuple[str, Patch]] = []
    for record in region.face_report(vertices):
        name = str(record["name"])
        if name in EDGE_RECORD_NAMES:
            continue
        color, label, anchor = FACE_STYLE[name]
        polygon = [to_plot(point) for point in record["points"]]
        axes.add_collection3d(
            Poly3DCollection(
                [polygon],
                facecolor=color,
                edgecolor="#17324a",
                linewidth=1.4,
                alpha=FACE_ALPHA,
                zorder=2,
            )
        )
        axes.scatter(*to_plot(anchor), color="#17324a", s=13, depthshade=False, zorder=8)
        handles.append((name, Patch(facecolor=color, edgecolor="#17324a", label=label)))
    ordered = {name: handle for name, handle in handles}
    return [ordered[name] for name in LEGEND_ORDER]


def draw_corners(axes, vertices: list) -> None:
    """Mark each corner and write its name away from the solid."""
    names = {point: name for name, point in figure_anchors.VERTEX_NAMES}
    for point in vertices:
        position = np.array(to_plot(point))
        axes.scatter(*position, color="#0d2233", s=30, depthshade=False, zorder=7)
        axes.text(
            *(position + np.array(CORNER_OFFSETS[names[point]])),
            names[point],
            fontsize=10,
            color="#0d2233",
            horizontalalignment="center",
            verticalalignment="center",
            zorder=8,
        )


def draw_height(axes) -> None:
    """Draw the height of one point of the base up to the top face."""
    foot = np.array(to_plot(figure_anchors.HEIGHT_SEGMENT_FOOT))
    head = np.array(to_plot(figure_anchors.HEIGHT_SEGMENT_HEAD))
    axes.plot(
        [foot[0], head[0]],
        [foot[1], head[1]],
        [foot[2], head[2]],
        color="#9c2f1c",
        linewidth=1.8,
        linestyle=(0, (4, 3)),
        zorder=6,
    )
    for end in (foot, head):
        axes.scatter(*end, color="#9c2f1c", s=16, depthshade=False, zorder=7)
    axes.text(
        *(head + np.array([0.30, -0.10, 0.04])),
        r"$2-2z$",
        fontsize=10.5,
        color="#9c2f1c",
        horizontalalignment="left",
        verticalalignment="center",
        zorder=8,
    )


def draw_axes(axes) -> None:
    """Draw one arrow and one letter for each screen axis."""
    for letter, direction, length, style in AXIS_ARROWS:
        vector = np.array(direction) * length
        axes.quiver(
            0.0,
            0.0,
            0.0,
            vector[0],
            vector[1],
            vector[2],
            color="#333333",
            linewidth=1.4 if style == "solid" else 1.2,
            linestyle="solid" if style == "solid" else (0, (5, 3)),
            arrow_length_ratio=0.085,
            zorder=9,
        )
        tip = vector + unit(np.array(direction)) * 0.14
        axes.text(
            *tip,
            rf"${letter}$",
            fontsize=13,
            color="#222222",
            horizontalalignment="center",
            verticalalignment="center",
            zorder=10,
        )


def main() -> None:
    """Draw the solid and write the figure file."""
    elevation = float(sys.argv[1]) if len(sys.argv) > 1 else 20.0
    azimuth = float(sys.argv[2]) if len(sys.argv) > 2 else -62.0
    output = sys.argv[3] if len(sys.argv) > 3 else FIGURE_PATH
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Cambria", "DejaVu Serif"]
    plt.rcParams["mathtext.fontset"] = "stix"
    figure = plt.figure(figsize=(9.8, 6.3))
    axes = figure.add_axes((0.0, 0.0, 0.74, 1.0), projection="3d", computed_zorder=False)
    vertices = region.enumerate_vertices()
    handles = draw_faces(axes, vertices)
    draw_corners(axes, vertices)
    draw_height(axes)
    draw_axes(axes)
    axes.set_xlim(-0.14, 1.50)
    axes.set_ylim(-0.14, 1.50)
    axes.set_zlim(-0.12, 2.60)
    axes.set_box_aspect((1.64, 1.64, 2.72))
    axes.set_axis_off()
    axes.view_init(elev=elevation, azim=azimuth)
    figure.legend(
        handles=handles,
        loc="center right",
        frameon=False,
        fontsize=10.5,
        handlelength=1.4,
        labelspacing=0.9,
        borderaxespad=0.2,
    )
    figure.savefig(output, dpi=190, bbox_inches="tight", pad_inches=0.08)
    print(f"wrote {output} with elev={elevation} azim={azimuth}")


if __name__ == "__main__":
    main()
