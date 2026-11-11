"""Part 1, Figure 1 - 3D sketch of the solid for exercise 15.7.47.

Solid enclosed by the parabolic cylinder y = x^2 (curved wall, opens +y),
the plane z = 0 (bottom), and the plane z = 1 - y (top).
Region: -1 <= x <= 1,  x^2 <= y <= 1,  0 <= z <= 1 - y.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure(figsize=(8.8, 6.8))
ax = fig.add_subplot(111, projection="3d")
m = 40

# curved wall y = x^2,  -1<=x<=1, 0 <= z <= 1 - x^2
Xw, Zw = np.meshgrid(np.linspace(-1, 1, m), np.linspace(0, 1, m))
Yw = Xw**2
Zw = Zw * (1 - Xw**2)
ax.plot_surface(Xw, Yw, Zw, color="skyblue", alpha=0.9)

# bottom z = 0 over the base region  x^2 <= y <= 1
Xb, Yb = np.meshgrid(np.linspace(-1, 1, m), np.linspace(0, 1, m))
mask = Yb >= Xb**2
Zb = np.where(mask, np.zeros_like(Xb), np.nan)
ax.plot_surface(Xb, Yb, Zb, color="orange", alpha=0.8)

# top plane z = 1 - y over the same base region
Zt = np.where(mask, 1 - Yb, np.nan)
ax.plot_surface(Xb, Yb, Zt, color="lightgreen", alpha=0.85)

# outline: bottom parabola y = x^2 at z=0
xa = np.linspace(-1, 1, 60)
ax.plot(xa, xa**2, np.zeros_like(xa), "k-", lw=1.8)
# top rim: parabola y = x^2 at z = 1 - x^2 (wall meets top plane)
ax.plot(xa, xa**2, 1 - xa**2, "m-", lw=1.8)
# where top plane meets y=1 at z=0 (line y=1, z=0)
ax.plot([-1, 1], [1, 1], [0, 0], "g-", lw=1.4)

for P, name in [((0, 0, 1), r"$(0,0,1)$"), ((1, 1, 0), r"$(1,1,0)$"),
                ((-1, 1, 0), r"$(-1,1,0)$")]:
    ax.scatter(*P, color="r", s=24)
    ax.text(P[0], P[1] - 0.16, P[2] + 0.04, name, fontsize=9)

ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1.3, 1.3); ax.set_ylim(0, 1.4); ax.set_zlim(0, 1.3)
ax.view_init(elev=20, azim=-115)
ax.set_title(rf"Solid: cylinder $y=x^2$ with planes $z=0$ and $y+z=1$",
             fontsize=12)
fig.tight_layout()
fig.savefig("calculus-15.7.47/solution/part1_figure1.png", dpi=140)
print("saved part1_figure1.png")
