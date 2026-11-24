"""Figure 1.1: the solid E under the plane z = y inside the quarter cylinder."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

theta = np.linspace(0, np.pi / 2, 40)
rad = np.linspace(0, 1, 24)
th, rr = np.meshgrid(theta, rad)
x, y = rr * np.cos(th), rr * np.sin(th)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6))
cmap = plt.get_cmap("viridis")
ax.plot_surface(x, y, np.zeros_like(x), cmap=cmap, alpha=0.85, rstride=2, cstride=2)
ax.plot_surface(x, y, y, cmap=cmap, alpha=0.85, rstride=2, cstride=2)
ts, ss = np.meshgrid(np.linspace(0, np.pi / 2, 40), np.linspace(0, 1, 30))
ax.plot_surface(np.cos(ts), np.sin(ts), ss * np.sin(ts), cmap=cmap, alpha=0.85)
ax.plot(np.cos(theta), np.sin(theta), np.sin(theta), color="k", lw=0.8)
ax.text2D(0.05, 0.1, "z = 0", transform=ax.transAxes, fontsize=8)
ax.text2D(0.5, 0.75, "z = y", transform=ax.transAxes, fontsize=8)
ax.text2D(0.62, 0.25, "x^2 + y^2 = 1", transform=ax.transAxes, fontsize=8)
ax.set_box_aspect((1, 1, 1))
fig.savefig("calculus-15.7.49/solution/part1_figure1.png", dpi=150)
figure, axes = fig, ax
figure.canvas.draw()
renderer = figure.canvas.get_renderer()
artists = list(axes.texts) + ([axes.get_legend()] if axes.get_legend() else [])
for artist in artists:
    box = artist.get_window_extent(renderer)
    name = artist.get_text() if hasattr(artist, "get_text") else "legend"
    assert axes.bbox.x0 - 1 <= box.x0 and box.x1 <= axes.bbox.x1 + 1, name
    assert axes.bbox.y0 - 1 <= box.y0 and box.y1 <= axes.bbox.y1 + 1, name
print("PASS figure 1.1")
