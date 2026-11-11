"""Fig 2: cross section in the yz-plane (cylinder projects to the strip -2<=z<=2)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 5.5))
z = np.linspace(-2, 2, 100)
ax.fill_between(z, -1, 4 - z, color="#bcd7f0", alpha=0.6, label="section region")
ax.plot(z, np.full_like(z, -1.0), "b-", lw=2, label=r"$y=-1$ (bottom)")
ax.plot(z, 4 - z, "r-", lw=2, label=r"$y=4-z$ (top)")
ax.set_xlabel("z"); ax.set_ylabel("y")
ax.set_xlim(-2.4, 2.4); ax.set_ylim(-1.6, 6.4)
ax.set_title(r"Cross section at fixed $x$:  $-2 leq z leq 2$,  $-1 leq y leq 4-z$")
ax.grid(alpha=0.4); ax.legend(fontsize=9, loc="upper right")
plt.tight_layout()
plt.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.22/solution/part1_figure2.png",
            dpi=110, bbox_inches="tight")
print("saved fig2")
