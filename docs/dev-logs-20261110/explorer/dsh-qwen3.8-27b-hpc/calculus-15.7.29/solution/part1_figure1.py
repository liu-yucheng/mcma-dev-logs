import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure(figsize=(9, 6.5))
ax = fig.add_subplot(111, projection="3d")

# Elliptic paraboloid y = 4 - x^2 - 4 z^2, vertex (0,4,0), cap at y = 0
r = np.linspace(0, 1, 40)
th = np.linspace(0, 2*np.pi, 80)
R, T = np.meshgrid(r, th)
X = 2 * R * np.cos(T)
Z = 1 * R * np.sin(T)
Y = 4 - X**2 - 4 * Z**2
ax.plot_surface(X, Y, Z, color="tab:green", alpha=0.75,
                rstride=2, cstride=2)

# Cap: ellipse x^2 + 4 z^2 = 4 in the plane y = 0
th2 = np.linspace(0, 2*np.pi, 80)
ex, ez = 2*np.cos(th2), np.sin(th2)
xe = np.concatenate([ex, [ex[0]]]); ze = np.concatenate([ez, [ez[0]]])
ax.plot(xe, np.zeros_like(xe), ze, "k-", lw=1.2)
ax.add_collection3d(Poly3DCollection(
    [[(px, 0.0, pz) for px, pz in zip(ex, ez)]],
    facecolors="tab:blue", alpha=0.35, edgecolors="tab:blue"))

ax.set_title(r"Solid $E$: $0\leq y\leq 4-x^2-4z^2$, i.e. $x^2+4z^2\leq 4$")
ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_zlabel(r"$z$")
ax.set_box_aspect((4, 4, 2))
ax.view_init(elev=15, azim=-70)
fig.tight_layout()
fig.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.29/solution/part1_figure1.png", dpi=150)
print("wrote part1_figure1.png (29)")
