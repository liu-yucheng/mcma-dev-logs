"""Figure 1: the quarter cylinder y^2 + z^2 <= 9 under the plane x = y/3 in the first octant."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import proj3d
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
phi = np.linspace(0.05, np.pi / 2, 40)
ss = np.linspace(0, 1, 20)
P, S = np.meshgrid(phi, ss)
Y = 3.0 * np.cos(P)
Z = 3.0 * np.sin(P)
X = S * Y / 3.0
ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.85)
Yg = np.linspace(0, 3, 12)
Xg = np.linspace(0, 1, 12)
yg, xg = np.meshgrid(Yg, Xg)
ax.plot_surface(xg, yg, np.zeros_like(xg), color="#9aa4b2", alpha=0.85)
ax.set_xlim(0, 1.2)
ax.set_ylim(0, 3.2)
ax.set_zlim(0, 3.2)
ax.view_init(elev=18, azim=-55)
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
put((0.36, 1.08, 2.863), "cylinder y$^2$+z$^2$=9")
put((0.55, 1.65, 2.279), "plane x = y/3")
put((0.5, 1.5, 0.0), "plane z = 0")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.7.18/solution/part1_figure1.png", dpi=150)
print("figure saved: part1_figure1.png")
