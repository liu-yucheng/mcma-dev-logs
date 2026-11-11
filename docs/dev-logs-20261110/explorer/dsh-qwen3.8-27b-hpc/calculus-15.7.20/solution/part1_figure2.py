"""Fig 2: cross section z=0 and the xz-disk footprint."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
ax = axes[0]
xs = np.linspace(0, 4, 60)
ax.plot(xs, xs**2, "b-", lw=2, label=r"$y=x^2$ (lower)")
ax.plot(xs, 8 - xs**2, "r-", lw=2, label=r"$y=8-x^2$ (upper)")
ax.fill(xs, xs**2, 8 - xs**2, color="lightblue", alpha=0.5)
ax.plot([2, 2], [4, 4], "ko", ms=5)
ax.annotate("$(2, 4)$", (2, 4), textcoords="offset points", xytext=(8, -14), fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"Cross section $z=0$: $y$ from $x^2$ to $8-x^2$")
ax.set_aspect("equal"); ax.grid(alpha=0.4); ax.legend(fontsize=9)

ax = axes[1]
th = np.linspace(0, 2*np.pi, 100)
ax.plot(2*np.cos(th), 2*np.sin(th), "b-", lw=2, label=r"$x^2+z^2=4$")
ax.fill(2*np.cos(th), 2*np.sin(th), color="lightblue", alpha=0.5)
ax.set_xlabel("x"); ax.set_ylabel("z")
ax.set_title(r"Footprint in the $xz$-plane: disk $x^2+z^2 \leq 4$")
ax.set_aspect("equal"); ax.grid(alpha=0.4); ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.20/solution/part1_figure2.png",
            dpi=110, bbox_inches="tight")
print("saved fig2")
