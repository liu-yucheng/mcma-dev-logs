"""Figure for 15.7.54: the solid under the paraboloid dome."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(5, 3.6))
ax = fig.add_subplot(111, projection='3d')
r = np.linspace(0, 1, 50); th = np.linspace(0, 2*np.pi, 80)
R, T = np.meshgrid(r, th)
ax.plot_surface(R*np.cos(T), R*np.sin(T), 1 - R**2, cmap='viridis', alpha=0.85)
ax.text2D(0.55, 0.50, "paraboloid z = 1 - r^2", transform=ax.transAxes, fontsize=8)
ax.text2D(0.35, 0.22, "plane z = 0", transform=ax.transAxes, fontsize=8)
ax.set_box_aspect((1, 1, 0.7)); ax.view_init(25, 235)
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
