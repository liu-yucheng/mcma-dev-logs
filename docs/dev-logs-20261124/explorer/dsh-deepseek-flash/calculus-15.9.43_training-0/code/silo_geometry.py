"""Geometry of the silo of Exercise 43.

The exercise body says: a cylinder with radius 3 and height 10, surmounted by a hemisphere.

The frame of this tutorial puts the origin at the center of the lower face.  The z axis runs
along the axis of the cylinder, upward.  The x axis and the y axis lie in the plane of the lower
face.  The frame is a choice of the reader: the exercise prints no axis and no origin.

Two independent descriptions of the body live in this module.  The first description reads one
ceiling function over the disk of radius 3.  The second description joins the two solids of the
exercise words.  A check compares the two descriptions, so the description itself is tested.
"""

import math
from typing import Callable

CYLINDER_RADIUS = 3.0
"""Radius of the cylinder, from the words "radius 3" of the exercise body."""

CYLINDER_HEIGHT = 10.0
"""Height of the cylinder, from the words "height 10" of the exercise body."""

CAP_RADIUS = 3.0
"""Radius of the hemisphere, equal to the cylinder radius by the word "surmounted"."""

CAP_CENTER_HEIGHT = CYLINDER_HEIGHT
"""Height of the center of the hemisphere, on the upper face of the cylinder."""

APEX_HEIGHT = CYLINDER_HEIGHT + CAP_RADIUS
"""Height of the highest point of the body, at the pole of the hemisphere."""

LOWER_FACE_AREA = math.pi * CYLINDER_RADIUS**2
"""Area of the disk at the height 0, in square units."""


def ceiling_height(squared_radius: float) -> float:
    """Return the highest point of the body above the point at the given squared radius."""
    inner = max(0.0, CAP_RADIUS**2 - squared_radius)
    return CAP_CENTER_HEIGHT + math.sqrt(inner)


def body_holds(x_value: float, y_value: float, z_value: float) -> bool:
    """Return True when the point belongs to the body, through the ceiling function.

    The test reads one condition: the squared distance from the z axis is at most 9, and the
    height lies between 0 and the ceiling.  The ceiling is 10 + sqrt(9 - r**2).
    """
    squared_radius = x_value * x_value + y_value * y_value
    if squared_radius > CYLINDER_RADIUS * CYLINDER_RADIUS:
        return False
    if z_value < 0.0 or z_value > APEX_HEIGHT:
        return False
    return z_value <= ceiling_height(squared_radius)


def body_holds_by_parts(x_value: float, y_value: float, z_value: float) -> bool:
    """Return True when the point belongs to the cylinder or to the hemispherical cap.

    This is the second description.  It joins the two solids that the exercise words name, so a
    disagreement with :func:`body_holds` shows a fault in one of the two descriptions.
    """
    squared_radius = x_value * x_value + y_value * y_value
    inside_cylinder = squared_radius <= CYLINDER_RADIUS**2 and 0.0 <= z_value <= CYLINDER_HEIGHT
    inside_cap = (
        squared_radius + (z_value - CAP_CENTER_HEIGHT) ** 2 <= CAP_RADIUS**2
        and z_value >= CAP_CENTER_HEIGHT
    )
    return inside_cylinder or inside_cap


def section_radius_from_formula(height: float) -> float:
    """Return the radius of the horizontal section at a height, from the ceiling formula.

    Above the height 10 the ceiling is the sphere, so the radius solves
    ``r**2 + (height - 10)**2 = 9``.  At or below the height 10 the section is the full disk.
    """
    if height < 0.0 or height > APEX_HEIGHT:
        return 0.0
    if height <= CYLINDER_HEIGHT:
        return CYLINDER_RADIUS
    return math.sqrt(max(0.0, CAP_RADIUS**2 - (height - CAP_CENTER_HEIGHT) ** 2))


