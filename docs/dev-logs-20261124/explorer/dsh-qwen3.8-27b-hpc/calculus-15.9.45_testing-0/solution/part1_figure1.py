"""Figure 1.1: the bumpy sphere with m = 6 and n = 5."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
th = np.linspace(0, 2 * np.pi, 180)
ph = np.linspace(0, np.pi, 120)
TH, PH = np.meshgrid(th, ph)
rho = 1.0 + 0.2 * np.sin(6.0 * TH) * np.sin(5.0 * PH)
X = rho * np.sin(PH) * np.cos(TH)
Y = rho * np.sin(PH) * np.sin(TH)
Z = rho * np.cos(PH)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6))
cm = plt.cm.viridis
ax.plot_surface(X, Y, Z, facecolors=cm((rho - rho.min()) / (rho.max() - rho.min())), alpha=0.85)
t0, p0 = np.pi / 12, np.pi / 10
r0 = 1.0 + 0.2 * np.sin(6 * t0) * np.sin(5 * p0)
pt = (r0 * np.sin(p0) * np.cos(t0), r0 * np.sin(p0) * np.sin(t0), r0 * np.cos(p0))
ax.scatter(pt[0], pt[1], pt[2], s=8, color="white", depthshade=False)
print("label point rho = %.4f; sin(6*pi/12)*sin(5*pi/10) = %.4f" % (r0, np.sin(6 * t0) * np.sin(5 * p0)))
ax.text2D(0.02, 0.03, "surface, m = 6, n = 5", transform=ax.transAxes, fontsize=8)
fig.canvas.draw()
rn = fig.canvas.get_renderer()
ab = ax.get_window_extent(rn)
arts = list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else [])
for a in arts:
    bx = a.get_window_extent(rn)
    nm = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ab.x0 - 1 <= bx.x0 and bx.x1 <= ab.x1 + 1, nm
    assert ab.y0 - 1 <= bx.y0 and bx.y1 <= ab.y1 + 1, nm
fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "part1_figure1.png"), dpi=150)
print("saved part1_figure1.png")
