"""3D sketch of the solid E for problem 15.7.50.

E: first octant, y^2 + z^2 <= 9, 0 <= x <= y/3.
Surfaces: half-cylinder y = sqrt(9 - z^2) (0 <= z <= 3),
triangle in the yz-plane (x = 0), the plane x = y/3, and z = 0.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

fig = plt.figure(figsize=(7.6, 5.6))
ax = fig.add_subplot(111, projection="3d")

# 1) half-cylinder y = sqrt(9 - z^2), 0 <= z <= 3, 0 <= x <= y/3
zg = np.linspace(0, 3, 60)
xg = np.linspace(0, 1, 60)
ZG, XG = np.meshgrid(zg, xg)
YG = np.sqrt(np.maximum(9 - ZG**2, 0.0))
XG = np.minimum(XG, YG / 3.0)  # clip to x <= y/3
ax.plot_surface(XG, YG, ZG, color="#7fb069", alpha=0.85, rstride=2, cstride=2)

# 2) triangle in the plane x = 0: 0 <= y <= 3, 0 <= z <= sqrt(9 - y^2)
yg, zg2 = np.meshgrid(np.linspace(0, 3, 60), np.linspace(0, 3, 60))
keep = (yg**2 + zg2**2) <= 9
zt = np.where(keep, np.sqrt(np.maximum(9 - yg**2, 0.0)), 0.0)
# build the triangle as the region 0 <= z <= sqrt(9-y^2)
zt2 = np.minimum(zg2, np.sqrt(np.maximum(9 - yg**2, 0.0)))
keep2 = (zg2 <= np.sqrt(np.maximum(9 - yg**2, 0.0)))
zt2 = np.where(keep2, zg2, np.nan)
xt = np.zeros_like(yg)
ax.plot_surface(xt, yg, zt2, color="#e0a04a", alpha=0.85)

# 3) plane x = y/3: parameterize by (y, z) with y^2 + z^2 <= 9, 0 <= y <= 3
yp, zp = np.meshgrid(np.linspace(0, 3, 60), np.linspace(0, 3, 60))
keep3 = (yp**2 + zp**2) <= 9
xp = np.where(keep3, yp / 3.0, np.nan)
ax.plot_surface(xp, yp, zp, color="#c0504d", alpha=0.7)

# 4) bottom quarter disk in z = 0
rp, tp = np.meshgrid(np.linspace(0, 3, 40), np.linspace(0, np.pi / 2, 40))
ypb = rp * np.cos(tp)
zpb = rp * np.sin(tp)
xp = np.full_like(ypb, 0.0)
# bottom: z=0, 0 <= y <= 3, 0 <= x <= y/3
yb2 = np.linspace(0, 3, 60)
xb2 = np.linspace(0, 1, 60)
YB, XB = np.meshgrid(yb2, xb2)
XB = np.minimum(XB, YB / 3.0)
ZB = np.zeros_like(XB)
ax.plot_surface(XB, YB, ZB, color="#4a6fa5", alpha=0.85)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title(rf"15.7.50: $E$ between $x=0$ and $x=y/3$ inside the half-cylinder $y^2+z^2\leq 9$")
ax.set_box_aspect((1.1, 3.0, 3.0))
fig.tight_layout()
fig.savefig("calculus-15.7.50/solution/part1_figure1.png", dpi=150)
print("saved figure 1")
