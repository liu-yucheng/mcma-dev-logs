"""Verify the frame and the three boundary faces of Part 1.

Every check compares a value that one method computes with a value that a second method
computes: the ceiling description against the union of the two solids, a parametric point
against an implicit equation, a rim point of the cap against a rim point of the cylinder, and a
labelled anchor point against the equation of the surface that its label names.
"""

import math

import numpy as np

from figure_anchors import (
    cap_label_anchor,
    label_anchor_table,
    lateral_label_anchor,
    lower_face_label_anchor,
    rim_label_anchor,
    rim_radius_check,
)
from silo_geometry import (
    APEX_HEIGHT,
    CAP_CENTER_HEIGHT,
    CAP_RADIUS,
    CYLINDER_HEIGHT,
    CYLINDER_RADIUS,
    body_holds,
    body_holds_by_parts,
    cap_point,
    cap_residual,
    lateral_point,
    lateral_residual,
    lower_face_point,
    upper_face_point,
)
from verification_report import CheckLog

SAMPLE_COUNT = 720
"""Number of sampled angles along each closed curve."""

TOLERANCE = 1.0e-12
"""Tolerance of an algebraic identity, in the unit of length of the exercise."""

GRID_SIDE = 61
"""Number of sampled values of each coordinate in the membership comparison."""

RANDOM_SEED = 20261123
"""Seed of the random sample of the membership comparison."""


def polygon_area(points: np.ndarray) -> float:
    """Return the area of a closed polygon from the shoelace formula."""
    x_values = points[:, 0]
    y_values = points[:, 1]
    shifted_x = np.roll(x_values, -1)
    shifted_y = np.roll(y_values, -1)
    return float(0.5 * abs(np.sum(x_values * shifted_y - shifted_x * y_values)))


def membership_disagreement_count() -> int:
    """Return the number of sampled points where the two descriptions disagree."""
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.uniform(-4.0, 4.0, GRID_SIDE * GRID_SIDE * 3)
    y_values = generator.uniform(-4.0, 4.0, GRID_SIDE * GRID_SIDE * 3)
    z_values = generator.uniform(-1.0, 14.0, GRID_SIDE * GRID_SIDE * 3)
    disagreements = 0
    for x_value, y_value, z_value in zip(x_values, y_values, z_values):
        if body_holds(float(x_value), float(y_value), float(z_value)) != body_holds_by_parts(
            float(x_value), float(y_value), float(z_value)
        ):
            disagreements += 1
    return disagreements


def boundary_crossing_errors() -> tuple[int, int]:
    """Return the counts of outward steps that stay inside and inward steps that leave.

    The routine tests three faces.  A point of a face moves 0.05 along the outward normal of the
    face and 0.05 along the inward normal.  The outward point must lie outside the body and the
    inward point must lie inside the body.
    """
    outward_failures = 0
    inward_failures = 0
    step = 0.05
    for angle in np.linspace(0.0, 2.0 * math.pi, 24, endpoint=False):
        base = lower_face_point(1.5, float(angle))
        if body_holds(base[0], base[1], base[2] - step):
            outward_failures += 1
        if not body_holds(base[0], base[1], base[2] + step):
            inward_failures += 1

        wall = lateral_point(float(angle), 5.0)
        radius = math.hypot(wall[0], wall[1])
        outward_wall = (wall[0] * (1.0 + step / radius), wall[1] * (1.0 + step / radius), 5.0)
        inward_wall = (wall[0] * (1.0 - step / radius), wall[1] * (1.0 - step / radius), 5.0)
        if body_holds(*outward_wall):
            outward_failures += 1
        if not body_holds(*inward_wall):
            inward_failures += 1

        inclination = 0.9
        dome = cap_point(inclination, float(angle))
        unit = (math.sin(inclination) * math.cos(float(angle)),
                math.sin(inclination) * math.sin(float(angle)), math.cos(inclination))
        outward_dome = (dome[0] + step * unit[0], dome[1] + step * unit[1],
                        dome[2] + step * unit[2])
        inward_dome = (dome[0] - step * unit[0], dome[1] - step * unit[1],
                       dome[2] - step * unit[2])
        if body_holds(*outward_dome):
            outward_failures += 1
        if not body_holds(*inward_dome):
            inward_failures += 1
    return outward_failures, inward_failures


