"""Plot the wedge: the cylinder y^2+z^2=1 with the planes y=x and x=1 in the first octant."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import proj3d
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
cx, ct = np.meshgrid(np.linspace(0, 1, 40), np.linspace(0, np.pi / 2, 40))
ax.plot_surface(cx, np.cos(ct), np.sin(ct), cmap="viridis", alpha=0.85)
Qx, Qz = np.meshgrid(np.linspace(0, 1, 30), np.linspace(0, 1, 30))
Z1 = np.where(Qz <= np.sqrt(np.clip(1 - Qx**2, 0, None)), Qz, np.nan)
ax.plot_surface(Qx, Qx, Z1, cmap="viridis", alpha=0.85)
Qy, Qz2 = np.meshgrid(np.linspace(0, 1, 30), np.linspace(0, 1, 30))
Z2 = np.where(Qz2 <= np.sqrt(np.clip(1 - Qy**2, 0, None)), Qz2, np.nan)
ax.plot_surface(np.ones_like(Qy), Qy, Z2, cmap="viridis", alpha=0.85)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
put((0.3, 0.6, 0.8), "cylinder $y^2+z^2=1$")
put((0.65, 0.65, 0.3), "plane $y=x$")
put((0.97, 0.35, 0.55), "plane $x=1$")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.7.23/solution/part1_figure1.png", dpi=150)
print("PASS figure")
