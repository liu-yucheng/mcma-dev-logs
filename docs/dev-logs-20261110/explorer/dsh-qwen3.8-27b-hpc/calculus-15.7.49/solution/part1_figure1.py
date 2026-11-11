"""3D sketch of the solid E for problem 15.7.49.

E: first octant, 0 <= z <= y, x^2 + y^2 <= 1.
Surfaces: quarter-cylinder x = sqrt(1-y^2), bottom disk in z = 0,
triangle in x = 0, and the plane z = y over the quarter disk.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

fig = plt.figure(figsize=(7.6, 5.6))
ax = fig.add_subplot(111, projection="3d")

# 1) quarter-cylinder x = sqrt(1 - y^2), 0 <= y <= 1, 0 <= z <= y
yg, zg = np.meshgrid(np.linspace(0, 1, 60), np.linspace(0, 1, 60))
xg = np.sqrt(np.maximum(1 - yg**2, 0.0))
ax.plot_surface(xg, yg, zg, color="#7fb069", alpha=0.85, rstride=2, cstride=2)

# 2) bottom quarter disk in the plane z = 0
rg, tg = np.meshgrid(np.linspace(0, 1, 40), np.linspace(0, np.pi / 2, 40))
xb = rg * np.cos(tg)
yb = rg * np.sin(tg)
zb = np.zeros_like(xb)
ax.plot_surface(xb, yb, zb, color="#4a6fa5", alpha=0.9)

# 3) triangle in the plane x = 0 (0 <= z <= y <= 1)
yt, zt = np.meshgrid(np.linspace(0, 1, 40), np.linspace(0, 1, 40))
zt = np.minimum(zt, yt)  # keep z <= y
xt = np.zeros_like(yt)
ax.plot_surface(xt, yt, zt, color="#e0a04a", alpha=0.85)

# 4) plane z = y over the quarter disk
rp, tp = np.meshgrid(np.linspace(0, 1, 40), np.linspace(0, np.pi / 2, 40))
xp = rp * np.cos(tp)
yp = rp * np.sin(tp)
zp = yp
ax.plot_surface(xp, yp, zp, color="#c0504d", alpha=0.7)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title(rf"15.7.49: $E$ between $z=0$ and $z=y$ over the quarter disk $x^2+y^2\leq 1$")
ax.set_box_aspect((1.3, 1.3, 0.9))
fig.tight_layout()
fig.savefig("calculus-15.7.49/solution/part1_figure1.png", dpi=150)
print("saved figure 1")
