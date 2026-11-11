import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.4))

# Left: cross section in the xy plane (z = 0): 0 <= y <= 2, 0 <= x <= 4 - y^2
yv = np.linspace(0, 2, 60)
a1.fill(np.concatenate([[0], 4 - yv**2, [0]]),
        np.concatenate([[0], yv, [2]]),
        color="tab:blue", alpha=0.25)
a1.plot(np.concatenate([[0], 4 - yv**2, [0]]),
        np.concatenate([[0], yv, [2]]), "k-", lw=1.5)
a1.text(1.2, 1.2, r"$(x,y)$", fontsize=12)
a1.annotate(r"$(4,0)$", (3.3, -0.32), fontsize=11)
a1.annotate(r"$(0,2)$", (0.12, 1.85), fontsize=11)
a1.annotate(r"$x = 4-y^2$", (2.2, 0.55), fontsize=11, rotation=-50)
a1.set_title(r"Cross section in the $xy$-plane: $0\leq x\leq 4-y^2$")
a1.set_xlabel(r"$x$"); a1.set_ylabel(r"$y$")
a1.set_xlim(-0.3, 4.5); a1.set_ylim(-0.3, 2.4); a1.set_aspect("auto")
a1.grid(alpha=0.3)

# Right: cross section at fixed x (yz plane): 0 <= z <= 2 - y
a2.fill([0, 0, 2], [0, 2, 0], color="tab:green", alpha=0.25)
a2.plot([0, 0, 2, 0], [0, 2, 0, 0], "k-", lw=1.5)
a2.plot([0, 0, 2], [0, 2, 0], "o", ms=4)
a2.annotate(r"$(0,0)$", (0.05, 0.08), fontsize=11)
a2.annotate(r"$(0,2)$", (0.08, 1.8), fontsize=11)
a2.annotate(r"$(2,0)$", (1.7, 0.15), fontsize=11)
a2.text(0.5, 0.6, r"$(y,z)$", fontsize=12)
a2.set_title(r"Cross section at fixed $x$: $0\leq z\leq 2-y$")
a2.set_xlabel(r"$y$"); a2.set_ylabel(r"$z$")
a2.set_xlim(-0.15, 2.4); a2.set_ylim(-0.15, 2.35); a2.set_aspect("equal")
a2.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.28/solution/part1_figure2.png", dpi=150)
print("wrote part1_figure2.png (28)")
