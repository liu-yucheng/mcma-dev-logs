"""Draw a horizontal cross section of E at a fixed x for problem 15.7.17.

At height x0 the cross section is the disk y**2 + z**2 <= x0/4.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x0 = 3.0
radius = np.sqrt(x0) / 2

theta = np.linspace(0, 2 * np.pi, 300)
fig, ax = plt.subplots(figsize=(5.6, 5.2))
ax.plot(radius * np.cos(theta), radius * np.sin(theta), "b-", lw=2)
ax.fill(radius * np.cos(theta), radius * np.sin(theta), color="#cfe0f3",
        alpha=0.6)
ax.plot([0, radius * 0.7], [0, 0], "k-")
ax.annotate(r"$\sqrt{x_0/4}$", (radius * 0.5, 0.06), fontsize=13)
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_aspect("equal")
ax.set_xlabel("y")
ax.set_ylabel("z")
ax.set_title(rf"Cross section at $x_0={x0}$: disk $y^2+z^2\leq x_0/4$")
ax.grid(True, ls=":", alpha=0.6)
fig.tight_layout()
fig.savefig("calculus-15.7.17/solution/part1_figure2.png", dpi=150)
print("saved figure 2")
