"""Set comparison between the limits of an order and the half-spaces of E.

A printed set of limits is correct only when it describes the same set of points as the
four half-spaces. This module compares the two descriptions on random points and on a
list of boundary points, where a wrong bound shows first.

Constants:
    BOUNDARY_POINTS: Points on a face, on an edge, at a vertex, and just outside E.
    RANDOM_COUNT: The number of random points of one comparison.
    RANDOM_SEED: The random seed of the reported result.
"""

import numpy as np

import orders
import solid

RANDOM_COUNT = 300_000
RANDOM_SEED = 20261123

BOUNDARY_POINTS = np.array(
    [
        [2.0, 2.0, 0.0],
        [2.0, 2.0, 1.0],
        [2.0, 0.0, 0.0],
        [0.0, 2.0, 0.0],
        [2.0, 1.0, 0.0],
        [1.0, 2.0, 0.0],
        [1.0, 1.0, 0.0],
        [1.5, 1.5, 0.5],
        [2.0, 2.0, 0.5],
        [2.0, 1.0, 0.5],
        [2.0, 0.0, 0.0],
        [1.0, 2.0, 0.5],
        [0.0, 2.0, 0.0],
        [1.5, 1.5, 0.25],
        [0.0, 0.0, 0.0],
        [2.0, 0.0, 0.5],
        [0.0, 2.0, 0.5],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [2.0, 2.0, 1.5],
        [2.5, 2.0, 0.0],
        [2.0, 2.5, 0.0],
        [0.5, 0.5, 0.0],
        [1.0, 1.0, 0.5],
    ]
)


def agreement(order_name):
    """Compare the membership of one order with the membership of the half-spaces.

    Args:
        order_name: The order in words, such as "dz dx dy".

    Returns:
        A tuple of the number of agreeing points and the number of compared points.
    """
    membership = orders.ORDERS[order_name]["membership"]
    generator = np.random.default_rng(RANDOM_SEED)
    random_points = generator.uniform(solid.BOX_LOWER, solid.BOX_UPPER, size=(RANDOM_COUNT, 3))
    points = np.vstack([random_points, BOUNDARY_POINTS])
    from_limits = membership(points[:, 0], points[:, 1], points[:, 2])
    from_half_spaces = solid.contains(points)
    return int(np.count_nonzero(from_limits == from_half_spaces)), int(points.shape[0])


def outside_count(order_name):
    """Return how many boundary points the limits place outside E, as a witness.

    Args:
        order_name: The order in words, such as "dz dx dy".

    Returns:
        The number of boundary points that the half-spaces reject.
    """
    from_half_spaces = solid.contains(BOUNDARY_POINTS)
    return int(np.count_nonzero(~from_half_spaces))
