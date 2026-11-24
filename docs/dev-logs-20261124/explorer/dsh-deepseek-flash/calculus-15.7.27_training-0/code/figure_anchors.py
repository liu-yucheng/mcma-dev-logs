"""Points that the figures of the tutorial label.

Every anchor is a point that its own surface equation accepts, and every anchor
lies inside the solid. The figure scripts place a label at an anchor, and
`part3_verify.py` asserts that each anchor satisfies the equation of the face
that it names. Thus no label can float off its surface.
"""

from fractions import Fraction

from region_tools import Point

ORIGIN = (Fraction(0), Fraction(0), Fraction(0))
"""The point (0, 0, 0), the corner of the solid with x = y = z = 0."""

X_CORNER = (Fraction(1), Fraction(0), Fraction(0))
"""The point (1, 0, 0), the corner at x = 1 on the x axis."""

Z_CORNER = (Fraction(0), Fraction(0), Fraction(1))
"""The point (0, 0, 1), the highest point of the z axis in the solid."""

HIGH_ORIGIN = (Fraction(0), Fraction(2), Fraction(0))
"""The point (0, 2, 0), the corner above the origin at the top height 2."""

HIGH_X_CORNER = (Fraction(1), Fraction(2), Fraction(0))
"""The point (1, 2, 0), the corner above the x corner at the top height 2."""

VERTEX_NAMES: tuple[tuple[str, Point], ...] = (
    ("P0", ORIGIN),
    ("P1", X_CORNER),
    ("P2", Z_CORNER),
    ("P3", HIGH_ORIGIN),
    ("P4", HIGH_X_CORNER),
)
"""The five corners of the solid, with the name that the tutorial uses."""

TOP_FACE_ANCHOR: Point = (Fraction(1, 2), Fraction(3, 2), Fraction(1, 4))
"""A point of the top face. y = 3 / 2 and 2 - 2 z = 2 - 1 / 2 = 3 / 2."""

BOTTOM_FACE_ANCHOR: Point = (Fraction(1, 2), Fraction(0), Fraction(1, 4))
"""A point of the bottom face. y = 0 and x + z = 3 / 4 stays below 1."""

WALL_Z_ZERO_ANCHOR: Point = (Fraction(1, 2), Fraction(1), Fraction(0))
"""A point of the wall in the plane z = 0. y = 1 stays below 2 - 2 z = 2."""

WALL_X_ZERO_ANCHOR: Point = (Fraction(0), Fraction(3, 4), Fraction(1, 4))
"""A point of the wall in the plane x = 0. y = 3 / 4 stays below 2 - 2 z = 3 / 2."""

WALL_SUM_ONE_ANCHOR: Point = (Fraction(1, 4), Fraction(1, 4), Fraction(3, 4))
"""A point of the wall in the plane x + z = 1. y = 1 / 4 stays below 2 - 3 / 2 = 1 / 2."""

FACE_ANCHORS: tuple[tuple[str, str, Point], ...] = (
    ("top face", "y is not above 2 - 2 z", TOP_FACE_ANCHOR),
    ("bottom face", "y is not below 0", BOTTOM_FACE_ANCHOR),
    ("wall z = 0", "z is not below 0", WALL_Z_ZERO_ANCHOR),
    ("wall x = 0", "x is not below 0", WALL_X_ZERO_ANCHOR),
    ("wall x + z = 1", "z is not above 1 - x", WALL_SUM_ONE_ANCHOR),
)
"""Each face of the drawing, the half-space that owns it, and its label anchor."""

HEIGHT_SAMPLE_X = Fraction(1, 4)
"""The x value of the vertical segment that shows the height of the solid."""

HEIGHT_SAMPLE_Z = Fraction(2, 5)
"""The z value of the vertical segment that shows the height of the solid."""

HEIGHT_SEGMENT_FOOT: Point = (HEIGHT_SAMPLE_X, Fraction(0), HEIGHT_SAMPLE_Z)
"""The bottom end of the drawn height segment. y = 0."""

HEIGHT_SEGMENT_HEAD: Point = (HEIGHT_SAMPLE_X, Fraction(6, 5), HEIGHT_SAMPLE_Z)
"""The top end of the drawn height segment. y = 2 - 2 z = 2 - 4 / 5 = 6 / 5."""

PROJECTION_TRIANGLE: tuple[tuple[Fraction, Fraction], ...] = (
    (Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(1)),
)
"""The base triangle in the xz plane, as (x, z) pairs."""
