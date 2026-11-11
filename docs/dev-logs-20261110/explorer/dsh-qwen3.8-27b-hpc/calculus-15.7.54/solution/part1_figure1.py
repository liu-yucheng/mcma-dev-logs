"""3D sketch of the solid E for problem 15.7.54.

E is the region under the paraboloid z = 1 - x^2 - y^2 (vertex (0,0,1),
meets z = 0 at the unit circle) and above the plane z = 0.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

fig = plt.figure(figsize=(7.2, 5.6))
ax = fig.add_subplot(111, projection="3d")

rp, tp = np.meshgrid(np.linspace(0, 1, 60), np.linspace(0, 2 * np.pi, 90))
xp = rp * np.cos(tp)
yp = rp * np.sin(tp)
zp = 1 - rp**2
ax.plot_surface(xp, yp, zp, color="#7fb069", alpha=0.9, rstride=2, cstride=2)

# base disk in the plane z = 0
xb = rp * np.cos(tp)
yb = rp * np.sin(tp)
zb = np.zeros_like(xp)
ax.plot_surface(xb, yb, zb, color="#4a6fa5", alpha=0.85)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title(rf"15.7.54: $E$ between $z=0$ and the paraboloid $z=1-x^2-y^2$")
ax.set_box_aspect((2.0, 2.0, 1.3))
fig.tight_layout()
fig.savefig("calculus-15.7.54/solution/part1_figure1.png", dpi=150)
print("saved figure 1")
