"""Draw Figure 1: the silo in space, and its projection on the plane y = 0.

The left panel shows the three faces of the body, one horizontal section, the three axes, and
one label for each face.  Each label is joined to an anchor point that the equation of its own
surface satisfies, so a label cannot float away from the surface that it names.  The right
panel shows the projection on the plane y = 0: the rectangle of the cylinder and the half disk
of the cap.

Every text of the left panel is a two-dimensional annotation placed at the projected position of
its anchor.  The script checks that each text lies inside the box of its axes and that no two
texts overlap.  It writes the figure to ``code/figures/part1_figure1.png``.
"""

import math
import pathlib

import matplotlib
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers the three-dimensional projection)
from mpl_toolkits.mplot3d import proj3d

from figure_anchors import (
    AXIS_X_MAXIMUM,
    AXIS_X_MINIMUM,
    AXIS_Y_MAXIMUM,
    AXIS_Y_MINIMUM,
    AXIS_Z_MAXIMUM,
    AXIS_Z_MINIMUM,
    CAP_ALPHA,
    SECTION_HEIGHT_SHOWN,
    VIEW_AZIMUTH_DEGREES,
    VIEW_ELEVATION_DEGREES,
    WALL_ALPHA,
    cap_label_anchor,
    lateral_label_anchor,
    lower_face_label_anchor,
)
from silo_geometry import (
    APEX_HEIGHT,
    CAP_RADIUS,
    CYLINDER_HEIGHT,
    CYLINDER_RADIUS,
    cap_residual,
    lateral_residual,
    section_radius_from_formula,
)

matplotlib.rcParams["font.family"] = "Cambria"
matplotlib.rcParams["mathtext.fontset"] = "custom"
matplotlib.rcParams["mathtext.rm"] = "XITS"
matplotlib.rcParams["mathtext.it"] = "XITS:italic"

OUTPUT_PATH = pathlib.Path(__file__).resolve().parent / "figures" / "part1_figure1.png"
"""Path of the drawn figure."""

TEXT_SIZE = 9.0
"""Font size of every label of the figure, in points."""

LATERAL_LABEL_OFFSET = (-74.0, -8.0)
"""Offset of the lateral face label from its anchor, in points."""

CAP_LABEL_OFFSET = (-30.0, 22.0)
"""Offset of the cap label from its anchor, in points."""

LOWER_LABEL_OFFSET = (-2.0, -48.0)
"""Offset of the lower disk label from its anchor, in points."""

SECTION_LABEL_OFFSET = (26.0, 26.0)
"""Offset of the section label from its anchor, in points."""

SECTION_LABEL_ANGLE_DEGREES = 38.0
"""Angle of the point of the section that carries the section label, in degrees."""

FIGURE_SIZE_INCHES = (10.2, 5.6)
"""Size of the drawn figure, in inches."""

THREE_DIMENSIONAL_PANEL_BOUNDS = (0.005, 0.005, 0.575, 0.925)
"""Bounds of the three-dimensional panel in figure coordinates."""

PROJECTION_PANEL_LEFT = 0.655
"""Left edge of the projection panel in figure coordinates."""

PROJECTION_PANEL_BOTTOM = 0.095
"""Bottom edge of the projection panel in figure coordinates."""

PROJECTION_PANEL_HEIGHT = 0.845
"""Height of the projection panel in figure coordinates."""

PROJECTION_X_LIMITS = (-4.2, 4.2)
"""Limits of the horizontal coordinate of the projection panel."""

PROJECTION_Z_LIMITS = (-1.3, 14.1)
"""Limits of the vertical coordinate of the projection panel."""


def project_to_axes_fraction(axes, point):
    """Return the position of a point of space in the coordinate system of the axes box."""
    projected = proj3d.proj_transform(point[0], point[1], point[2], axes.get_proj())
    pixel = axes.transData.transform((projected[0], projected[1]))
    return tuple(axes.transAxes.inverted().transform(pixel))


def annotate_point(axes, point, text, offset, color, size=TEXT_SIZE, alignment="center",
                   halo=False):
    """Place a two-dimensional label at the projected position of a point of space."""
    position = project_to_axes_fraction(axes, point)
    label = axes.annotate(
        text,
        xy=position,
        xycoords=axes.transAxes,
        xytext=offset,
        textcoords="offset points",
        ha=alignment,
        va="center",
        fontsize=size,
        color=color,
        annotation_clip=False,
        arrowprops={
            "arrowstyle": "-",
            "linewidth": 0.8,
            "linestyle": (0, (2.4, 1.8)),
            "color": color,
            "shrinkA": 2.0,
            "shrinkB": 2.0,
        },
    )
    if halo:
        label.set_path_effects([path_effects.withStroke(linewidth=2.4, foreground="white")])
    return label


