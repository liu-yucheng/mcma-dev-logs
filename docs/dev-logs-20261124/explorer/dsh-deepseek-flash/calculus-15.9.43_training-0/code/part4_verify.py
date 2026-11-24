"""Verify the surface areas of the three drawn faces of Part 4.

Each check compares two computations: a product of numerical factors of a surface integral with
the closed form of the same integral, and the summed area of a triangle mesh of one face at four
resolutions with the closed form of that face.
"""

import math

from silo_geometry import (
    CAP_RADIUS,
    CYLINDER_HEIGHT,
    CYLINDER_RADIUS,
    LOWER_FACE_AREA,
    base_mesh,
    cap_mesh,
    cap_surface_area,
    cylinder_surface_area,
    exposed_surface_area,
    lateral_mesh,
    mesh_area,
)
from verification_report import CheckLog

RESOLUTIONS = (16, 32, 64, 128)
"""Resolutions of the mesh check, in cells along the closed direction."""

TOLERANCE = 1.0e-9
"""Tolerance of a product of numerical factors, in square units."""


def simpson(function, lower: float, upper: float, count: int = 20001) -> float:
    """Return the integral of a function of one variable by the composite Simpson rule."""
    if count % 2 == 0:
        count += 1
    step = (upper - lower) / (count - 1)
    total = 0.0
    for index in range(count):
        value = lower + index * step
        weight = 1.0 if index in (0, count - 1) else (4.0 if index % 2 == 1 else 2.0)
        total += weight * function(value)
    return total * step / 3.0


def face_mesh_areas(resolution: int) -> tuple[float, float, float]:
    """Return the mesh area of the lateral face, of the cap, and of the base disk."""
    lateral_nodes, lateral_triangles = lateral_mesh(resolution, resolution)
    cap_nodes, cap_triangles = cap_mesh(resolution, max(1, resolution // 2))
    base_nodes, base_triangles = base_mesh(resolution, max(1, resolution // 2))
    return (
        mesh_area(lateral_nodes, lateral_triangles),
        mesh_area(cap_nodes, cap_triangles),
        mesh_area(base_nodes, base_triangles),
    )


def main() -> None:
    """Run every check of Part 4 and write the summary table."""
    log = CheckLog("part4")

    theta_factor = simpson(lambda value: 1.0, 0.0, 2.0 * math.pi, 2001)
    height_factor = simpson(lambda value: 1.0, 0.0, CYLINDER_HEIGHT, 2001)
    lateral_numeric = theta_factor * height_factor * CYLINDER_RADIUS
    log.record(
        "C1 lateral area: $\\int\\int 3\\,dz\\,d\\theta$ by factors against $2\\pi RH$",
        lateral_numeric,
        cylinder_surface_area(),
        abs(lateral_numeric - cylinder_surface_area()),
        abs(lateral_numeric - cylinder_surface_area()) < TOLERANCE,
    )

    phi_factor = simpson(math.sin, 0.0, 0.5 * math.pi, 2001)
    cap_numeric = theta_factor * phi_factor * CAP_RADIUS**2
    log.record(
        "C2 cap area: $\\int\\int 9\\sin\\varphi\\,d\\varphi\\,d\\theta$ against $2\\pi R^{2}$",
        cap_numeric,
        cap_surface_area(),
        abs(cap_numeric - cap_surface_area()),
        abs(cap_numeric - cap_surface_area()) < TOLERANCE,
    )

    radial_factor = simpson(lambda value: value, 0.0, CYLINDER_RADIUS, 2001)
    base_numeric = theta_factor * radial_factor
    log.record(
        "C3 base area: $\\int\\int r\\,dr\\,d\\theta$ against $\\pi R^{2}$",
        base_numeric,
        LOWER_FACE_AREA,
        abs(base_numeric - LOWER_FACE_AREA),
        abs(base_numeric - LOWER_FACE_AREA) < TOLERANCE,
    )

    total_numeric = lateral_numeric + cap_numeric + base_numeric
    log.record(
        "C4 total drawn area: three numerical integrals against $87\\pi$",
        total_numeric,
        exposed_surface_area(),
        abs(total_numeric - exposed_surface_area()),
        abs(total_numeric - exposed_surface_area()) < 1.0e-6,
    )

    print("resolution | lateral mesh | cap mesh | base mesh", flush=True)
    lateral_values = []
    cap_values = []
    base_values = []
    for resolution in RESOLUTIONS:
        lateral_value, cap_value, base_value = face_mesh_areas(resolution)
        lateral_values.append(lateral_value)
        cap_values.append(cap_value)
        base_values.append(base_value)
        print(f"{resolution:10d} | {lateral_value:.9f} | {cap_value:.9f} | "
              f"{base_value:.9f}", flush=True)

    for name, values, reference in (
        ("lateral face", lateral_values, cylinder_surface_area()),
        ("cap", cap_values, cap_surface_area()),
        ("base disk", base_values, LOWER_FACE_AREA),
    ):
        errors = [abs(value - reference) for value in values]
        monotone = all(errors[index + 1] < errors[index] for index in range(len(errors) - 1))
        relative = errors[-1] / reference
        log.record(
            f"C5 {name}: mesh area at 16, 32, 64, 128 cells against the closed form",
            values[-1],
            reference,
            errors[-1],
            monotone and relative < 5.0e-4,
        )

    print(f"lateral {cylinder_surface_area():.9f}, cap {cap_surface_area():.9f}, "
          f"base {LOWER_FACE_AREA:.9f}", flush=True)
    print(f"total {exposed_surface_area():.9f}, 87*pi {87.0 * math.pi:.9f}", flush=True)
    log.require_all_passed()
    log.write()


if __name__ == "__main__":
    main()
