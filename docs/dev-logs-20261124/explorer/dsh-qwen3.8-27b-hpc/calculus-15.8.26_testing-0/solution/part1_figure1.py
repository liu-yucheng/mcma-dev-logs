"""Figure 1: the sphere of radius 1 and the cylinder r = cos(theta)."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import proj3d

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
u = np.linspace(0.0, 2.0 * np.pi, 70)
v = np.linspace(-np.pi / 2, np.pi / 2, 40)
UU, VV = np.meshgrid(u, v)
ax.plot_surface(np.cos(UU) * np.cos(VV), np.sin(UU) * np.cos(VV), np.sin(VV),
                cmap="viridis", alpha=0.85)
t = np.linspace(0.0, 2.0 * np.pi, 90)
w = np.linspace(-1.0, 1.0, 30)
TT, WW = np.meshgrid(t, w)
Xc = 0.5 + 0.5 * np.cos(TT)
Yc = 0.5 * np.sin(TT)
ax.plot_surface(Xc, Yc, WW, color="#9aa4b2", alpha=0.85)
ax.set_xlim(-1.25, 1.25)
ax.set_ylim(-1.25, 1.25)
ax.set_zlim(-1.25, 1.25)
ax.view_init(elev=18, azim=-65)
fig.canvas.draw()

def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)

put((0.0, 0.0, 1.0), "sphere r = 1")
put((1.0, 0.0, 0.3), "cylinder r = cos(theta)")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a_ in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    for _ in range(6):
        box = a_.get_window_extent(renderer)
        if box.x1 > ax.bbox.x1 + 1:
            a_.set_position((a_.get_position()[0] - (box.x1 - ax.bbox.x1) / (ax.bbox.x1 - ax.bbox.x0), a_.get_position()[1]))
        if box.x0 < ax.bbox.x0 - 1:
            a_.set_position((a_.get_position()[0] + (ax.bbox.x0 - 1 - box.x0) / (ax.bbox.x1 - ax.bbox.x0), a_.get_position()[1]))
        if box.y1 > ax.bbox.y1 + 1:
            a_.set_position((a_.get_position()[0], a_.get_position()[1] - (box.y1 - ax.bbox.y1) / (ax.bbox.y1 - ax.bbox.y0)))
        if box.y0 < ax.bbox.y0 - 1:
            a_.set_position((a_.get_position()[0], a_.get_position()[1] + (ax.bbox.y0 - 1 - box.y0) / (ax.bbox.y1 - ax.bbox.y0)))
        if box.x0 >= ax.bbox.x0 - 1 and box.x1 <= ax.bbox.x1 + 1 and box.y0 >= ax.bbox.y0 - 1 and box.y1 <= ax.bbox.y1 + 1:
            break
    box = a_.get_window_extent(renderer)
    name = a_.get_text() if hasattr(a_, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.8.26/solution/part1_figure1.png", dpi=150)
print("figure saved: calculus-15.8.26/solution/part1_figure1.png")