def section_radius_from_membership(height: float) -> float:
    """Return the radius of the horizontal section by a bisection on the body test.

    The routine searches the largest radius whose point on the x axis belongs to the body.  It
    reads no formula of a slice: it reads :func:`body_holds` only.
    """
    if height < 0.0 or height > APEX_HEIGHT:
        return 0.0
    if not body_holds(0.0, 0.0, height):
        return 0.0
    low = 0.0
    high = CYLINDER_RADIUS
    for _ in range(200):
        middle = 0.5 * (low + high)
        if body_holds(middle, 0.0, height):
            low = middle
        else:
            high = middle
    return 0.5 * (low + high)


def section_area(height: float) -> float:
    """Return the area of the horizontal section at a height."""
    radius = section_radius_from_formula(height)
    return math.pi * radius * radius


def slice_area_integral(lower: float, upper: float, count: int = 400001) -> float:
    """Return the integral of the section area by the composite Simpson rule."""
    if count % 2 == 0:
        count += 1
    step = (upper - lower) / (count - 1)
    total = 0.0
    for index in range(count):
        height = lower + index * step
        weight = 1.0 if index in (0, count - 1) else (4.0 if index % 2 == 1 else 2.0)
        total += weight * section_area(height)
    return total * step / 3.0


def cylinder_volume() -> float:
    """Return the volume of the cylinder of the body."""
    return math.pi * CYLINDER_RADIUS**2 * CYLINDER_HEIGHT


def cap_volume() -> float:
    """Return the volume of the hemispherical cap of the body."""
    return 2.0 / 3.0 * math.pi * CAP_RADIUS**3


def total_volume() -> float:
    """Return the volume of the body as the sum of its two solid parts."""
    return cylinder_volume() + cap_volume()


def inner_cylinder_integral() -> float:
    """Return the exact value of the radial integral of the cylindrical description.

    The integral is ``int from 0 to 3 of r * (10 + sqrt(9 - r**2)) dr``, which is 45 + 9.
    """
    return 0.5 * CYLINDER_RADIUS**2 * CYLINDER_HEIGHT + CAP_RADIUS**3 / 3.0


def cylinder_surface_area() -> float:
    """Return the area of the lateral face of the cylinder."""
    return 2.0 * math.pi * CYLINDER_RADIUS * CYLINDER_HEIGHT


def cap_surface_area() -> float:
    """Return the area of the hemispherical cap."""
    return 2.0 * math.pi * CAP_RADIUS**2


def exposed_surface_area() -> float:
    """Return the area of the three drawn faces: base disk, lateral face, and cap."""
    return LOWER_FACE_AREA + cylinder_surface_area() + cap_surface_area()


def cylinder_moment_about_height(height_of_axis: float = 0.0) -> float:
    """Return the integral of z over the cylinder of the body."""
    return LOWER_FACE_AREA * 0.5 * (CYLINDER_HEIGHT**2 - height_of_axis**2)


def cap_moment_about_base() -> float:
    """Return the exact integral of z over the hemispherical cap.

    The cap has the height 10 at its base and the height 10 + w at the height w above its base.
    The integral is ``10 * 18 * pi + pi * (81/2 - 81/4)``.
    """
    return CYLINDER_HEIGHT * cap_volume() + math.pi * (CAP_RADIUS**4 / 2.0 - CAP_RADIUS**4 / 4.0)


def volume_moment_about_base() -> float:
    """Return the exact integral of z over the whole body."""
    return cylinder_moment_about_height() + cap_moment_about_base()


def centroid_height() -> float:
    """Return the height of the centroid of the body."""
    return volume_moment_about_base() / total_volume()


def lateral_point(angle: float, height: float) -> tuple[float, float, float]:
    """Return the point of the lateral face of the cylinder at an angle and a height."""
    return (
        CYLINDER_RADIUS * math.cos(angle),
        CYLINDER_RADIUS * math.sin(angle),
        height,
    )


