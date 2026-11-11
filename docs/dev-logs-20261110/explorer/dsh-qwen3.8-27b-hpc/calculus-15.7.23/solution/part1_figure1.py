"""Fig 1: 3D wedge for 15.7.23: quarter cylinder y^2+z^2=1, y<=x<=1, first octant."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6.5))
ax = fig.add_subplot(111, projection="3d")
# cylinder side: t in [0,pi/2]: y=cos t, z=sin t;  s in [0,1]: x = y + s(1-y)
t = np.linspace(0, np.pi/2, 40)
s = np.linspace(0, 1, 30)
T, S = np.meshgrid(t, s, indexing="ij")
Yc = np.cos(T)
Zc = np.sin(T)
Xc = Yc + S * (1.0 - Yc)
ax.plot_surface(Xc, Yc, Zc, alpha=0.85, color="#66a3d2", rstride=2, cstride=2)
# floor z=0: 0<=y<=1, y<=x<=1
Yg = np.linspace(0, 1, 30)
Xg = np.linspace(0, 1, 30)
YG, XG = np.meshgrid(Yg, Xg, indexing="ij")
m = XG >= YG
Zfloor = np.where(m, 0.0, np.nan)
ax.plot_surface(XG, YG, Zfloor, alpha=0.9, color="#9ad0a0", rstride=2, cstride=2)
# plane y=x: 0<=y<=1, 0<=z<=sqrt(1-y^2)
Yp = np.linspace(0, 1, 40)
Zp = np.sqrt(np.clip(1 - Yp**2, 0, None))
YP, ZPP = np.meshgrid(Yp, Zp, indexing="ij")
ax.plot_surface(YP, YP, ZPP, alpha=0.6, color="#c98ab8", rstride=2, cstride=2)
# plane x=1
ax.plot_surface(np.ones_like(YP), YP, ZPP, alpha=0.55, color="#d2b46a", rstride=2, cstride=2)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_title(rf"Exercise 15.7.23: first-octant wedge, $y^2+z^2 \leq 1$, $y \leq x \leq 1$")
ax.view_init(elev=20, azim=-115)
plt.tight_layout()
plt.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.23/solution/part1_figure1.png",
            dpi=110, bbox_inches="tight")
print("saved fig1")
