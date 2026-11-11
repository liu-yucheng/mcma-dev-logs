"""Part 1, Figure 1 - 3D sketch of the solid E for exercise 15.7.40.

E bounded by the parabolic cylinder z = 1 - y^2 and the planes
x + z = 1, x = 0, z = 0.
Faces:
  bottom  z = 0:            0 <= x <= 1, -1 <= y <= 1
  left    x = 0:            -1 <= y <= 1, 0 <= z <= 1 - y^2
  top     z = 1 - y^2:      -1 <= y <= 1, 0 <= x <= y^2
  slant   x + z = 1:        0 <= z <= 1, -sqrt(1-z) <= y <= sqrt(1-z)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8.8, 6.6))
ax = fig.add_subplot(111, projection="3d")
m = 40

# bottom z = 0
X, Y = np.meshgrid(np.linspace(0, 1, m), np.linspace(-1, 1, m))
ax.plot_surface(X, Y, np.zeros_like(X), color="orange", alpha=0.7)

# left face x = 0: parabolic segment
Yl, T = np.meshgrid(np.linspace(-1, 1, m), np.linspace(0, 1, m))
Zl = T * (1 - Yl**2)
ax.plot_surface(np.zeros_like(Yl), Yl, Zl, color="lightblue", alpha=0.85)

# top face: parabolic cylinder z = 1 - y^2, 0 <= x <= y^2
Yt, S = np.meshgrid(np.linspace(-1, 1, m), np.linspace(0, 1, m))
Zt = 1 - Yt**2
Xt = S * Yt**2
ax.plot_surface(Xt, Yt, Zt, color="lightgreen", alpha=0.85)

# slant face x + z = 1
Zs, Ss = np.meshgrid(np.linspace(0, 1, m), np.linspace(-1, 1, m))
Ys = Ss * np.sqrt(1 - Zs)
Xs = 1 - Zs
ax.plot_surface(Xs, Ys, Zs, color="plum", alpha=0.85)

# edges
ax.plot([0, 1], [0, 0], [0, 0], "k-", lw=1.0)
ax.plot([0, 1], [1, 1], [0, 0], "k-", lw=1.0)
ax.plot([0, 1], [-1, -1], [0, 0], "k-", lw=1.0)
# top arch at x = 0
ya = np.linspace(-1, 1, 60)
ax.plot(np.zeros_like(ya), ya, 1 - ya**2, "b-", lw=1.8)
# slant top edge x = 1-z, z = 1-y^2 -> x = y^2
ax.plot(ya**2, ya, 1 - ya**2, "m-", lw=1.8)
# slant bottom edges
ax.plot([1, 1], [-1, 1], [0, 0], "k-", lw=1.0)

for P, name in [((0, 0, 0), r"$(0,0,0)$"), ((1, 0, 0), r"$(1,0,0)$"),
                ((0, 0, 1), r"$(0,0,1)$"), ((0, 1, 0), r"$(0,1,0)$")]:
    ax.scatter(*P, color="r", s=22)
    ax.text(P[0], P[1] - 0.14, P[2] - 0.08, name, fontsize=9)

ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1.25); ax.set_ylim(-1.3, 1.3); ax.set_zlim(0, 1.25)
ax.view_init(elev=20, azim=-60)
ax.set_title(rf"Solid $E$: parabolic cylinder $z = 1-y^2$ with planes "
             rf"$x+z=1$, $x=0$, $z=0$", fontsize=11)
fig.tight_layout()
fig.savefig("calculus-15.7.40/solution/part1_figure1.png", dpi=140)
print("saved part1_figure1.png")
