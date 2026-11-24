"""Figure of the solid: 0 <= y <= 2, 0 <= z <= 2 - y, 0 <= x <= 4 - y**2."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import proj3d
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
cmap = plt.cm.viridis
Y, U = np.meshgrid(np.linspace(0, 2, 30), np.linspace(0, 1, 30))
XT = U * (4 - Y**2)
ax.plot_surface(XT, Y, 2 - Y, color=cmap(0.9), alpha=0.85)
ax.plot_surface(XT, Y, np.zeros_like(XT), color=cmap(0.6), alpha=0.85)
Y2, V = np.meshgrid(np.linspace(0, 2, 30), np.linspace(0, 1, 30))
ax.plot_surface(4 - Y2**2, Y2, V * (2 - Y2), color=cmap(0.45), alpha=0.85)
ax.plot_surface(np.zeros_like(Y2), Y2, V * (2 - Y2), color=cmap(0.3), alpha=0.85)
X3, Z3 = np.meshgrid(np.linspace(0, 4, 30), np.linspace(0, 2, 30))
ax.plot_surface(X3, np.zeros_like(X3), Z3, color=cmap(0.15), alpha=0.85)
ax.set_xlim(0, 4); ax.set_ylim(0, 2); ax.set_zlim(0, 2)
ax.set_box_aspect((4, 2, 2))
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
put((2.0, 0.0, 1.0), "y = 0")
put((3.0, 1.0, 0.5), "x = 4 - y^2")
put((2.0, 0.8, 1.2), "z = 2 - y")
put((2.0, 0.5, 0.0), "z = 0")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.7.28/solution/part1_figure1.png", dpi=150)
print("figure saved")