def draw_lateral_face(axes) -> None:
    """Draw the lateral face of the cylinder as a surface."""
    angles = np.linspace(0.0, 2.0 * math.pi, 121)
    heights = np.linspace(0.0, CYLINDER_HEIGHT, 41)
    angle_grid, height_grid = np.meshgrid(angles, heights)
    axes.plot_surface(
        CYLINDER_RADIUS * np.cos(angle_grid),
        CYLINDER_RADIUS * np.sin(angle_grid),
        height_grid,
        color="#9ec5e8",
        alpha=WALL_ALPHA,
        linewidth=0.0,
        antialiased=True,
        shade=True,
    )


def draw_cap(axes) -> None:
    """Draw the hemispherical cap as a surface."""
    angles = np.linspace(0.0, 2.0 * math.pi, 121)
    inclinations = np.linspace(0.0, 0.5 * math.pi, 41)
    angle_grid, inclination_grid = np.meshgrid(angles, inclinations)
    axes.plot_surface(
        CAP_RADIUS * np.sin(inclination_grid) * np.cos(angle_grid),
        CAP_RADIUS * np.sin(inclination_grid) * np.sin(angle_grid),
        CYLINDER_HEIGHT + CAP_RADIUS * np.cos(inclination_grid),
        color="#f3c9a0",
        alpha=CAP_ALPHA,
        linewidth=0.0,
        antialiased=True,
        shade=True,
    )


def draw_lower_disk(axes) -> None:
    """Draw the lower disk of the body as a filled surface."""
    radii = np.linspace(0.0, CYLINDER_RADIUS, 31)
    angles = np.linspace(0.0, 2.0 * math.pi, 121)
    radius_grid, angle_grid = np.meshgrid(radii, angles)
    axes.plot_surface(
        radius_grid * np.cos(angle_grid),
        radius_grid * np.sin(angle_grid),
        np.zeros_like(radius_grid),
        color="#b9d5c9",
        alpha=0.85,
        linewidth=0.0,
        antialiased=True,
        shade=False,
    )


def draw_section(axes) -> None:
    """Draw the horizontal section at the height shown, as a filled disk."""
    radius = section_radius_from_formula(SECTION_HEIGHT_SHOWN)
    radii = np.linspace(0.0, radius, 11)
    angles = np.linspace(0.0, 2.0 * math.pi, 121)
    radius_grid, angle_grid = np.meshgrid(radii, angles)
    axes.plot_surface(
        radius_grid * np.cos(angle_grid),
        radius_grid * np.sin(angle_grid),
        np.full_like(radius_grid, SECTION_HEIGHT_SHOWN),
        color="#d94f4f",
        alpha=0.30,
        linewidth=0.0,
        antialiased=True,
        shade=False,
    )
    outline = np.linspace(0.0, 2.0 * math.pi, 361)
    axes.plot(
        radius * np.cos(outline),
        radius * np.sin(outline),
        np.full_like(outline, SECTION_HEIGHT_SHOWN),
        color="#a32020",
        linewidth=1.1,
    )


