"""Figure 1: the solid E bounded by y = x^3, z = 0, and y + 2z = 4."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

figure, axes = plt.subplots(1, 1, figsize=(5, 3.6), subplot_kw={"projection": "3d"})
cmap = plt.get_cmap("viridis")
xx = np.linspace(0, 4 ** (1 / 3), 26)
zz = np.linspace(0, 2, 26)
XW, ZW = np.meshgrid(xx, zz)
axes.plot_surface(XW, XW ** 3, np.where(ZW <= (4 - XW ** 3) / 2, ZW, np.nan), cmap=cmap, alpha=0.85)
XX, YY = np.meshgrid(xx, np.linspace(0, 4, 26))
mask = YY >= XX ** 3
axes.plot_surface(XX, YY, np.where(mask, 2 - YY / 2, np.nan), cmap=cmap, alpha=0.85)
axes.plot_surface(XX, YY, np.where(mask, np.zeros_like(YY), np.nan), cmap=cmap, alpha=0.85)
axes.set_box_aspect((4, 4, 2))
axes.view_init(elev=18, azim=-115)
axes.text2D(0.05, 0.32, "$y = x^3$", transform=axes.transAxes, fontsize=8)
axes.text2D(0.58, 0.55, "$y + 2z = 4$", transform=axes.transAxes, fontsize=8)
axes.text2D(0.28, 0.10, "$z = 0$", transform=axes.transAxes, fontsize=8)
axes.set_xlabel("$x$", fontsize=8)
axes.set_ylabel("$y$", fontsize=8)
axes.set_zlabel("$z$", fontsize=8)
figure.canvas.draw()
renderer = figure.canvas.get_renderer()
artists = list(axes.texts) + ([axes.get_legend()] if axes.get_legend() else [])
for artist in artists:
    box = artist.get_window_extent(renderer)
    name = artist.get_text() if hasattr(artist, "get_text") else "legend"
    assert axes.bbox.x0 - 1 <= box.x0 and box.x1 <= axes.bbox.x1 + 1, name
    assert axes.bbox.y0 - 1 <= box.y0 and box.y1 <= axes.bbox.y1 + 1, name
figure.savefig("calculus-15.7.31/solution/part1_figure1.png", dpi=150)
print("PASS figure")
