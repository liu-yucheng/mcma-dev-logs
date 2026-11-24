import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import proj3d
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
c = plt.get_cmap("tab10")
Yc, Xc = np.meshgrid(np.linspace(-1, 1, 60), np.linspace(0, 1, 60))
ax.plot_surface(Xc * Yc**2, Yc, 1 - Yc**2, color=c(0), alpha=0.85)
T, Yp = np.meshgrid(np.linspace(0, 1, 50), np.linspace(-1, 1, 50))
ax.plot_surface(1 - T, Yp * np.sqrt(np.clip(1 - T, 0, None)), T, color=c(1), alpha=0.85)
Y0, W0 = np.meshgrid(np.linspace(-1, 1, 50), np.linspace(0, 1, 50))
ax.plot_surface(np.zeros_like(Y0), Y0, W0 * np.sqrt(np.clip(1 - Y0**2, 0, None)), color=c(2), alpha=0.85)
Xb, Yb = np.meshgrid(np.linspace(0, 1, 40), np.linspace(-1, 1, 40))
ax.plot_surface(Xb, Yb, np.zeros_like(Xb), color=c(3), alpha=0.85)
ax.set_xlim(0, 1); ax.set_ylim(-1, 1); ax.set_zlim(0, 1)
ax.set_box_aspect((1, 2, 1))
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
put((0.1, 0.5, 0.75), "z = 1 - y^2")
put((0.5, 0.3, 0.5), "x + z = 1")
put((0.0, 0.2, 0.6), "x = 0")
put((0.5, 0.0, 0.0), "z = 0")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.7.40/solution/part1_figure1.png", dpi=150)
