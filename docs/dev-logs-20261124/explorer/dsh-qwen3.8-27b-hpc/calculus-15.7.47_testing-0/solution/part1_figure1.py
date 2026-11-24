"""Figure: the cylinder y = x^2 and the plane y + z = 1."""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
xx = np.linspace(-1, 1, 32)
zz = np.linspace(0, 1, 16)
XX, ZZ = np.meshgrid(xx, zz)
ax.plot_surface(XX, XX**2, ZZ, cmap="viridis", alpha=0.85)
yy = np.linspace(0, 1, 16)
XY, YY = np.meshgrid(xx, yy)
ax.plot_surface(XY, YY, 1.0 - YY, cmap="viridis", alpha=0.85)
ax.set_xlim(-1, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
fig.canvas.draw()

def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)

put((0.0, 0.0, 0.3), "cylinder y = x^2")
put((0.0, 0.05, 0.95), "plane y + z = 1")
print("labels at (0,0,0.3) and (0,0.05,0.95)")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("part1_figure1.png")
print("figure ok")
