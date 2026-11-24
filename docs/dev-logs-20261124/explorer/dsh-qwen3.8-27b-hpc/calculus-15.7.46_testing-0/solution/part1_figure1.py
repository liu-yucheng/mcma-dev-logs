"""Figure: the cone r <= z <= h with its base disk."""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
u = np.linspace(0, 2 * np.pi, 48)
u, v = np.meshgrid(u, np.linspace(0, 2, 24))
ax.plot_surface(v * np.cos(u), v * np.sin(u), v, cmap="viridis", alpha=0.85)
th = np.linspace(0, 2 * np.pi, 72)
ax.plot(2 * np.cos(th), 2 * np.sin(th), np.full_like(th, 2.0), color="k", lw=0.7)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(0, 2)
fig.canvas.draw()

def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)

s = 1.0 / np.sqrt(2)
put((0.0, 0.0, 2.0), "base z = h")
put((s, s, 2 * s), "cone r = z")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("part1_figure1.png")
print("figure ok")
