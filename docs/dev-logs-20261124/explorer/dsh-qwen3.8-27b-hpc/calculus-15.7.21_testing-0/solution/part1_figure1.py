"""Save one labeled 3D figure of the solid."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import proj3d
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(5, 3.6), dpi=150)
xg = np.linspace(-1, 1, 80)
zg = np.linspace(0, 1, 40)
X, Z = np.meshgrid(xg, zg)
Y = X ** 2
ax.plot_surface(X, Y, Z, cmap="Blues", alpha=0.85)
yg = np.linspace(0, 1, 60)
Zg = np.linspace(0, 1, 40)
Y2, Z2 = np.meshgrid(yg, Zg)
ax.plot_surface(np.zeros_like(Y2), Y2, Z2, cmap="Oranges", alpha=0.85)
xx = np.linspace(-1, 1, 80)
ax.plot(xx, np.zeros_like(xx), np.ones_like(xx) * 1, "k-", lw=1)
ax.plot(np.zeros_like(xx), xx, np.ones_like(xx) * 1, "k-", lw=1)
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-0.1, 1.1)
ax.set_zlim(0, 1.1)
ax.set_box_aspect((2.2, 1.2, 1.1))
ax.view_init(elev=22, azim=-40)
fig.canvas.draw()
def put(p, s):
    px, py, pz = proj3d.proj_transform(p[0], p[1], p[2], ax.get_proj())
    dx, dy = ax.transData.transform((px, py))
    fx = (dx - ax.bbox.x0) / (ax.bbox.x1 - ax.bbox.x0)
    fy = (dy - ax.bbox.y0) / (ax.bbox.y1 - ax.bbox.y0)
    return ax.text2D(fx, fy, s, transform=ax.transAxes, fontsize=8)
pts = [(-0.85, 0.7225, 0.4), (0.75, 0.5625, 0.4375), (0.9, 0.9, 0.0)]
labs = ["y = x^2", "y + z = 1", "z = 0"]
for p, s in zip(pts, labs):
    ok = False
    a = None
    for i in range(3):
        a = put(p, s)
        a.set_position((a.get_position()[0] + i * 0.03, a.get_position()[1] - i * 0.03))
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        b = a.get_window_extent(r)
        if ax.bbox.x0 - 1 <= b.x0 and b.x1 <= ax.bbox.x1 + 1 and ax.bbox.y0 - 1 <= b.y0 and b.y1 <= ax.bbox.y1 + 1:
            ok = True
            break
    if not ok and a is not None:
        a.remove()
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for a in list(ax.texts):
    box = a.get_window_extent(renderer)
    name = a.get_text() if hasattr(a, "get_text") else "text"
    assert ax.bbox.x0 - 1 <= box.x0 and box.x1 <= ax.bbox.x1 + 1, name
    assert ax.bbox.y0 - 1 <= box.y0 and box.y1 <= ax.bbox.y1 + 1, name
fig.savefig("calculus-15.7.21/solution/part1_figure1.png", dpi=150)
print("PASS figure")
