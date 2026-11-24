"""Figure for 15.7.55: the ellipsoid that maximizes the integral."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(5, 3.6))
ax = fig.add_subplot(111, projection='3d')
th = np.linspace(0, 2*np.pi, 70); ph = np.linspace(0, np.pi, 40)
T, P = np.meshgrid(th, ph)
X = np.cos(T)*np.sin(P); Y = np.cos(P)/np.sqrt(2); Z = np.sin(T)*np.sin(P)/np.sqrt(3)
ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.85)
ax.text2D(0.55, 0.45, "ellipsoid x^2 + 2y^2 + 3z^2 = 1", transform=ax.transAxes, fontsize=8)
ax.set_box_aspect((1, 0.7, 0.7)); ax.view_init(20, 250)
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
