"""Plot the solid enclosed by x^2+z^2=4, y=-1, y+z=4."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import proj3d
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
th = np.linspace(0, 2*np.pi, 100)
yy = np.linspace(-1, 6, 40)
T, Y = np.meshgrid(th, yy)
mask = (Y < -1) | (Y > 4 - 2*np.sin(T))
ax.plot_surface(np.ma.masked_where(mask, 2*np.cos(T)), np.ma.masked_where(mask, Y), np.ma.masked_where(mask, 2*np.sin(T)), cmap="viridis", alpha=0.85)
rad = np.linspace(0, 2, 24)
R, TH = np.meshgrid(rad, th)
X1, Z1 = R*np.cos(TH), R*np.sin(TH)
ax.plot_surface(X1, np.full_like(X1, -1.0), Z1, cmap="viridis", alpha=0.85)
Z2 = R*np.sin(TH)
ax.plot_surface(X1, 4 - Z2, Z2, cmap="viridis", alpha=0.85)
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-1.4, 6.4); ax.set_zlim(-2.6, 2.6)
ax.legend(["x^2+z^2=4", "y=-1", "y+z=4"], loc="upper left", fontsize=8)
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
put((1.4142, 2.0, -1.4142), "x^2+z^2=4")
put((-1.2, -1.0, 0.8), "y=-1")
put((0.0, 2.1, 1.9), "y+z=4")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.7.22/solution/part1_figure1.png", dpi=150)
print("figure saved")