def draw_axes(axes) -> None:
    """Draw the three axes with one arrow for each axis.

    Each arrow is the only axis mechanism of the panel, and each letter sits just beyond the
    tip of its own arrow.
    """
    arrow_ratio = 0.05
    axes.quiver(AXIS_X_MINIMUM, 0.0, 0.0, AXIS_X_MAXIMUM - AXIS_X_MINIMUM, 0.0, 0.0,
                arrow_length_ratio=arrow_ratio, linewidth=1.1, color="#333333")
    axes.quiver(0.0, AXIS_Y_MINIMUM, 0.0, 0.0, AXIS_Y_MAXIMUM - AXIS_Y_MINIMUM, 0.0,
                arrow_length_ratio=arrow_ratio, linewidth=1.1, color="#333333")
    axes.quiver(0.0, 0.0, AXIS_Z_MINIMUM, 0.0, 0.0, AXIS_Z_MAXIMUM - AXIS_Z_MINIMUM,
                arrow_length_ratio=arrow_ratio, linewidth=1.1, color="#333333")
    annotate_point(axes, (AXIS_X_MAXIMUM, 0.0, 0.0), "$x$", (5.0, -7.0), "#222222",
                   size=TEXT_SIZE + 1.5)
    annotate_point(axes, (0.0, AXIS_Y_MAXIMUM, 0.0), "$y$", (6.0, 3.0), "#222222",
                   size=TEXT_SIZE + 1.5)
    annotate_point(axes, (0.0, 0.0, AXIS_Z_MAXIMUM), "$z$", (-9.0, 2.0), "#222222",
                   size=TEXT_SIZE + 1.5)

    for height in (3.0, 10.0, 13.0):
        axes.plot([-0.15, 0.15], [0.0, 0.0], [height, height], color="#333333", linewidth=0.9)
        annotate_point(axes, (0.0, 0.0, height), f"{height:.0f}", (13.0, -1.0), "#2b2b2b",
                       size=TEXT_SIZE - 1.0, halo=True)
    for direction in (1.0, -1.0):
        axes.plot([direction * 3.0, direction * 3.0], [-0.15, 0.15], [0.0, 0.0],
                  color="#333333", linewidth=0.9)
        axes.plot([-0.15, 0.15], [direction * 3.0, direction * 3.0], [0.0, 0.0],
                  color="#333333", linewidth=0.9)


def draw_projection_panel(panel) -> None:
    """Draw the projection of the body on the plane y = 0."""
    rectangle = plt.Rectangle((-CYLINDER_RADIUS, 0.0), 2.0 * CYLINDER_RADIUS, CYLINDER_HEIGHT,
                              facecolor="#9ec5e8", edgecolor="#2f5f8f", alpha=0.55,
                              linewidth=1.0)
    panel.add_patch(rectangle)
    angles = np.linspace(0.0, math.pi, 241)
    panel.fill_between(
        CAP_RADIUS * np.cos(angles),
        CYLINDER_HEIGHT,
        CYLINDER_HEIGHT + CAP_RADIUS * np.sin(angles),
        color="#f3c9a0",
        alpha=0.75,
        edgecolor="#9a6a3a",
        linewidth=1.0,
    )
    panel.plot([-CYLINDER_RADIUS, CYLINDER_RADIUS], [CYLINDER_HEIGHT, CYLINDER_HEIGHT],
               color="#8a8a8a", linewidth=0.9, linestyle=(0, (4.0, 2.0)))
    panel.set_xlim(*PROJECTION_X_LIMITS)
    panel.set_ylim(*PROJECTION_Z_LIMITS)
    panel.set_aspect("equal")
    panel.set_xlabel("$x$", fontsize=TEXT_SIZE + 1.5, color="#222222", labelpad=1.0)
    vertical_label = panel.annotate(
        "$z$", xy=(0.0, 1.0), xycoords="axes fraction", xytext=(-16.0, 2.0),
        textcoords="offset points", ha="right", va="center",
        fontsize=TEXT_SIZE + 1.5, color="#222222", annotation_clip=False,
    )
    vertical_label.set_gid("axis-label")
    panel.set_xticks([-3.0, 0.0, 3.0])
    panel.set_xticklabels(["$-3$", "$0$", "$3$"])
    panel.set_yticks([0.0, 10.0, 13.0])
    panel.tick_params(labelsize=TEXT_SIZE - 0.5, length=3.2, pad=2.0, colors="#2b2b2b")
    panel.grid(False)
    for side in ("top", "right"):
        panel.spines[side].set_visible(False)
    panel.text(0.0, 5.0, "rectangle\n$|x|\\leq 3$, $0\\leq z\\leq 10$",
               fontsize=TEXT_SIZE - 1.0, ha="center", va="center", color="#1d3f5f")
    panel.text(0.0, 11.6, "half disk\n$x^{2}+(z-10)^{2}\\leq 9$",
               fontsize=TEXT_SIZE - 1.0, ha="center", va="center", color="#6b441d")


