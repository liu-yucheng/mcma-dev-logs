"""Figure 1: the solid between the paraboloids y = x^2 + z^2 and y = 8 - x^2 - z^2."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import proj3d
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
th = np.linspace(0, 2 * np.pi, 60)
rw = np.linspace(0, 2, 25)
T, R = np.meshgrid(th, rw)
X = R * np.cos(T)
Z = R * np.sin(T)
ax.plot_surface(X, X**2 + Z**2, Z, cmap="viridis", alpha=0.85)
ax.plot_surface(X, 8.0 - X**2 - Z**2, Z, color="#9aa4b2", alpha=0.85)
ax.set_xlim(-2.3, 2.3)
ax.set_ylim(0, 8)
ax.set_zlim(-2.3, 2.3)
ax.view_init(elev=20, azim=35)
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
put((1.5, 2.25, 0.0), "y = x$^2$+z$^2$")
put((1.1, 4.3, 0.6), "y = 8-x$^2$-z$^2$")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.7.20/solution/part1_figure1.png", dpi=150)
print("figure saved: part1_figure1.png")
