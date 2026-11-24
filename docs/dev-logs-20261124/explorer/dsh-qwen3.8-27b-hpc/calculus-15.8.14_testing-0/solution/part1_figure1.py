"""Draw both paraboloids with labels placed through the projection recipe."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import proj3d

R = float(np.sqrt(2.5))
u = np.linspace(0.0, 2*np.pi, 120)
rr = np.linspace(0.0, R, 60)
U, RR = np.meshgrid(u, rr)
X = RR*np.cos(U); Y = RR*np.sin(U)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
ax.plot_surface(X, Y, RR**2, cmap="coolwarm", alpha=0.85)
ax.plot_surface(X, Y, 5 - RR**2, cmap="coolwarm", alpha=0.85)
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(0, 5)
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
put((1.0, 0.6, 1.36), "z=x^2+y^2")
put((1.0, 0.6, 3.64), "z=5-x^2-y^2")
put((-R, 0.0, 2.5), "z=5/2")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "legend"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.8.14/solution/part1_figure1.png", dpi=150)
