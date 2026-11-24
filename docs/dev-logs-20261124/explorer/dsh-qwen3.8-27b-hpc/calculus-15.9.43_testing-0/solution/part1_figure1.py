"""Figure 1.1: the silo with the cylinder wall, the hemisphere, and the base disk."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
th = np.linspace(0, 2 * np.pi, 160)
zw = np.linspace(0, 10, 40)
ph = np.linspace(0, np.pi / 2, 40)
TH, ZW = np.meshgrid(th, zw)
PH, TH2 = np.meshgrid(ph, th)
cw, sw, zw_ = 3 * np.cos(TH), 3 * np.sin(TH), ZW
hx = 3 * np.sin(PH) * np.cos(TH2)
hy = 3 * np.sin(PH) * np.sin(TH2)
hz = 10 + 3 * np.cos(PH)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6))
cm = plt.cm.viridis
ax.plot_surface(cw, sw, zw_, facecolors=cm(np.full(cw.shape, 0.45)), alpha=0.85)
ax.plot_surface(hx, hy, hz, facecolors=cm(np.full(hx.shape, 0.75)), alpha=0.85)
ax.plot(3 * np.cos(th), 3 * np.sin(th), np.zeros_like(th), color="black", linewidth=0.8)
p1 = (3 * np.cos(np.pi / 3), 3 * np.sin(np.pi / 3), 5.0)
p2 = (3 * np.sin(np.pi / 4) * np.cos(np.pi / 3), 3 * np.sin(np.pi / 4) * np.sin(np.pi / 3), 10 + 3 * np.cos(np.pi / 4))
p3 = (2.0, 0.0, 0.0)
pts = np.array([p1, p2, p3])
ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], s=6, color="white", depthshade=False)
ax.text2D(0.02, 0.60, "cylinder wall", transform=ax.transAxes, fontsize=8)
ax.text2D(0.55, 0.90, "hemisphere", transform=ax.transAxes, fontsize=8)
ax.text2D(0.02, 0.03, "base disk", transform=ax.transAxes, fontsize=8)
fig.canvas.draw()
rn = fig.canvas.get_renderer()
ab = ax.get_window_extent(rn)
arts = list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else [])
for a in arts:
    b = a.get_window_extent(rn)
    n = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ab.x0 - 1 <= b.x0 and b.x1 <= ab.x1 + 1, n
    assert ab.y0 - 1 <= b.y0 and b.y1 <= ab.y1 + 1, n
fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "part1_figure1.png"), dpi=150)
print("saved part1_figure1.png")
