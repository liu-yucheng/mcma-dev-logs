"""Shared helpers for the figures of the tutorial.

Every figure of the tutorial is exported as a PNG file under ``code/figures/``. The helpers
of this module keep the decoration clear of the data: each label is placed at a point that
the drawn object satisfies, each label is checked against the box of its axes, and each
reference line is offset from the curve that it names.

Constants:
    SURFACE_ALPHA: The opacity of a wall of the solid, above one half.
    FIGURE_DPI: The resolution of the exported PNG file.
    TEXT_FONT: The font family of the natural language of a figure.
    MATH_FONT: The mathtext font set, which stands for XITS in the page.
    FIGURE_DIRECTORY: The directory of the PNG files, relative to the code directory.
    OFFSET_CANDIDATES: The label offsets that the placement helper tries in order.
"""

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

SURFACE_ALPHA = 0.55
FIGURE_DPI = 200
TEXT_FONT = "Cambria"
MATH_FONT = "stix"
FIGURE_DIRECTORY = "figures"
OFFSET_CANDIDATES = [
    (10, 10),
    (10, -14),
    (-46, 10),
    (-46, -14),
    (16, 26),
    (16, -30),
    (-56, 26),
    (-56, -30),
    (26, 0),
    (-66, 0),
    (0, 34),
    (0, -38),
]

plt.rcParams["font.family"] = TEXT_FONT
plt.rcParams["mathtext.fontset"] = MATH_FONT
plt.rcParams["axes.unicode_minus"] = False


def figure_path(file_name):
    """Return the absolute path of one figure file.

    Args:
        file_name: The name of the PNG file, with its extension.

    Returns:
        The absolute path of the file below the figure directory.
    """
    base = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(base, FIGURE_DIRECTORY)
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, file_name)


def axes_box(axes, figure):
    """Return the pixel box of one axes.

    Args:
        axes: The axes of the figure.
        figure: The figure that holds the axes.

    Returns:
        The bounding box of the axes in display coordinates.
    """
    return axes.get_window_extent(figure.canvas.get_renderer())


def extent_of(artist, figure):
    """Return the pixel extent of one artist.

    Args:
        artist: The artist to measure.
        figure: The figure that holds the artist.

    Returns:
        The bounding box of the artist in display coordinates.
    """
    return artist.get_window_extent(figure.canvas.get_renderer())


def is_inside(extent, box, margin=1.0):
    """Report whether one extent lies inside one box with a margin.

    Args:
        extent: The extent to test.
        box: The box that must hold the extent.
        margin: The least gap in pixels between the extent and the box.

    Returns:
        True when the extent lies inside the box with the margin.
    """
    return bool(
        box.x0 + margin <= extent.x0
        and extent.x1 <= box.x1 - margin
        and box.y0 + margin <= extent.y0
        and extent.y1 <= box.y1 - margin
    )


def assert_inside(axes, figure, artists, description):
    """Assert that each artist lies inside the box of its axes.

    Args:
        axes: The axes of the figure.
        figure: The figure that holds the axes.
        artists: The artists to measure.
        description: The name of the group, used in the error message.

    Raises:
        AssertionError: When one artist leaves the box of the axes.
    """
    box = axes_box(axes, figure)
    for index, artist in enumerate(artists):
        extent = extent_of(artist, figure)
        assert is_inside(extent, box, margin=0.5), "artist %d of %s leaves the axes box" % (index, description)


def place_label(axes, figure, text, point, candidates=None, **keywords):
    """Place one label near a point and keep it inside the box of the axes.

    The helper tries each offset candidate in order and keeps the first annotation whose
    text lies inside the box of the axes. It raises an error when no candidate fits, so a
    label never leaves the figure without a report.

    Args:
        axes: The axes of the figure.
        figure: The figure that holds the axes.
        text: The text of the label.
        point: The point that the label names, in data coordinates.
        candidates: The offsets in points; the module list when omitted.
        **keywords: Further keywords for the annotation, such as arrowprops.

    Returns:
        The annotation artist.
    """
    box = axes_box(axes, figure)
    trial_list = OFFSET_CANDIDATES if candidates is None else candidates
    for offset in trial_list:
        annotation = axes.annotate(
            text,
            xy=point,
            xytext=offset,
            textcoords="offset points",
            **keywords,
        )
        figure.canvas.draw()
        if is_inside(extent_of(annotation, figure), box, margin=0.5):
            return annotation
        annotation.remove()
    raise AssertionError("no offset holds the label %r inside the axes box" % text)


def project_point(axes, point):
    """Project a point of a three dimensional axes to display coordinates.

    Args:
        axes: The three dimensional axes.
        point: The point as a sequence of three coordinates.

    Returns:
        The display coordinates as a pair of floats.
    """
    x_screen, y_screen, _ = proj3d.proj_transform(point[0], point[1], point[2], axes.get_proj())
    return axes.transData.transform((x_screen, y_screen))


def assert_points_inside(axes, figure, points, description, margin=26.0):
    """Assert that each projected point lies inside the box of a three dimensional axes.

    Args:
        axes: The three dimensional axes.
        figure: The figure that holds the axes.
        points: The points to project and to test.
        description: The name of the group, used in the error message.
        margin: The least gap in pixels between a point and the box.

    Raises:
        AssertionError: When one point leaves the box of the axes.
    """
    box = axes_box(axes, figure)
    for index, point in enumerate(points):
        display_x, display_y = project_point(axes, point)
        inside = bool(
            box.x0 + margin <= display_x <= box.x1 - margin
            and box.y0 + margin <= display_y <= box.y1 - margin
        )
        assert inside, "point %d of %s leaves the axes box at %s" % (index, description, (display_x, display_y))


def save_figure(figure, file_name):
    """Write one figure to the figure directory and close it.

    Args:
        figure: The figure to write.
        file_name: The name of the PNG file, with its extension.

    Returns:
        The absolute path of the written file.
    """
    path = figure_path(file_name)
    figure.savefig(path, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    return path
