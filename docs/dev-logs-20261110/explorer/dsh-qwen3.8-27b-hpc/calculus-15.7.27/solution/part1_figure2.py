import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.4))

# Left: projection on the xz plane (region of (x, z)): x + z <= 1
a1.fill([0, 1, 0], [0, 0, 1], color="tab:blue", alpha=0.25)
a1.plot([0, 1, 0, 0], [0, 0, 1, 0], "k-", lw=1.5)
a1.plot([0, 1, 0], [0, 0, 1], "o", ms=4)
a1.annotate(r"$(0,0)$", (0.03, 0.05), fontsize=11)
a1.annotate(r"$(1,0)$", (0.80, 0.08), fontsize=11)
a1.annotate(r"$(0,1)$", (0.05, 0.88), fontsize=11)
a1.text(0.35, 0.25, r"$(x,z)$", fontsize=12)
a1.set_title(r"Projection on the $xz$-plane: $x+z\leq 1$")
a1.set_xlabel(r"$x$"); a1.set_ylabel(r"$z$")
a1.set_xlim(-0.1, 1.25); a1.set_ylim(-0.1, 1.25); a1.set_aspect("equal")
a1.grid(alpha=0.3)

# Right: cross section at fixed x (yz plane): 0 <= y <= 2 - 2z
a2.fill([0, 0, 1], [0, 2, 0], color="tab:green", alpha=0.25)
a2.plot([0, 0, 1, 0], [0, 2, 0, 0], "k-", lw=1.5)
a2.plot([0, 0, 1], [0, 2, 0], "o", ms=4)
a2.annotate(r"$(0,0)$", (0.04, 0.1), fontsize=11)
a2.annotate(r"$(0,2)$", (0.06, 1.85), fontsize=11)
a2.annotate(r"$(1,0)$", (0.82, 0.1), fontsize=11)
a2.text(0.3, 0.6, r"$(z,y)$", fontsize=12)
a2.set_title(r"Cross section at fixed $x$: $0\leq y\leq 2-2z$")
a2.set_xlabel(r"$z$"); a2.set_ylabel(r"$y$")
a2.set_xlim(-0.1, 1.25); a2.set_ylim(-0.1, 2.3); a2.set_aspect("auto")
a2.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.27/solution/part1_figure2.png", dpi=150)
print("wrote part1_figure2.png (27)")
