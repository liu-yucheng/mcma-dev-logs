"""Draw Figure 2: the area of the horizontal section as a function of the height.

The left panel shows the area of the section through the whole body.  The right panel shows the
same curve as a fraction of the largest area, with the three heights of the verification script
marked.  The script checks that each legend and each annotation stays inside its axes box.

It writes the figure to ``code/figures/part2_figure1.png``.
"""

import pathlib

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from silo_geometry import (
    APEX_HEIGHT,
    CYLINDER_HEIGHT,
    CYLINDER_RADIUS,
    LOWER_FACE_AREA,
    section_area,
)

matplotlib.rcParams["font.family"] = "Cambria"
matplotlib.rcParams["mathtext.fontset"] = "custom"
matplotlib.rcParams["mathtext.rm"] = "XITS"
matplotlib.rcParams["mathtext.it"] = "XITS:italic"

OUTPUT_PATH = pathlib.Path(__file__).resolve().parent / "figures" / "part2_figure1.png"
"""Path of the drawn figure."""

MARKED_HEIGHTS = (3.0, 10.0, 11.5)
"""Heights whose area the verification script prints and the figure marks."""

HEIGHT_COUNT = 1301
"""Number of heights of the drawn curve."""


def check_artist_inside(figure, axes, artists) -> None:
    """Assert that each artist lies inside the box of its axes."""
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    for artist in artists:
        extent = artist.get_window_extent(renderer=renderer)
        box = axes.bbox
        if not (
            extent.x0 >= box.x0 - 1.5
            and extent.x1 <= box.x1 + 1.5
            and extent.y0 >= box.y0 - 1.5
            and extent.y1 <= box.y1 + 1.5
        ):
            raise AssertionError(
                f"artist {artist.get_text()!r} leaves the axes box: {extent.bounds}"
            )


def main() -> None:
    """Draw the figure and write the PNG file."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    heights = np.linspace(0.0, APEX_HEIGHT, HEIGHT_COUNT)
    areas = np.array([section_area(float(height)) for height in heights])

    figure, (area_panel, fraction_panel) = plt.subplots(
        1, 2, figsize=(9.6, 3.9), dpi=200, gridspec_kw={"width_ratios": (1.25, 1.0)}
    )
    figure.subplots_adjust(left=0.085, right=0.985, top=0.88, bottom=0.16, wspace=0.30)

    area_panel.plot(heights, areas, color="#1d4f7a", linewidth=1.6,
                    label="$A(z)$ from the defining inequalities")
    area_panel.axhline(LOWER_FACE_AREA, color="#8a8a8a", linewidth=0.9,
                       linestyle=(0, (4.0, 2.0)),
                       label=f"$\\pi r^{{2}}={LOWER_FACE_AREA:.6f}$")
    area_panel.axvline(CYLINDER_HEIGHT, color="#b04a4a", linewidth=0.9,
                       linestyle=(0, (2.0, 1.6)),
                       label=f"$z={CYLINDER_HEIGHT:.0f}$: the rim")
    for height in MARKED_HEIGHTS:
        area_panel.plot([height], [section_area(height)], marker="o", markersize=3.4,
                        color="#b04a4a", linestyle="none")
    area_panel.set_xlabel("height $z$", fontsize=9.0)
    area_panel.set_ylabel("area of the section $A(z)$", fontsize=9.0)
    area_panel.tick_params(labelsize=8.0)
    area_panel.grid(True, linewidth=0.4, alpha=0.4)
    legend = area_panel.legend(fontsize=7.2, loc="lower left", framealpha=0.92,
                              borderpad=0.35, handlelength=1.8)
    area_panel.set_title("constant area below $z=10$, then $\\pi(9-(z-10)^{2})$",
                         fontsize=8.6)
    area_panel.annotate(
        f"$A(11.5)={section_area(11.5):.6f}$",
        xy=(11.5, section_area(11.5)),
        xytext=(-96.0, 26.0),
        textcoords="offset points",
        fontsize=7.6,
        color="#7a2020",
        arrowprops={"arrowstyle": "-", "linewidth": 0.7, "color": "#7a2020"},
    )

    fraction_panel.plot(heights, areas / LOWER_FACE_AREA, color="#1d4f7a", linewidth=1.6,
                        label=f"$A(z)/(\\pi r^{{2}})$, $r={CYLINDER_RADIUS:.0f}$")
    for height in MARKED_HEIGHTS:
        fraction_panel.plot([height], [section_area(height) / LOWER_FACE_AREA], marker="o",
                            markersize=3.4, color="#b04a4a", linestyle="none")
        fraction_panel.annotate(f"$z={height:.1f}$", xy=(height,
                                                         section_area(height) / LOWER_FACE_AREA),
                                xytext=(4.0, -9.0), textcoords="offset points",
                                fontsize=7.4, color="#7a2020")
    fraction_panel.set_xlabel("height $z$", fontsize=9.0)
    fraction_panel.set_ylabel("$A(z)/A(0)$", fontsize=9.0)
    fraction_panel.tick_params(labelsize=8.0)
    fraction_panel.grid(True, linewidth=0.4, alpha=0.4)
    fraction_legend = fraction_panel.legend(fontsize=7.2, loc="lower left",
                                            framealpha=0.92, borderpad=0.35)
    fraction_panel.set_title("the cap removes area as the height grows", fontsize=8.6)

    check_artist_inside(figure, area_panel, [legend])
    check_artist_inside(figure, area_panel, list(area_panel.texts))
    check_artist_inside(figure, fraction_panel, [fraction_legend])
    check_artist_inside(figure, fraction_panel, list(fraction_panel.texts))

    for height in MARKED_HEIGHTS:
        print(f"height {height:.2f}: area {section_area(height):.9f}, "
              f"fraction {section_area(height) / LOWER_FACE_AREA:.9f}", flush=True)
    print(f"largest area {max(areas):.9f} at the height of constant area", flush=True)
    figure.savefig(OUTPUT_PATH, dpi=200, facecolor="white")
    print(f"wrote {OUTPUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
