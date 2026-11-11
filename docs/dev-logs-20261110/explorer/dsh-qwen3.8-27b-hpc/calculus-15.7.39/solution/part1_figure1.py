"""Part 1, Figure 1 - 3D sketch of the solid E for exercise 15.7.39.

E: under plane z = 1 + x + y, above D = {0 <= x <= 1, 0 <= y <= sqrt(x)}.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8.8, 6.6))
ax = fig.add_subplot(111, projection="3d")

# Top: plane z = 1 + x + y over D (masked with NaN outside D)
X, Y = np.meshgrid(np.linspace(0, 1, 40), np.linspace(0, 1, 40))
Z = np.where(Y <= np.sqrt(X), 1 + X + Y, np.nan)
ax.plot_surface(X, Y, Z, color="skyblue", alpha=0.85, edgecolor="none")

# Bottom cap z = 0 over D
Xb, Yb = np.meshgrid(np.linspace(0, 1, 40), np.linspace(0, 1, 40))
Zb = np.where(Yb <= np.sqrt(Xb), np.zeros_like(Xb), np.nan)
ax.plot_surface(Xb, Yb, Zb, color="orange", alpha=0.75, edgecolor="none")

# Boundary edges of the top plane
xs = np.linspace(0, 1, 60)
ax.plot(xs, np.sqrt(xs), 1 + xs + np.sqrt(xs), "b-", lw=1.8)   # y = sqrt(x) edge
ax.plot(xs, np.zeros_like(xs), 1 + xs, "b-", lw=1.8)            # y = 0 edge
ys = np.linspace(0, 1, 30)
ax.plot(np.ones_like(ys), ys, 2 + ys, "g-", lw=1.8)             # x = 1 edge
# vertical edges down to z=0
ax.plot([0, 0], [0, 0], [1, 0], "k-", lw=0.8)
ax.plot([1, 1], [0, 0], [2, 0], "k-", lw=0.8)
ax.plot([1, 1], [1, 1], [3, 0], "k-", lw=0.8)
ax.plot([1, 1], [np.sqrt(1), np.sqrt(1)], [3, 0], "k-", lw=0.8)

for P, name in [((0, 0, 1), r"$(0,0,1)$"), ((1, 0, 2), r"$(1,0,2)$"),
                ((1, 1, 3), r"$(1,1,3)$")]:
    ax.scatter(*P, color="r", s=25)
    ax.text(P[0] + 0.03, P[1] - 0.15, P[2] - 0.15, name, fontsize=9)

ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1.35); ax.set_ylim(-0.2, 1.35); ax.set_zlim(0, 3.4)
ax.view_init(elev=20, azim=-125)
ax.set_title(rf"Solid $E$: under $z = 1+x+y$, above $D = {{(x,y): 0le xle 1, 0le ylesqrt{{x}}}}$",
             fontsize=11)
fig.tight_layout()
fig.savefig("calculus-15.7.39/solution/part1_figure1.png", dpi=140)
print("saved part1_figure1.png")
