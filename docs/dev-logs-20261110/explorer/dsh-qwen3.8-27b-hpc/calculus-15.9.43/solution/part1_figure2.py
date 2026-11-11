"""Problem 15.9.43: labeled 2D cross-section (silhouette) of the silo.

Shows the cylinder (radius 3, height 10) and the hemispherical dome of
radius 3 with dimension labels; supports the 3D figure (Fig. 1).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R, H = 3.0, 10.0

fig, ax = plt.subplots(figsize=(6.4, 7.6))

# Silhouette outline.
t = np.linspace(0, np.pi, 100)
xd = R * np.cos(t)
zd = H + R * np.sin(t)
# Outline: (-R,0) -> (R,0) -> (R,H) -> dome (R -> -R at height H) -> (-R,0).
# xd[0] = R and zd[0] = H already give the corner (R, H).
ox = np.concatenate(([-R, R], xd, [-R]))
oz = np.concatenate(([0.0, 0.0], zd, [0.0]))
ax.plot(ox, oz, color="#2b5f8a", lw=2.0)
ax.fill(ox, oz, color="#cfe2f3", alpha=0.7)

# Dimension arrows.
ax.annotate("", xy=(R + 1.3, H), xytext=(R + 1.3, 0.0),
            arrowprops=dict(arrowstyle="<->", color="#333", lw=1.4))
ax.text(R + 1.5, H / 2, "height 10", rotation=90, va="center", fontsize=11)
ax.annotate("", xy=(0.0, -1.1), xytext=(R, -1.1),
            arrowprops=dict(arrowstyle="<->", color="#333", lw=1.4))
ax.text(R / 2, -1.55, "radius 3", ha="center", fontsize=11)
ax.annotate("", xy=(-R - 1.3, H + R), xytext=(-R - 1.3, H),
            arrowprops=dict(arrowstyle="<->", color="#333", lw=1.4))
ax.text(-R - 1.5, H + R / 2, "dome radius 3", va="center", ha="right",
        fontsize=10)
ax.text(0.0, H + R + 0.35, "top of silo (height 13)", ha="center", fontsize=10)
ax.text(0.0, -2.1, "bottom (z = 0)", ha="center", fontsize=10)
ax.plot([0], [H], "o", ms=4, color="#e6550d")
ax.text(0.25, H - 0.45, "rim at z = 10", fontsize=10, color="#e6550d")

ax.set_xlim(-R - 2.9, R + 2.6)
ax.set_ylim(-2.4, H + R + 1.0)
ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("z")
ax.set_title("Silo cross section: cylinder (radius 3, height 10)\n"
             "surmounted by a hemisphere (radius 3)")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("calculus-15.9.43/solution/part1_figure2.png", dpi=150)
print("saved part1_figure2.png")
