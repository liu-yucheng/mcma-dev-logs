"""Draw the pyramid solid: base in z=0, apex (0,0,1)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import proj3d
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
cm = plt.cm.viridis
c = [cm(i / 4) for i in range(5)]
X, Y = np.meshgrid(np.linspace(0, 1, 8), np.linspace(0, 2, 8))
ax.plot_surface(X, Y, np.zeros_like(X), color=c[0], alpha=0.85)  # z=0
U, V = np.meshgrid(np.linspace(0, 1, 8), np.linspace(0, 1, 8))
ax.plot_surface(U, np.zeros_like(U), (1 - U) * V, color=c[1], alpha=0.85)  # y=0
W = np.linspace(0, 1, 8)
Xg, Vg = np.meshgrid(W, W)
ax.plot_surface(Xg, 2 * Xg * Vg, 1 - Xg, color=c[2], alpha=0.85)  # x+z=1
Zg, Vg2 = np.meshgrid(W, W)
ax.plot_surface((1 - Zg) * Vg2, 2 - 2 * Zg, Zg, color=c[3], alpha=0.85)  # y=2-2z
Y2 = np.linspace(0, 2, 8)
Yg, Vg3 = np.meshgrid(Y2, W)
ax.plot_surface(np.zeros_like(Yg), Yg, (1 - Yg / 2) * Vg3, color=c[4], alpha=0.85)  # x=0
ax.set_xlim(0, 1.15)
ax.set_ylim(0, 2.15)
ax.set_zlim(0, 1.15)
ax.set_xlabel("x", fontsize=8)
ax.set_ylabel("y", fontsize=8)
ax.set_zlabel("z", fontsize=8)
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
put((0.5, 1.0, 0.0), "z = 0")
put((0.4, 0.0, 0.4), "y = 0")
put((0.7, 1.0, 0.3), "x + z = 1")
put((0.3, 1.2, 0.4), "y + 2z = 2")
put((0.0, 1.0, 0.3), "x = 0")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.7.27/solution/part1_figure1.png", dpi=150)
print("figure saved")
