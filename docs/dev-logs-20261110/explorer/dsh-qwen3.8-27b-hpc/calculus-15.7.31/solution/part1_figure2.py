import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.4))

# Left: cross section in the xy plane (z = 0): x^2 <= y <= 4
import numpy as np
xv = np.linspace(-2, 2, 80)
a1.fill(np.concatenate([xv, xv[::-1]]), np.concatenate([xv**2, 4*np.ones_like(xv)]),
        color="tab:blue", alpha=0.25)
a1.plot(xv, xv**2, "k-", lw=1.5, label=r"$y=x^2$")
a1.plot([-2, 2], [4, 4], "k-", lw=1.5, label=r"$y=4$")
a1.text(0.3, 2.5, r"$(x,y)$", fontsize=12)
a1.annotate(r"$(\pm 2,\,4)$", (1.15, 4.12), fontsize=11)
a1.set_title(r"Cross section in the $xy$-plane: $x^2\leq y\leq 4$")
a1.set_xlabel(r"$x$"); a1.set_ylabel(r"$y$")
a1.set_xlim(-2.4, 2.4); a1.set_ylim(-0.2, 4.6); a1.set_aspect("auto")
a1.legend(loc="lower right", fontsize=10); a1.grid(alpha=0.3)

# Right: cross section at a fixed x = x0 (yz plane):
# x0^2 <= y <= 4,  0 <= z <= (4 - y)/2  -> triangle (x0^2,0), (x0^2,(4-x0^2)/2), (4,0)
x0 = 1.0
ya = x0**2
za = (4 - x0**2) / 2
a2.fill([ya, ya, 4, ya], [0, za, 0, 0], color="tab:green", alpha=0.25)
a2.plot([ya, ya, 4, ya, ya], [0, za, 0, 0, za], "k-", lw=1.5)
a2.plot([ya, ya, 4], [0, za, 0], "o", ms=4)
a2.annotate(r"$(y,z)=(x_0^2,\,0)$", (ya - 0.15, -0.24), fontsize=10)
a2.annotate(r"$(x_0^2,\,(4-x_0^2)/2)$", (ya + 0.15, za + 0.04), fontsize=10)
a2.annotate(r"$(4,0)$", (3.4, 0.1), fontsize=10)
a2.text(1.8, 0.45, r"$(y,z)$", fontsize=12)
a2.set_title(r"Cross section at fixed $x=x_0in(-2,2)$: $x_0^2leq yleq 4$, $0leq zleq (4-y)/2$")
a2.set_xlabel(r"$y$"); a2.set_ylabel(r"$z$")
a2.set_xlim(-0.4, 4.6); a2.set_ylim(-0.3, 2.35); a2.set_aspect("auto")
a2.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.31/solution/part1_figure2.png", dpi=150)
print("wrote part1_figure2.png (31)")
