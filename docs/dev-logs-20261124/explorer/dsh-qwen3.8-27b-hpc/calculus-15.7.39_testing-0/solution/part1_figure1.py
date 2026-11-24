import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import proj3d
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
c = plt.get_cmap("tab10")
u, v = np.meshgrid(np.linspace(0, 1, 60), np.linspace(0, 1, 60))
X1, Y1, Z1 = u**2, v * u, 1 + u**2 + v * u
ax.plot_surface(X1, Y1, Z1, color=c(0), alpha=0.85)
X2, Y2, Z2 = u**2, v * u, np.zeros_like(u)
ax.plot_surface(X2, Y2, Z2, color=c(1), alpha=0.85)
X3, T3 = np.meshgrid(np.linspace(0, 1, 40), np.linspace(0, 1, 40))
Y3 = np.sqrt(X3) * np.ones_like(T3)
Z3 = T3 * (1 + X3 + np.sqrt(X3))
ax.plot_surface(X3, Y3, Z3, color=c(2), alpha=0.85)
ax.set_xlim(0, 1.2); ax.set_ylim(-0.1, 1.1); ax.set_zlim(0, 3.2)
ax.set_box_aspect((1.2, 1.2, 3.2))
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
put((0.4, 0.4, 1.8), "z = 1 + x + y")
put((0.5, 0.2, 0.0), "D in the xy-plane")
put((0.16, 0.4, 1.2), "y = sqrt(x)")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.7.39/solution/part1_figure1.png", dpi=150)
