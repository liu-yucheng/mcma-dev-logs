"""Fig 1: 3D solid for 15.7.21: cylinder y=x^2, floor z=0, slanted roof y+z=1."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6.5))
ax = fig.add_subplot(111, projection="3d")

# cylinder side y = x^2, 0<=z<=1-x^2
xs = np.linspace(-1, 1, 60)
zs = np.linspace(0, 1, 30)
XS, ZS = np.meshgrid(xs, zs, indexing="ij")
ax.plot_surface(XS, XS**2, ZS, alpha=0.9, color="#66a3d2", rstride=2, cstride=2)

# floor (z=0) and roof (z=1-y) over the region x^2<=y<=1  (NaN outside)
xg = np.linspace(-1, 1, 60)
yg = np.linspace(0, 1, 60)
XG, YG = np.meshgrid(xg, yg, indexing="ij")
m = XG**2 <= YG
Zfloor = np.where(m, 0.0, np.nan)
Zroof = np.where(m, 1.0 - YG, np.nan)
ax.plot_surface(XG, YG, Zfloor, alpha=0.85, color="#9ad0a0", rstride=2, cstride=2)
ax.plot_surface(XG, YG, Zroof, alpha=0.6, color="#c98ab8", rstride=2, cstride=2)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_title(rf"Exercise 15.7.21: cylinder $y=x^2$ (blue), floor $z=0$ (green), roof $y+z=1$ (purple)")
ax.view_init(elev=20, azim=-70)
plt.tight_layout()
plt.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.21/solution/part1_figure1.png",
            dpi=110, bbox_inches="tight")
print("saved fig1")
