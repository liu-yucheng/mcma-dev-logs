"""Figure for 15.7.50: the solid E under the first octant."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(5, 3.6))
ax = fig.add_subplot(111, projection='3d')
th = np.linspace(0, np.pi/2, 90); ph = np.linspace(0, np.pi/2, 25)
T, P = np.meshgrid(th, ph)
ax.plot_surface(3*np.cos(T), 3*np.sin(T), 4*P, cmap='viridis', alpha=0.85)
thw = np.linspace(0, np.pi/6, 30); zw = np.linspace(0, 3, 8)
TW, ZW = np.meshgrid(thw, zw)
ax.plot_surface(3*np.cos(TW), 9*np.sin(TW), ZW, cmap='magma', alpha=0.85)
ax.text2D(0.55, 0.42, "cylinder r = 3", transform=ax.transAxes, fontsize=8)
ax.text2D(0.30, 0.28, "wall y = 3x", transform=ax.transAxes, fontsize=8)
ax.text2D(0.72, 0.60, "plane z = 0", transform=ax.transAxes, fontsize=8)
ax.set_box_aspect((1, 1, 0.6)); ax.view_init(22, 230)
fig.savefig("solution/part1_figure1.png", dpi=150)
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
artists = list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else [])
for artist in artists:
    box = artist.get_window_extent(renderer)
    name = artist.get_text() if hasattr(artist, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
print("figure saved")
