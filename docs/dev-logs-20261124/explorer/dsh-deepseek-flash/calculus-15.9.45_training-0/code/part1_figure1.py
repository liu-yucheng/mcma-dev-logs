"""Draw Figure 1: the bumpy sphere in space and the radius as a map of the two angles.

The left panel draws the surface of the statement with the unit sphere beside it, so the reader
sees how far the bumps leave the sphere.  The right panel draws the same function as a filled
contour map over the rectangle of the two angles, so the reader sees where the bumps sit.  Both
marked points are read from :mod:`bumpy_sphere`, which the checks also read.

The script writes ``code/figures/part1_figure1.png`` and, for the working record, a larger view
without labels under the name ``solution_baseline.png`` at the workspace root.
"""

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.axes
import matplotlib.cm
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import bumpy_sphere
import figure_tools

WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
"""Root of the problem workspace."""

THETA_LINE_COUNT = 361
"""Number of sample lines along the azimuthal angle of the drawn surface."""

PHI_LINE_COUNT = 181
"""Number of sample lines along the polar angle of the drawn surface."""

WIRE_LINE_COUNT = 25
"""Number of wire lines of the unit sphere of the left panel."""

MAP_LINE_COUNT = 361
"""Number of sample lines along each angle of the contour map."""

LABEL_OFFSET = 0.30
"""Distance of a label from the point that it names, in length units."""

LABEL_GAP_PIXELS = 46.0
"""Distance in pixels between a label and the mark that its arrow names."""


