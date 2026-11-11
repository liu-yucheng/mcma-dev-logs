import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6.5, 6.5))
th = np.linspace(0, np.pi / 2, 100)
ax.plot(3 * np.cos(th), 3 * np.sin(th), "b-", lw=2, label=r"$y^2+z^2=9$")
YQ, ZQ = np.meshgrid(np.linspace(0, 3, 40), np.linspace(0, 3, 40))
ax.contourf(YQ, ZQ, YQ**2 + ZQ**2, levels=[0, 9], colors=["#bcd7f0"], alpha=0.5)
ax.plot([0, 3], [0, 0], "b-", lw=2)
ax.plot([0, 0], [0, 3], "b-", lw=2)
ax.plot([3, 0], [0, 3], "r--", lw=1.5, label=r"line $y=z$ (reference)")
ax.fill([0, 0, 3], [0, 3, 0], color="#bcd7f0", alpha=0.5)
ax.set_xlabel("y")
ax.set_ylabel("z")
ax.set_title(r"Domain $D$ in the $yz$-plane: quarter disk, $0 \leq z \leq \sqrt{9-y^2}$, $0 \leq y \leq 3$")
ax.set_aspect("equal")
ax.grid(True, alpha=0.4)
ax.legend(loc="upper right", fontsize=9)
plt.tight_layout()
plt.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.18/solution/part1_figure2.png",
            dpi=110, bbox_inches="tight")
print("saved fig2")