def cap_point(inclination: float, azimuth: float) -> tuple[float, float, float]:
    """Return the point of the cap from an inclination from its pole and an azimuth.

    The inclination lies in the interval from 0 to pi/2.  The radius is the cap radius, and the
    center of the sphere is at the height 10.
    """
    return (
        CAP_RADIUS * math.sin(inclination) * math.cos(azimuth),
        CAP_RADIUS * math.sin(inclination) * math.sin(azimuth),
        CAP_CENTER_HEIGHT + CAP_RADIUS * math.cos(inclination),
    )


def lower_face_point(radius: float, angle: float) -> tuple[float, float, float]:
    """Return the point of the lower disk at a radius and an angle."""
    return (radius * math.cos(angle), radius * math.sin(angle), 0.0)


def upper_face_point(radius: float, angle: float) -> tuple[float, float, float]:
    """Return the point of the disk at the height 10 at a radius and an angle.

    The disk at the height 10 is not a face of the body: the cap covers it.  The routine exists
    to test that statement.
    """
    return (radius * math.cos(angle), radius * math.sin(angle), CYLINDER_HEIGHT)


def lateral_residual(x_value: float, y_value: float, z_value: float) -> float:
    """Return the value of ``x**2 + y**2 - 9`` of the lateral face equation."""
    return x_value * x_value + y_value * y_value - CYLINDER_RADIUS**2


def cap_residual(x_value: float, y_value: float, z_value: float) -> float:
    """Return the value of the implicit equation of the spherical surface."""
    return (
        x_value * x_value
        + y_value * y_value
        + (z_value - CAP_CENTER_HEIGHT) ** 2
        - CAP_RADIUS**2
    )


def projection_region_from_ceiling(x_value: float, z_value: float) -> bool:
    """Return True when a point of the body at this x and this z exists, by the ceiling.

    The largest allowed squared radius is 9 - z**2 at the height of the point, so a point of the
    body with this x exists when ``z <= 10 + sqrt(9 - x**2)``.
    """
    if abs(x_value) > CYLINDER_RADIUS:
        return False
    if z_value < 0.0 or z_value > APEX_HEIGHT:
        return False
    return z_value <= ceiling_height(x_value * x_value)


def projection_region_from_shapes(x_value: float, z_value: float) -> bool:
    """Return True when the point belongs to the rectangle or to the half disk.

    The rectangle is ``|x| <= 3`` and ``0 <= z <= 10``.  The half disk is
    ``x**2 + (z - 10)**2 <= 9`` with ``z >= 10``.  This is the second description of the
    projection: it reads the silhouette that the drawing shows.
    """
    in_rectangle = abs(x_value) <= CYLINDER_RADIUS and 0.0 <= z_value <= CYLINDER_HEIGHT
    in_half_disk = (
        x_value * x_value + (z_value - CAP_CENTER_HEIGHT) ** 2 <= CAP_RADIUS**2
        and z_value >= CAP_CENTER_HEIGHT
    )
    return in_rectangle or in_half_disk


def lateral_mesh(angle_count: int, height_count: int) -> tuple[list, list]:
    """Return the nodes and the triangles of a mesh of the lateral face of the cylinder."""
    nodes = []
    for angle_index in range(angle_count):
        angle = 2.0 * math.pi * angle_index / angle_count
        for height_index in range(height_count + 1):
            height = CYLINDER_HEIGHT * height_index / height_count
            nodes.append(lateral_point(angle, height))
    triangles = []
    for angle_index in range(angle_count):
        next_angle = (angle_index + 1) % angle_count
        for height_index in range(height_count):
            lower_left = angle_index * (height_count + 1) + height_index
            lower_right = next_angle * (height_count + 1) + height_index
            triangles.append((lower_left, lower_right, lower_right + 1))
            triangles.append((lower_left, lower_right + 1, lower_left + 1))
    return nodes, triangles