def surface_grid() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return the drawn coordinates of the surface and its radius.

    Returns:
        The arrays ``x``, ``y``, ``z`` of the surface and the array of the radius.
    """
    theta = np.linspace(0.0, 2.0 * np.pi, THETA_LINE_COUNT)
    phi = np.linspace(0.0, np.pi, PHI_LINE_COUNT)
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    rho = bumpy_sphere.radius_array(theta_grid, phi_grid)
    x, y, z = bumpy_sphere.to_cartesian(theta_grid, phi_grid, rho)
    return x, y, z, rho


def draw_solid_panel(axes: matplotlib.axes.Axes) -> list:
    """Draw the surface and the unit sphere in one three dimensional axes.

    Args:
        axes: Three dimensional axes of the left panel.

    Returns:
        The handles that the legend shows.
    """
    x, y, z, rho = surface_grid()
    colour_map = matplotlib.colormaps[bumpy_sphere.COLOR_MAP]
    normalizer = matplotlib.colors.Normalize(float(bumpy_sphere.RADIUS_MINIMUM),
                                             float(bumpy_sphere.RADIUS_MAXIMUM))
    faces = colour_map(normalizer(rho))
    surface = axes.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=faces, shade=False,
                                alpha=0.92, linewidth=0.0, antialiased=True)

    theta_wire = np.linspace(0.0, 2.0 * np.pi, WIRE_LINE_COUNT)
    phi_wire = np.linspace(0.0, np.pi, WIRE_LINE_COUNT)
    wire_theta, wire_phi = np.meshgrid(theta_wire, phi_wire)
    wire = axes.plot_wireframe(np.sin(wire_phi) * np.cos(wire_theta),
                               np.sin(wire_phi) * np.sin(wire_theta),
                               np.cos(wire_phi), rstride=2, cstride=2, color="0.30",
                               linewidth=0.55, alpha=0.45)

    axes.set_xlabel("$x$", fontsize=9, labelpad=1)
    axes.set_ylabel("$y$", fontsize=9, labelpad=1)
    axes.set_zlabel("$z$", fontsize=9, labelpad=1)
    axes.tick_params(labelsize=7, pad=0)
    axes.set_xlim(-1.45, 1.45)
    axes.set_ylim(-1.45, 1.45)
    axes.set_zlim(-1.45, 1.45)
    axes.set_box_aspect((1.0, 1.0, 1.0))
    axes.view_init(elev=bumpy_sphere.VIEW_ELEVATION, azim=bumpy_sphere.VIEW_AZIMUTH)
    axes.set_title("(a) the body and the unit sphere", fontsize=10, pad=2)
    return [surface, wire]


def draw_marked_points(
    axes: matplotlib.axes.Axes,
    figure: matplotlib.figure.Figure,
) -> tuple[list, list]:
    """Mark the two extreme points of the surface and place one label beside each mark.

    The label of a mark sits on the outward radial direction of that mark, and the arrow of the
    label stops seven pixels short of the mark, so the arrowhead never covers the surface point
    that it names.

    Args:
        axes: Three dimensional axes of the left panel.
        figure: Figure that holds the axes.

    Returns:
        The two annotation texts and one pair of a text and the display position of its mark.
    """
    marked = bumpy_sphere.marked_points()
    texts = []
    anchors = []
    for name, colour, label in (
        ("peak", "#b2182b", r"$\rho = 6/5$"),
        ("valley", "#2166ac", r"$\rho = 4/5$"),
    ):
        point = np.array(marked[name])
        direction = point / float(np.linalg.norm(point))
        outward = point + direction * LABEL_OFFSET
        display_point = figure_tools.project_point_3d(axes, figure, tuple(point))
        display_outward = figure_tools.project_point_3d(axes, figure, tuple(outward))
        step = np.subtract(display_outward, display_point)
        length = float(np.hypot(step[0], step[1]))
        unit = step / length if length > 1.0e-9 else np.array([0.0, 1.0])
        offset = np.add(display_point, unit * LABEL_GAP_PIXELS)
        axes.plot([point[0]], [point[1]], [point[2]], marker="o", markersize=4.8, color=colour,
                  markeredgecolor="white", markeredgewidth=0.7, linestyle="none", zorder=12)
        annotation = axes.annotate(
            label,
            xy=figure_tools.axes_fraction(axes, display_point),
            xycoords="axes fraction",
            xytext=figure_tools.axes_fraction(axes, (float(offset[0]), float(offset[1]))),
            textcoords="axes fraction",
            fontsize=9, color=colour, ha="center", va="center", zorder=14,
            bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": colour,
                  "alpha": 0.94, "linewidth": 0.7},
            arrowprops={"arrowstyle": "-|>", "color": colour, "linewidth": 1.1,
                        "shrinkA": 3.0, "shrinkB": 7.0, "mutation_scale": 9.0},
        )
        texts.append(annotation)
        anchors.append((annotation, display_point))
    return texts, anchors


def draw_map_panel(axes: matplotlib.axes.Axes) -> tuple[list, matplotlib.axes.Axes]:
    """Draw the radius as a filled contour map over the rectangle of the two angles.

    Args:
        axes: Axes of the right panel.

    Returns:
        The texts of the marked points and the axes of the colour bar.
    """
    theta = np.linspace(0.0, 2.0 * np.pi, MAP_LINE_COUNT)
    phi = np.linspace(0.0, np.pi, MAP_LINE_COUNT)
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    rho = bumpy_sphere.radius_array(theta_grid, phi_grid)
    levels = np.linspace(float(bumpy_sphere.RADIUS_MINIMUM), float(bumpy_sphere.RADIUS_MAXIMUM),
                         13)
    filled = axes.contourf(theta_grid, phi_grid, rho, levels=levels,
                           cmap=bumpy_sphere.COLOR_MAP, extend="neither")
    axes.contour(theta_grid, phi_grid, rho, levels=levels, colors="0.25", linewidths=0.35)
    colour_bar = axes.figure.colorbar(filled, ax=axes, pad=0.03, fraction=0.046)
    colour_bar.set_label(r"$\rho$ in length units", fontsize=9)
    colour_bar.ax.tick_params(labelsize=7, pad=1)

    marked = bumpy_sphere.marked_points()
    marks = (
        (bumpy_sphere.LOBE_THETA, bumpy_sphere.LOBE_PHI, r"$6/5$", "#b2182b", 12.0, 8.0),
        (bumpy_sphere.VALLEY_THETA, bumpy_sphere.VALLEY_PHI, r"$4/5$", "#2166ac", 12.0, -14.0),
    )
    texts = []
    for angle_theta, angle_phi, label, colour, offset_x, offset_y in marks:
        axes.plot([angle_theta], [angle_phi], marker="o", markersize=4.6, color=colour,
                  markeredgecolor="white", markeredgewidth=0.7, linestyle="none", zorder=8)
        texts.append(axes.annotate(label, xy=(angle_theta, angle_phi),
                                   xytext=(offset_x, offset_y), textcoords="offset points",
                                   fontsize=9, color=colour, ha="left",
                                   va="center",
                                   bbox={"boxstyle": "round,pad=0.16", "facecolor": "white",
                                         "edgecolor": colour, "alpha": 0.92, "linewidth": 0.6}))
    axes.set_xlabel(r"$\theta$", fontsize=9, labelpad=1)
    axes.set_ylabel(r"$\varphi$", fontsize=9, labelpad=1)
    axes.tick_params(labelsize=7, pad=1)
    axes.set_xlim(0.0, 2.0 * np.pi)
    axes.set_ylim(0.0, np.pi)
    axes.set_xticks([0.0, np.pi / 2.0, np.pi, 3.0 * np.pi / 2.0, 2.0 * np.pi])
    axes.set_xticklabels(["$0$", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    axes.set_yticks([0.0, np.pi / 4.0, np.pi / 2.0, 3.0 * np.pi / 4.0, np.pi])
    axes.set_yticklabels(["$0$", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])
    axes.set_title("(b) the radius over the rectangle of the angles", fontsize=10, pad=2)
    return texts, colour_bar.ax


def draw_baseline() -> pathlib.Path:
    """Draw one large view of the body without labels and write it at the workspace root.

    Returns:
        The path of the written image.
    """
    figure = plt.figure(figsize=(5.4, 5.0))
    axes = figure.add_subplot(111, projection="3d")
    x, y, z, rho = surface_grid()
    colour_map = matplotlib.colormaps[bumpy_sphere.COLOR_MAP]
    normalizer = matplotlib.colors.Normalize(float(bumpy_sphere.RADIUS_MINIMUM),
                                             float(bumpy_sphere.RADIUS_MAXIMUM))
    axes.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=colour_map(normalizer(rho)),
                      shade=False, alpha=0.95, linewidth=0.0, antialiased=True)
    axes.set_xlabel("$x$")
    axes.set_ylabel("$y$")
    axes.set_zlabel("$z$")
    axes.set_box_aspect((1.0, 1.0, 1.0))
    axes.view_init(elev=bumpy_sphere.VIEW_ELEVATION, azim=bumpy_sphere.VIEW_AZIMUTH)
    path = WORKSPACE / "solution_baseline.png"
    figure.savefig(path, dpi=170, bbox_inches="tight", pad_inches=0.1)
    plt.close(figure)
    print(f"baseline written to {path}", flush=True)
    return path


def main() -> None:
    """Draw both panels, check the label layout, and write the PNG file."""
    figure = plt.figure(figsize=(11.4, 4.9))
    axes_left = figure.add_subplot(1, 2, 1, projection="3d")
    axes_right = figure.add_subplot(1, 2, 2)

    handles = draw_solid_panel(axes_left)
    texts_left, anchors_left = draw_marked_points(axes_left, figure)
    texts_right, colour_axes = draw_map_panel(axes_right)
    axes_left.legend(handles, [r"surface $\rho = 1 + \frac{1}{5}\sin 6\theta\,\sin 5\varphi$",
                               r"unit sphere $\rho = 1$"],
                     loc="upper left", fontsize=7.4, framealpha=0.92,
                     handlelength=1.4, borderpad=0.35)

    figure.canvas.draw()
    anchors = list(anchors_left)
    for text, angles in zip(texts_right, ((bumpy_sphere.LOBE_THETA, bumpy_sphere.LOBE_PHI),
                                          (bumpy_sphere.VALLEY_THETA, bumpy_sphere.VALLEY_PHI))):
        display = axes_right.transData.transform(angles)
        anchors.append((text, (float(display[0]), float(display[1]))))

    legend_texts = list(axes_left.get_legend().get_texts())
    record = figure_tools.finish_figure(
        figure, [axes_left, axes_right, colour_axes],
        texts_left + texts_right + legend_texts,
        "part1_figure1", anchors=anchors,
    )
    plt.close(figure)

    x, y, z, rho = surface_grid()
    print(f"drawn surface: {THETA_LINE_COUNT} by {PHI_LINE_COUNT} sample lines, "
          f"radius from {rho.min():.6f} to {rho.max():.6f}", flush=True)
    print(f"labels: {record['labels']}", flush=True)
    draw_baseline()


if __name__ == "__main__":
    main()
