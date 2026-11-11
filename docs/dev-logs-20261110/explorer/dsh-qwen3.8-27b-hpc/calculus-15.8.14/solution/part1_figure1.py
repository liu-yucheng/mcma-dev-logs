"""3D picture of the solid enclosed by z = x^2 + y^2 and z = 5 - x^2 - y^2.

The two paraboloids meet along the circle r = sqrt(5/2) at height
z = 5/2; the solid sits between them.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

r_star = np.sqrt(5.0 / 2.0)
rp, tp = np.meshgrid(np.linspace(0, r_star, 60), np.linspace(0, 2 * np.pi, 90))
xp = rp * np.cos(tp)
yp = rp * np.sin(tp)

# lower paraboloid z = r^2
zl = rp**2
ax_surf_l = None
fig = plt.figure(figsize=(7.2, 5.8))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(xp, yp, zl, color="#e0a04a", alpha=0.9, rstride=2, cstride=2)

# upper paraboloid z = 5 - r^2
zu = 5 - rp**2
ax.plot_surface(xp, yp, zu, color="#7fb069", alpha=0.9, rstride=2, cstride=2)

# intersection circle r = r_star at z = 5/2
tc = np.linspace(0, 2 * np.pi, 200)
ax.plot(r_star * np.cos(tc), r_star * np.sin(tc),
        np.full_like(tc, 2.5), color="#c0504d", lw=2)

# vertices
ax.scatter([0], [0], [0], color="k", s=25, zorder=5)
ax.scatter([0], [0], [5], color="k", s=25, zorder=5)
ax.text(0.15, 0.15, 0.1, r"$(0,0,0)$", fontsize=11)
ax.text(0.15, 0.15, 5.1, r"$(0,0,5)$", fontsize=11)
ax.text(r_star * 0.72, r_star * 0.72, 2.55,
        r"$r=\sqrt{5/2}, z=5/2$", fontsize=11, color="#c0504d")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title(rf"15.8.14: solid between $z=x^2+y^2$ and $z=5-x^2-y^2$")
ax.set_box_aspect((2.0, 2.0, 2.2))
fig.tight_layout()
fig.savefig("calculus-15.8.14/solution/part1_figure1.png", dpi=150)
print("saved figure 1")
