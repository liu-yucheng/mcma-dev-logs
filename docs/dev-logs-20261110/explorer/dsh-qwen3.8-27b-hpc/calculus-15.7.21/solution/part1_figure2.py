"""Fig 2: cross section in the yz-plane at a fixed x (triangle region)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6.5, 6))
a2 = 0.36   # example fixed x^2 value
ax.plot([0, 1], [0, 0], "b-", lw=2, label=r"$z=0$")
ax.plot([0, 1], [1, 0], "r-", lw=2, label=r"$y+z=1$")
ax.plot([a2, a2], [0, 1 - a2], "g-", lw=2, label=r"$y=x^2$ (fixed $x$)")
ax.fill([a2, 1, a2], [0, 0, 1 - a2], color="#bcd7f0", alpha=0.6)
ax.set_xlabel("y"); ax.set_ylabel("z")
ax.set_title(r"Cross section at fixed $x$:  $x^2 \leq y \leq 1$,  $0 \leq z \leq 1-y$")
ax.set_aspect("equal"); ax.grid(alpha=0.4); ax.legend(fontsize=9, loc="upper right")
plt.tight_layout()
plt.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.21/solution/part1_figure2.png",
            dpi=110, bbox_inches="tight")
print("saved fig2")
