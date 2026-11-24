"""Verify the volume of the enclosed solid with methods that are independent of the polar integral.

The first method uses washers about the vertical axis. The second method samples
points at random in a box that contains the solid. The third method compares the
volume with the volume of a cone inside the solid and the cylinder around it.

Every check prints the computed value and the expected value. A random check
also prints the standard error, and its assertion uses both the difference and
the standard error.
"""

import math

import numpy as np
from scipy.integrate import quad

# The upper surface is y = 8 - radius**2, so its constant term is 8.
UPPER_SURFACE_CONSTANT = 8.0
# The two surfaces meet at the height 4.
MEETING_HEIGHT = 4.0
# The projection of the solid is the disk of radius 2.
PROJECTION_RADIUS = 2.0
# The volume of the solid is 16 * pi.
EXPECTED_VOLUME = 16.0 * math.pi
# The numerical comparisons use this absolute tolerance.
COMPARISON_TOLERANCE = 1.0e-9
# The random check uses this seed, so that a second run repeats the result.
RANDOM_SEED = 20261122
# The random check uses this number of samples.
SAMPLE_COUNT = 400000
# The random check allows this many standard errors of deviation.
STANDARD_ERROR_FACTOR = 4.0


def washer_outer_radius_squared(height: float) -> float:
    """Return the squared radius of the upper surface at the given height."""
    return UPPER_SURFACE_CONSTANT - height


def washer_inner_radius_squared(height: float) -> float:
    """Return the squared radius of the lower surface at the given height."""
    return height


def washer_cross_section_area(height: float) -> float:
    """Return the area of the horizontal cross section of the solid at the given height."""
    return math.pi * (washer_outer_radius_squared(height) - washer_inner_radius_squared(height))


def report(name: str, computed: float, expected: float) -> None:
    """Print one checked value, its expected value, and the absolute difference."""
    difference = abs(computed - expected)
    print(f"{name}: computed = {computed:.12f}, expected = {expected:.12f}, difference = {difference:.3e}")


def main() -> None:
    """Run every independent check of the volume."""
    print(f"Part 4: independent checks (numpy {np.__version__}, seed {RANDOM_SEED})")

    # Check 1: the washer method gives the same volume.
    washer_volume, _ = quad(washer_cross_section_area, 0.0, MEETING_HEIGHT)
    report("volume from the washer method", washer_volume, EXPECTED_VOLUME)
    assert abs(washer_volume - EXPECTED_VOLUME) < COMPARISON_TOLERANCE

    # Check 2: the cross section area is positive at every height of the solid.
    heights = np.linspace(0.0, MEETING_HEIGHT, 401)
    cross_section_areas = np.array([washer_cross_section_area(height) for height in heights])
    report("smallest cross section area", float(cross_section_areas.min()), 0.0)
    report("largest cross section area", float(cross_section_areas.max()), math.pi * UPPER_SURFACE_CONSTANT)
    assert cross_section_areas.min() >= 0.0
    assert abs(cross_section_areas.max() - math.pi * UPPER_SURFACE_CONSTANT) < COMPARISON_TOLERANCE

    # Check 3: random sampling in a box gives the volume with a stated standard error.
    generator = np.random.default_rng(RANDOM_SEED)
    samples = generator.uniform(
        low=np.array([-PROJECTION_RADIUS, 0.0, -PROJECTION_RADIUS]),
        high=np.array([PROJECTION_RADIUS, UPPER_SURFACE_CONSTANT, PROJECTION_RADIUS]),
        size=(SAMPLE_COUNT, 3),
    )
    horizontal_x = samples[:, 0]
    vertical_y = samples[:, 1]
    horizontal_z = samples[:, 2]
    squared_radius = horizontal_x**2 + horizontal_z**2
    inside = (vertical_y >= squared_radius) & (vertical_y <= UPPER_SURFACE_CONSTANT - squared_radius)
    inside_fraction = float(inside.mean())
    box_volume = (2.0 * PROJECTION_RADIUS) * UPPER_SURFACE_CONSTANT * (2.0 * PROJECTION_RADIUS)
    random_volume = inside_fraction * box_volume
    standard_error = box_volume * math.sqrt(inside_fraction * (1.0 - inside_fraction) / SAMPLE_COUNT)
    reported_difference = abs(random_volume - EXPECTED_VOLUME)
    allowed_difference = STANDARD_ERROR_FACTOR * standard_error
    print(f"random check: samples = {SAMPLE_COUNT}, inside fraction = {inside_fraction:.6f}")
    print(f"random check: volume = {random_volume:.6f}, expected = {EXPECTED_VOLUME:.6f}, "
          f"difference = {reported_difference:.6f}")
    print(f"random check: standard error = {standard_error:.6f}, "
          f"allowed difference = {STANDARD_ERROR_FACTOR:.1f} * standard error = {allowed_difference:.6f}")
    assert standard_error < 0.3
    assert 0.0 < inside_fraction < 1.0
    assert reported_difference < allowed_difference

    # Check 4: the solid contains a double cone and stays inside the bounding cylinder.
    lower_heights = np.linspace(0.0, MEETING_HEIGHT, 401)
    cone_radius = lower_heights / 2.0
    paraboloid_radius = np.sqrt(lower_heights)
    report("largest excess of the cone radius over the paraboloid radius",
           float(np.max(cone_radius - paraboloid_radius)), 0.0)
    assert np.all(cone_radius <= paraboloid_radius + COMPARISON_TOLERANCE)
    # The double cone has two cones of base radius 2 and height 4.
    inscribed_cone_volume = 2.0 * math.pi * PROJECTION_RADIUS**2 * MEETING_HEIGHT / 3.0
    report("volume of the inscribed double cone", inscribed_cone_volume, 32.0 * math.pi / 3.0)
    assert abs(inscribed_cone_volume - 32.0 * math.pi / 3.0) < COMPARISON_TOLERANCE
    cylinder_volume = math.pi * PROJECTION_RADIUS**2 * UPPER_SURFACE_CONSTANT
    report("volume of the bounding cylinder", cylinder_volume, 32.0 * math.pi)
    print(f"bound check: {inscribed_cone_volume:.6f} < {EXPECTED_VOLUME:.6f} < {cylinder_volume:.6f}")
    assert inscribed_cone_volume < EXPECTED_VOLUME < cylinder_volume

    # Check 5: the volume is exactly one half of the bounding cylinder.
    report("volume of the solid", EXPECTED_VOLUME, cylinder_volume / 2.0)
    assert abs(EXPECTED_VOLUME - cylinder_volume / 2.0) < COMPARISON_TOLERANCE

    print("Part 4: all checks passed")


if __name__ == "__main__":
    main()