def check_layout(figure, axes, panel) -> None:
    """Assert that every text lies inside its axes box and that no two texts overlap."""
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    for artists, box in (
        (list(axes.texts), axes.bbox),
        (list(panel.texts), panel.bbox),
    ):
        extents = [artist.get_window_extent(renderer=renderer) for artist in artists]
        for artist, extent in zip(artists, extents):
            if artist.get_gid() == "axis-label":
                continue
            inside = (
                extent.x0 >= box.x0 - 1.5
                and extent.x1 <= box.x1 + 1.5
                and extent.y0 >= box.y0 - 1.5
                and extent.y1 <= box.y1 + 1.5
            )
            if not inside:
                raise AssertionError(
                    f"text {artist.get_text()!r} leaves its axes box: "
                    f"{extent.bounds} against {box.bounds}"
                )
        for first_index in range(len(artists)):
            for second_index in range(first_index + 1, len(artists)):
                if extents[first_index].overlaps(extents[second_index]):
                    raise AssertionError(
                        f"texts {artists[first_index].get_text()!r} and "
                        f"{artists[second_index].get_text()!r} overlap"
                    )


def main() -> None:
    """Draw the figure, check its layout, and write the PNG file."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure = plt.figure(figsize=FIGURE_SIZE_INCHES, dpi=200)
    axes = figure.add_axes(THREE_DIMENSIONAL_PANEL_BOUNDS, projection="3d")
    width = (
        PROJECTION_PANEL_HEIGHT
        * FIGURE_SIZE_INCHES[1]
        / FIGURE_SIZE_INCHES[0]
        * (PROJECTION_X_LIMITS[1] - PROJECTION_X_LIMITS[0])
        / (PROJECTION_Z_LIMITS[1] - PROJECTION_Z_LIMITS[0])
    )
    panel = figure.add_axes(
        (PROJECTION_PANEL_LEFT, PROJECTION_PANEL_BOTTOM, width, PROJECTION_PANEL_HEIGHT)
    )
    figure.text(0.275, 0.975, "the silo: cylinder $r=3$, $0\\leq z\\leq 10$, and a hemisphere",
                fontsize=10.0, ha="center", va="top", color="#222222")
    figure.text(0.785, 0.975, "projection on the plane $y=0$", fontsize=10.0,
                ha="center", va="top", color="#222222")

    draw_lower_disk(axes)
    draw_lateral_face(axes)
    draw_cap(axes)
    draw_section(axes)

    axes.set_xlim(AXIS_X_MINIMUM, AXIS_X_MAXIMUM)
    axes.set_ylim(AXIS_Y_MINIMUM, AXIS_Y_MAXIMUM)
    axes.set_zlim(AXIS_Z_MINIMUM, AXIS_Z_MAXIMUM)
    axes.set_box_aspect((1.0, 1.0, 1.62), zoom=0.90)
    axes.view_init(elev=VIEW_ELEVATION_DEGREES, azim=VIEW_AZIMUTH_DEGREES)
    axes.set_axis_off()

    draw_axes(axes)
    annotate_point(axes, lateral_label_anchor(), "lateral face\n$x^{2}+y^{2}=9$",
                   LATERAL_LABEL_OFFSET, "#1d4f7a")
    annotate_point(axes, cap_label_anchor(), "cap\n$x^{2}+y^{2}+(z-10)^{2}=9$",
                   CAP_LABEL_OFFSET, "#8a5520")
    annotate_point(axes, lower_face_label_anchor(), "lower disk\n$z=0$",
                   LOWER_LABEL_OFFSET, "#2f5f4a")
    section_angle = math.radians(SECTION_LABEL_ANGLE_DEGREES)
    section_radius = section_radius_from_formula(SECTION_HEIGHT_SHOWN)
    annotate_point(
        axes,
        (section_radius * math.cos(section_angle), section_radius * math.sin(section_angle),
         SECTION_HEIGHT_SHOWN),
        f"section at $z={SECTION_HEIGHT_SHOWN:.0f}$",
        SECTION_LABEL_OFFSET,
        "#a32020",
        size=TEXT_SIZE - 1.5,
    )

    draw_projection_panel(panel)

    print(f"lateral residual of its label anchor: "
          f"{abs(lateral_residual(*lateral_label_anchor())):.3e}", flush=True)
    print(f"cap residual of its label anchor: {abs(cap_residual(*cap_label_anchor())):.3e}",
          flush=True)
    print(f"lower disk anchor height: {lower_face_label_anchor()[2]:.6f}", flush=True)
    print(f"apex height: {APEX_HEIGHT:.6f}, section radius at "
          f"{SECTION_HEIGHT_SHOWN:.1f}: {section_radius_from_formula(SECTION_HEIGHT_SHOWN):.6f}",
          flush=True)
    check_layout(figure, axes, panel)
    figure.savefig(OUTPUT_PATH, dpi=200, facecolor="white")
    print(f"wrote {OUTPUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
