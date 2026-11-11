"""3D sketch of the maximizing region E for problem 15.7.55.

E = {x^2 + 2 y^2 + 3 z^2 <= 1}: ellipsoid with semi-axes
1 (x), 1/sqrt(2) (y), 1/sqrt(3) (z).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

a, b, c = 1.0, 1 / np.sqrt(2), 1 / np.sqrt(3)
uu, vv = np.meshgrid(np.linspace(0, 2 * np.pi, 80), np.linspace(0, np.pi, 50))
X = a * np.sin(vv) * np.cos(uu)
Y = b * np.sin(vv) * np.sin(uu)
Z = c * np.cos(vv)

fig = plt.figure(figsize=(7.2, 5.6))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, Z, color="#7fb069", alpha=0.9, rstride=2, cstride=2)
ax.plot([0, a], [0, 0], [0, 0], "k-", lw=1.2)
ax.plot([0, 0], [0, b], [0, 0], "k-", lw=1.2)
ax.plot([0, 0], [0, 0], [0, c], "k-", lw=1.2)
ax.text(a, 0, 0, " $a=1$", fontsize=11)
ax.text(0, b, 0, r" $b=1/\sqrt{2}$", fontsize=11)
ax.text(0, 0, c, r" $c=1/\sqrt{3}$", fontsize=11)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title(rf"15.7.55: maximizing region $E$: ellipsoid $x^2+2y^2+3z^2\leq 1$")
ax.set_box_aspect((2.0, 1.8, 1.5))
fig.tight_layout()
fig.savefig("calculus-15.7.55/solution/part1_figure1.png", dpi=150)
print("saved figure 1")
