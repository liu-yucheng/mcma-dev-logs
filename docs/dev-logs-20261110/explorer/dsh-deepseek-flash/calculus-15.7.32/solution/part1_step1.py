"""Confirm the tetrahedron description of E and estimate its volume by sampling.

The planes x = 2, y = 2, z = 0, and x + y - 2*z = 2 meet at four vertices. This
script lists the vertices, computes the volume from the scalar triple product,
and estimates the same volume by Monte Carlo sampling.
"""

import numpy as np

vertex_a = np.array([2.0, 0.0, 0.0])
vertex_b = np.array([0.0, 2.0, 0.0])
vertex_c = np.array([2.0, 2.0, 0.0])
vertex_d = np.array([2.0, 2.0, 1.0])
vertices = [vertex_a, vertex_b, vertex_c, vertex_d]
vertex_names = ["A", "B", "C", "D"]
plane_names = ["x=2", "y=2", "z=0", "x+y-2z=2"]

for name, point in zip(vertex_names, vertices):
    print(f"vertex {name} = ({point[0]:.0f}, {point[1]:.0f}, {point[2]:.0f})")

for name, point in zip(vertex_names, vertices):
    residuals = [
        2.0 - point[0],
        2.0 - point[1],
        point[2],
        point[0] + point[1] - 2.0 * point[2] - 2.0,
    ]
    on_planes = [label for label, value in zip(plane_names, residuals) if abs(value) < 1e-12]
    print(f"vertex {name} lies on {', '.join(on_planes)}")

triple_product = np.dot(
    np.cross(vertex_b - vertex_a, vertex_c - vertex_a), vertex_d - vertex_a
)
print(f"scalar triple product = {triple_product:.6f}")
print(f"volume from the triple product = {abs(triple_product) / 6.0:.12f}")

base_area = 0.5 * float(np.linalg.norm(np.cross(vertex_b - vertex_a, vertex_c - vertex_a)))
print(f"area of the base triangle ABC = {base_area:.6f}")
print(f"height of vertex D above z = 0 = {vertex_d[2]:.6f}")
print(f"volume from base and height = {base_area * vertex_d[2] / 3.0:.12f}")

# Sample the bounding box 0 <= x <= 2, 0 <= y <= 2, 0 <= z <= 1.
generator = np.random.default_rng(20261109)
sample_count = 4000000
sample_x = generator.uniform(0.0, 2.0, sample_count)
sample_y = generator.uniform(0.0, 2.0, sample_count)
sample_z = generator.uniform(0.0, 1.0, sample_count)
inside = (sample_x + sample_y - 2.0 * sample_z) >= 2.0
box_volume = 2.0 * 2.0 * 1.0
estimate = box_volume * float(np.mean(inside))
standard_error = box_volume * float(np.std(inside)) / np.sqrt(sample_count)
print(f"Monte Carlo volume estimate = {estimate:.5f}")
print(f"standard error = {standard_error:.5f}")
print(f"deviation from 2/3 in standard errors = {(estimate - 2.0 / 3.0) / standard_error:+.2f}")

# The face z = 0 carries the base triangle, so the projection of E onto the
# xy-plane is the triangle with vertices A, B, C.
print("projection onto z = 0 is the triangle with vertices A, B, C")
