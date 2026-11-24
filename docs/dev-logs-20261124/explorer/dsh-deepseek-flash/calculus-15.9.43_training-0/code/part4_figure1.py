"""Draw Figure 3: the surface area of a triangle mesh against its resolution.

Each curve is the area of one face of the body computed from a triangle mesh.  The closed form
of the same face is printed in the title of the left panel of the page, and the right panel
shows the relative error of each face against that closed form.

It writes the figure to ``code/figures/part4_figure1.png``.
"""

import pathlib

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from silo_geometry import (
    base_mesh,
    cap_mesh,
    cap_surface_area,
    cylinder_surface_area,
    lateral_mesh,
    LOWER_FACE_AREA,
    mesh_area,
    surface_area_by_mesh,
)

matplotlib.rcParams["font.family"] = "Cambria"
matplotlib.rcParams["mathtext.fontset"] = "custom"
matplotlib.rcParams["mathtext.rm"] = "XITS"
matplotlib.rcParams["mathtext.it"] = "XITS:italic"

OUTPUT_PATH = pathlib.Path(__file__).resolve().parent / "figures" / "part4_figure1.png"
"""Path of the drawn figure."""

RESOLUTIONS = (6, 10, 16, 24, 32, 48, 64, 96, 128)
"""Resolutions of the drawn mesh, in cells along one direction."""

TOLERANCE_FOR_THE_FINE_MESH = 5.0e-4
"""Relative error that the finest mesh of the figure must reach."""


def measure_mesh(resolution: int) -> dict:
    """Return the area of each face of a mesh of the given resolution."""
    lateral_nodes, lateral_triangles = lateral_mesh(resolution, resolution)
    cap_nodes, cap_triangles = cap_mesh(resolution, max(1, resolution // 2))
    base_nodes, base_triangles = base_mesh(resolution, max(1, resolution // 2))
    area = {
        "lateral": mesh_area(lateral_nodes, lateral_triangles),
        "cap": mesh_area(cap_nodes, cap_triangles),
        "base": mesh_area(base_nodes, base_triangles),
    }
    area["total"] = area["lateral"] + area["cap"] + area["base"]
    reference = surface_area_by_mesh(resolution)
    if abs(area["total"] - reference) > 1.0e-9:
        raise AssertionError(
            f"the face sum {area['total']:.12f} differs from the library total {reference:.12f}"
        )
    return area


def check_artist_inside(figure, axes, artist) -> None:
    """Assert that one artist lies inside the box of its axes."""
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    extent = artist.get_window_extent(renderer=renderer)
    box = axes.bbox
    if not (
        extent.x0 >= box.x0 - 1.5
        and extent.x1 <= box.x1 + 1.5
        and extent.y0 >= box.y0 - 1.5
        and extent.y1 <= box.y1 + 1.5
    ):
        raise AssertionError(f"artist leaves the axes box: {extent.bounds} against {box.bounds}")


def main() -> None:
    """Draw the figure and write the PNG file."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    records = [measure_mesh(resolution) for resolution in RESOLUTIONS]

    figure, (value_panel, error_panel) = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=200)
    figure.subplots_adjust(left=0.085, right=0.985, top=0.87, bottom=0.17, wspace=0.26)

    series = (
        ("lateral", "#1d4f7a", cylinder_surface_area(), "$60\\pi$"),
        ("cap", "#8a5520", cap_surface_area(), "$18\\pi$"),
        ("base", "#2f5f4a", LOWER_FACE_AREA, "$9\\pi$"),
    )
    positions = np.arange(len(RESOLUTIONS), dtype=float)
    for name, color, closed_form, symbol in series:
        values = np.array([record[name] for record in records])
        value_panel.plot(positions, values, marker="o", markersize=3.0, linewidth=1.4,
                         color=color, label=f"{name} face")
        error_panel.plot(positions, np.abs(values - closed_form) / closed_form, marker="o",
                         markersize=3.0, linewidth=1.4, color=color, label=f"{name} face")
        print(f"{name} face: closed form {closed_form:.9f} = {symbol}", flush=True)

    label_positions = [0, 2, 4, 6, 8]
    label_texts = [f"{RESOLUTIONS[index]:d}" for index in label_positions]
    for panel in (value_panel, error_panel):
        panel.set_xticks(label_positions)
        panel.set_xticklabels(label_texts)
        panel.set_xlabel("resolution of the mesh", fontsize=9.0)
        panel.tick_params(axis="y", labelsize=8.0)
        panel.grid(True, linewidth=0.4, alpha=0.35)

    value_panel.set_ylabel("area from the mesh", fontsize=9.0)
    value_legend = value_panel.legend(fontsize=7.6, loc="center right", framealpha=0.92,
                                      borderpad=0.35, handlelength=1.8)
    value_panel.set_title("each mesh under-estimates its closed form", fontsize=8.6)

    error_panel.set_yscale("log")
    error_panel.set_ylabel("relative error", fontsize=9.0)
    error_panel.axhline(TOLERANCE_FOR_THE_FINE_MESH, color="#555555", linewidth=0.9,
                        linestyle=(0, (3.0, 2.0)))
    error_panel.set_yticks([1.0e-4, 1.0e-3, 1.0e-2, 1.0e-1])
    error_panel.set_yticklabels(["$10^{-4}$", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$"],
                                fontsize=8.0)
    error_legend = error_panel.legend(fontsize=7.6, loc="lower left", framealpha=0.92,
                                     borderpad=0.35, handlelength=1.8)
    error_panel.set_title("dashed line: relative error $5\\times10^{-4}$", fontsize=8.6)

    check_artist_inside(figure, value_panel, value_legend)
    check_artist_inside(figure, error_panel, error_legend)

    finest = records[-1]
    for name, _, closed_form, _ in series:
        relative = abs(finest[name] - closed_form) / closed_form
        if relative >= TOLERANCE_FOR_THE_FINE_MESH:
            raise AssertionError(f"the finest {name} mesh keeps a relative error {relative:.3e}")
        print(f"finest {name} mesh: {finest[name]:.9f}, relative error {relative:.3e}", flush=True)
    for resolution, record in zip(RESOLUTIONS, records):
        print(f"resolution {resolution:4d}: total {record['total']:.9f}", flush=True)
    figure.savefig(OUTPUT_PATH, dpi=200, facecolor="white")
    print(f"wrote {OUTPUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
