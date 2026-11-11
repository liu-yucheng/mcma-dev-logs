import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure(figsize=(9, 6.5))
ax = fig.add_subplot(111, projection="3d")

# Pentagon (pentahedron) solid E with 5 vertices:
V000 = (0, 0, 0); V100 = (1, 0, 0); V001 = (0, 0, 1)
V020 = (0, 2, 0); V120 = (1, 2, 0)

faces = [
    # base triangle y = 0
    ([V000, V100, V001], "tab:blue", 0.35),
    # top triangle y = 2 - 2z
    ([V020, V120, V001], "tab:green", 0.60),
    # side z = 0 (rectangle)
    ([V000, V100, V120, V020], "tab:purple", 0.30),
    # side x = 0 (triangle)
    ([V000, V020, V001], "tab:red", 0.55),
    # slanted side x + z = 1 (triangle)
    ([V100, V120, V001], "tab:orange", 0.60),
]
for poly, col, a in faces:
    ax.add_collection3d(Poly3DCollection([poly], facecolors=col, alpha=a,
                                         edgecolors="k", linewidths=0.8))

ax.set_title(r"Solid $E$: $0\leq x\leq 1$, $0\leq z\leq 1-x$, $0\leq y\leq 2-2z$  (volume $2/3$)")
ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_zlabel(r"$z$")
ax.set_box_aspect((1, 2, 1))
ax.set_xlim(0, 1); ax.set_ylim(0, 2); ax.set_zlim(0, 1)
ax.view_init(elev=18, azim=-60)
fig.tight_layout()
fig.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.27/solution/part1_figure1.png", dpi=150)
print("wrote part1_figure1.png (27)")