def main() -> None:
    """Run every check of Part 1 and write the summary table."""
    log = CheckLog("part1")
    angles = np.linspace(0.0, 2.0 * math.pi, SAMPLE_COUNT, endpoint=False)
    heights = np.linspace(0.0, CYLINDER_HEIGHT, 5)

    disagreements = membership_disagreement_count()
    log.record(
        "C1 ceiling description against the union of the two solids, "
        f"{GRID_SIDE * GRID_SIDE * 3} sampled points",
        float(disagreements),
        0.0,
        float(disagreements),
        disagreements == 0,
    )

    lateral_points = np.array(
        [lateral_point(float(angle), float(height)) for angle in angles for height in heights]
    )
    lateral_error = float(
        np.max(np.abs(lateral_points[:, 0] ** 2 + lateral_points[:, 1] ** 2 - 9.0))
    )
    log.record(
        "C2 lateral face: parametric point against the equation $x^{2}+y^{2}=9$",
        lateral_error,
        0.0,
        lateral_error,
        lateral_error < TOLERANCE,
    )

    inclinations = np.linspace(0.0, 0.5 * math.pi, 181)
    cap_points = np.array([cap_point(float(phi), float(theta))
                           for phi in inclinations for theta in angles])
    cap_error = float(
        np.max(
            np.abs(
                cap_points[:, 0] ** 2
                + cap_points[:, 1] ** 2
                + (cap_points[:, 2] - CAP_CENTER_HEIGHT) ** 2
                - CAP_RADIUS**2
            )
        )
    )
    log.record(
        "C3 cap: parametric point against $x^{2}+y^{2}+(z-10)^{2}=9$",
        cap_error,
        0.0,
        cap_error,
        cap_error < TOLERANCE,
    )

    apex = np.array(cap_point(0.0, 0.0))
    apex_error = float(np.linalg.norm(apex - np.array([0.0, 0.0, 13.0])))
    log.record(
        "C4 apex: parametric point at $\\varphi=0$ against $10+3$",
        apex_error,
        0.0,
        apex_error,
        apex_error < TOLERANCE,
    )

    rim_of_cap = np.array([cap_point(0.5 * math.pi, float(angle)) for angle in angles])
    rim_of_cylinder = np.array([lateral_point(float(angle), CYLINDER_HEIGHT) for angle in angles])
    rim_error = float(np.max(np.linalg.norm(rim_of_cap - rim_of_cylinder, axis=1)))
    log.record(
        "C5 rim: cap point at $\\varphi=\\pi/2$ against cylinder point at $z=10$",
        rim_error,
        0.0,
        rim_error,
        rim_error < TOLERANCE,
    )

    residuals = []
    for name, point, _equation in label_anchor_table():
        x_value, y_value, z_value = point
        if name == "lateral face":
            residuals.append(abs(lateral_residual(x_value, y_value, z_value)))
        elif name == "lower disk":
            residuals.append(abs(z_value))
        else:
            residuals.append(abs(cap_residual(x_value, y_value, z_value)))
    label_error = max(residuals)
    log.record(
        "C6 label anchors against the equation of their own surface",
        label_error,
        0.0,
        label_error,
        label_error < TOLERANCE,
    )

    rim_distance = rim_radius_check()
    log.record(
        "C7 rim anchor: distance from the z axis against the radius 3",
        rim_distance,
        CYLINDER_RADIUS,
        abs(rim_distance - CYLINDER_RADIUS),
        abs(rim_distance - CYLINDER_RADIUS) < TOLERANCE,
    )

    cap_anchor_above_base = cap_label_anchor()[2] - CYLINDER_HEIGHT
    log.record(
        "C8 cap anchor: height above $z=10$ against $3\\cos(44^{\\circ})$",
        cap_anchor_above_base,
        3.0 * math.cos(math.radians(44.0)),
        abs(cap_anchor_above_base - 3.0 * math.cos(math.radians(44.0))),
        abs(cap_anchor_above_base - 3.0 * math.cos(math.radians(44.0))) < TOLERANCE,
    )

    inside_disk = upper_face_point(1.6, math.radians(145.0))
    step = 0.4
    samples = []
    generator = np.random.default_rng(RANDOM_SEED)
    for _ in range(400):
        direction = generator.normal(size=3)
        direction = direction / np.linalg.norm(direction)
        samples.append(
            body_holds(
                inside_disk[0] + step * float(direction[0]),
                inside_disk[1] + step * float(direction[1]),
                inside_disk[2] + step * float(direction[2]),
            )
        )
    outside_count = 400 - sum(samples)
    log.record(
        "C9 inner disk at $z=10$: 400 points at distance 0.4 against full membership",
        float(outside_count),
        0.0,
        float(outside_count),
        outside_count == 0,
    )

    lower_boundary = np.array(
        [lower_face_point(CYLINDER_RADIUS, float(angle))[:2] for angle in angles]
    )
    lower_area = polygon_area(lower_boundary)
    lower_reference = math.pi * CYLINDER_RADIUS**2
    log.record(
        "C10 lower disk: shoelace area of 720 rim points against $\\pi R^{2}$",
        lower_area,
        lower_reference,
        abs(lower_area - lower_reference),
        abs(lower_area - lower_reference) < 1.0e-3,
    )

    outward_failures, inward_failures = boundary_crossing_errors()
    log.record(
        "C11 three faces: 72 outward steps outside against 0, 72 inward steps inside",
        float(outward_failures + inward_failures),
        0.0,
        float(outward_failures + inward_failures),
        outward_failures + inward_failures == 0,
    )

    heights_reached = [APEX_HEIGHT, max(point[2] for point in cap_points)]
    log.record(
        "C12 highest point: $10+3$ against the largest sampled cap height",
        heights_reached[1],
        heights_reached[0],
        abs(heights_reached[1] - heights_reached[0]),
        abs(heights_reached[1] - heights_reached[0]) < 1.0e-15,
    )

    print("boundary faces: lateral cylinder, lower disk, hemispherical cap", flush=True)
    print(f"labelled anchors: {len(label_anchor_table())}, "
          f"lateral anchor at {lateral_label_anchor()}", flush=True)
    print(f"lower anchor at {lower_face_label_anchor()}, "
          f"cap anchor at {cap_label_anchor()}", flush=True)
    print(f"rim anchor at {rim_label_anchor()}", flush=True)
    log.require_all_passed()
    log.write()


if __name__ == "__main__":
    main()
