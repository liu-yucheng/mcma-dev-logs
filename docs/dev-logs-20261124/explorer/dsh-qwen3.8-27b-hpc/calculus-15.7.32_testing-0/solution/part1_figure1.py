"""Step figure: plot the four faces of the tetrahedron and label each face.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
V1, V2, V3, V4 = (2, 0, 0), (0, 2, 0), (2, 2, 0), (2, 2, 1)
faces = [((V1, V2, V4), "#7fb3d5"), ((V1, V3, V4), "#f7b733"),
         ((V2, V3, V4), "#fc4c02"), ((V1, V2, V3), "#3a9999")]
for tri, c in faces:
    ax.add_collection3d(Poly3DCollection([list(tri)], facecolors=[c], alpha=0.85))
ax.set_xlim(0, 2); ax.set_ylim(0, 2); ax.set_zlim(0, 1)
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
pts = [(4/3, 4/3, 1/3), (2, 4/3, 1/3), (4/3, 2, 1/3), (1.9, 1.55, 0.0)]
for p, s in zip(pts, ["x + y - 2z = 2", "x = 2", "y = 2", "z = 0"]):
    put(p, s)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts):
    box = a.get_window_extent(renderer)
    name = a.get_text()
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.7.32/solution/part1_figure1.png", dpi=150)
print("PASS FIG")
