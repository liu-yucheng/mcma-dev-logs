"""Plot the cylinder y**2 + z**2 = 9 between x = -2 and x = 2 with one label per surface."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import proj3d

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
X = np.linspace(-2, 2, 40)
T = np.linspace(0, 2*np.pi, 90)
XG, TG = np.meshgrid(X, T)
ax.plot_surface(XG, 3*np.cos(TG), 3*np.sin(TG), cmap="viridis", alpha=0.85)
R = np.linspace(0, 3, 30)
RG, TG2 = np.meshgrid(R, T)
for x0 in (-2, 2):
    ax.plot_surface(np.full_like(RG, float(x0)), RG*np.cos(TG2), RG*np.sin(TG2),
                    color="#f4a261", alpha=0.55)
ax.set_xlim(-2, 2)
ax.set_ylim(-3.6, 3.6)
ax.set_zlim(-3.6, 3.6)
ax.view_init(elev=18, azim=-65)
fig.canvas.draw()

def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)

put((0.0, -3.0, 0.0), "y^2 + z^2 = 9")
put((-2.0, 0.0, 0.0), "x = -2")
put((2.0, 0.0, 0.0), "x = 2")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("part1_figure1.png", dpi=150)
print("figure saved")
