"""Check the geometry of the pyramid and estimate its volume by sampling.

The solid is the set of points (x, y, z) with 0 <= x <= 1, 0 <= z <= 1 - x, and
0 <= y <= 2 - 2 z. The script tests the five corners, measures the two projections,
measures the horizontal slices, and estimates the volume by Monte Carlo sampling.
"""

import numpy as np

CORNERS = [
    (0.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
    (1.0, 2.0, 0.0),
    (0.0, 2.0, 0.0),
    (0.0, 0.0, 1.0),
]


def inside(point):
    """Return True when the point satisfies the three inequalities of the solid.

    Args:
        point: Triple (x, y, z) of floats.

    Returns:
        True when the point lies in the solid, else False.
    """
    x, y, z = point
    return 0.0 <= x <= 1.0 and 0.0 <= z <= 1.0 - x and 0.0 <= y <= 2.0 - 2.0 * z


def main():
    """Print the corner checks, the projection areas, the slice areas, and the estimate."""
    print("corners and their membership in the solid:")
    for point in CORNERS:
        x, y, z = point
        print(
            f"  {point}: 0 <= x <= 1 is {0.0 <= x <= 1.0}, "
            f"0 <= z <= 1 - x is {0.0 <= z <= 1.0 - x}, "
            f"0 <= y <= 2 - 2 z is {0.0 <= y <= 2.0 - 2.0 * z}"
        )

    triangle = 0.5 * 1.0 * 1.0
    rectangle = 1.0 * 2.0
    print(f"area of the projection onto the xz-plane (triangle): {triangle:.3f}")
    print(f"area of the projection onto the xy-plane (rectangle): {rectangle:.3f}")

    print("horizontal slices: the rectangle 0 <= x <= 1 - z and 0 <= y <= 2 - 2 z")
    for height in (0.0, 0.5, 1.0):
        width = 1.0 - height
        length = 2.0 - 2.0 * height
        print(f"  z = {height:3.1f}: x from 0 to {width:.3f}, y from 0 to {length:.3f}, "
              f"area {width * length:.3f}")

    generator = np.random.default_rng(seed=2026)
    count = 1_000_000
    sample = generator.random((count, 3))
    points = np.column_stack((sample[:, 0], 2.0 * sample[:, 1], sample[:, 2]))
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    hits = (z <= 1.0 - x) & (y <= 2.0 - 2.0 * z)
    box_volume = 1.0 * 2.0 * 1.0
    volumes = box_volume * hits.astype(float)
    estimate = volumes.mean()
    standard_error = volumes.std(ddof=1) / np.sqrt(count)
    exact = 2.0 / 3.0
    print(f"Monte Carlo volume estimate over the box: {estimate:.6f}")
    print(f"exact value 2/3:                          {exact:.6f}")
    print(f"estimated standard error:                 {standard_error:.6f}")
    print(f"deviation in standard errors:             {(estimate - exact) / standard_error:+.2f}")


if __name__ == "__main__":
    main()