def cap_mesh(angle_count: int, ring_count: int) -> tuple[list, list]:
    """Return the nodes and the triangles of a mesh of the hemispherical cap."""
    nodes = []
    for angle_index in range(angle_count):
        angle = 2.0 * math.pi * angle_index / angle_count
        for ring_index in range(ring_count + 1):
            inclination = 0.5 * math.pi * ring_index / ring_count
            nodes.append(cap_point(inclination, angle))
    triangles = []
    for angle_index in range(angle_count):
        next_angle = (angle_index + 1) % angle_count
        for ring_index in range(ring_count):
            first = angle_index * (ring_count + 1) + ring_index
            second = next_angle * (ring_count + 1) + ring_index
            triangles.append((first, second, second + 1))
            triangles.append((first, second + 1, first + 1))
    return nodes, triangles


def base_mesh(angle_count: int, radial_count: int) -> tuple[list, list]:
    """Return the nodes and the triangles of a mesh of the lower disk."""
    nodes = [(0.0, 0.0, 0.0)]
    for radial_index in range(1, radial_count + 1):
        radius = CYLINDER_RADIUS * radial_index / radial_count
        for angle_index in range(angle_count):
            angle = 2.0 * math.pi * angle_index / angle_count
            nodes.append(lower_face_point(radius, angle))
    triangles = []
    for angle_index in range(angle_count):
        next_angle = (angle_index + 1) % angle_count
        triangles.append((0, 1 + angle_index, 1 + next_angle))
    for radial_index in range(1, radial_count):
        inner_start = 1 + (radial_index - 1) * angle_count
        outer_start = 1 + radial_index * angle_count
        for angle_index in range(angle_count):
            next_angle = (angle_index + 1) % angle_count
            triangles.append(
                (inner_start + angle_index, outer_start + angle_index, outer_start + next_angle)
            )
            triangles.append(
                (inner_start + angle_index, outer_start + next_angle, inner_start + next_angle)
            )
    return nodes, triangles


def triangle_area(first: tuple, second: tuple, third: tuple) -> float:
    """Return the area of one triangle from the cross product of two of its edges."""
    first_edge = (second[0] - first[0], second[1] - first[1], second[2] - first[2])
    second_edge = (third[0] - first[0], third[1] - first[1], third[2] - first[2])
    cross = (
        first_edge[1] * second_edge[2] - first_edge[2] * second_edge[1],
        first_edge[2] * second_edge[0] - first_edge[0] * second_edge[2],
        first_edge[0] * second_edge[1] - first_edge[1] * second_edge[0],
    )
    return 0.5 * math.sqrt(cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2)


def mesh_area(nodes: list, triangles: list) -> float:
    """Return the summed area of the triangles of a mesh."""
    return sum(
        triangle_area(nodes[first], nodes[second], nodes[third])
        for first, second, third in triangles
    )


def surface_area_by_mesh(resolution: int) -> float:
    """Return the summed area of a mesh of the three faces at the given resolution."""
    lateral_nodes, lateral_triangles = lateral_mesh(resolution, resolution)
    cap_nodes, cap_triangles = cap_mesh(resolution, max(1, resolution // 2))
    base_nodes, base_triangles = base_mesh(resolution, max(1, resolution // 2))
    return (
        mesh_area(lateral_nodes, lateral_triangles)
        + mesh_area(cap_nodes, cap_triangles)
        + mesh_area(base_nodes, base_triangles)
    )


def integrate_over_sections(function: Callable[[float], float], lower: float, upper: float,
                            count: int = 200001) -> float:
    """Return the integral of a function of the height by the composite Simpson rule."""
    if count % 2 == 0:
        count += 1
    step = (upper - lower) / (count - 1)
    total = 0.0
    for index in range(count):
        height = lower + index * step
        weight = 1.0 if index in (0, count - 1) else (4.0 if index % 2 == 1 else 2.0)
        total += weight * function(height)
    return total * step / 3.0
