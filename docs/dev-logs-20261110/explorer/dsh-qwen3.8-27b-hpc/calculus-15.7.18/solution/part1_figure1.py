import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6.5))
ax = fig.add_subplot(111, projection="3d")

t = np.linspace(0, np.pi / 2, 40)
xx = np.linspace(0, 1, 40)
T, X = np.meshgrid(t, xx, indexing="ij")
Ys = 3 * np.cos(T)
Zs = 3 * np.sin(T)
Xs = X * np.cos(T)
ax.plot_surface(Xs, Ys, Zs, alpha=0.85, color="#66a3d2", rstride=2, cstride=2)

yy = np.linspace(0, 3, 40)
xxb = np.linspace(0, 1, 40)
YY, XXb = np.meshgrid(yy, xxb, indexing="ij")
ax.plot_surface(XXb * YY / 3, YY, np.zeros_like(YY), alpha=0.9,
                color="#9ad0a0", rstride=3, cstride=3)

yy2 = np.linspace(0, 3, 40)
yy3, zz3 = np.meshgrid(yy2, np.sqrt(np.clip(9 - yy2**2, 0, None)))
ax.plot_surface(np.zeros_like(zz3), yy3, zz3, alpha=0.6,
                color="#d2b46a", rstride=3, cstride=3)

xa = np.linspace(0, 1, 40)
za = np.sqrt(np.clip(9 - 9 * xa**2, 0, None))
XA, ZA = np.meshgrid(xa, za, indexing="ij")
ax.plot_surface(XA, 3 * XA, ZA, alpha=0.55, color="#c98ab8", rstride=3, cstride=3)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title(rf"Exercise 15.7.18: $E$: $y^2+z^2 \leq 9$, $0 \leq x \leq y/3$, $z \geq 0$")
ax.view_init(elev=22, azim=-115)
plt.tight_layout()
plt.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.18/solution/part1_figure1.png",
            dpi=110, bbox_inches="tight")
print("saved fig1")

