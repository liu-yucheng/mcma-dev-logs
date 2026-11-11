import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure(figsize=(9, 6.5))
ax = fig.add_subplot(111, projection="3d")

# Cylinder y^2 + z^2 = 9 along the x-axis, -2 <= x <= 2
t = np.linspace(0, 2*np.pi, 80)
X, T = np.meshgrid(np.linspace(-2, 2, 30), t)
Y = 3 * np.cos(T)
Z = 3 * np.sin(T)
ax.plot_surface(X, Y, Z, color="tab:green", alpha=0.6,
                rstride=2, cstride=2)

# Caps: disks y^2 + z^2 <= 9 at x = -2 and x = +2
for xc, col in [(-2, "tab:blue"), (2, "tab:orange")]:
    disc = [(xc, 3*np.cos(a), 3*np.sin(a)) for a in t]
    ax.add_collection3d(Poly3DCollection([disc], facecolors=col,
                                         alpha=0.4, edgecolors=col))

ax.set_title(r"Solid $E$: $y^2+z^2\leq 9$, $-2\leq x\leq 2$")
ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_zlabel(r"$z$")
ax.set_box_aspect((4, 6, 6))
ax.view_init(elev=18, azim=-65)
fig.tight_layout()
fig.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.30/solution/part1_figure1.png", dpi=150)
print("wrote part1_figure1.png (30)")
