"""Fig 1: 3D solid between the two paraboloids y = x^2+z^2 and y = 8-x^2-z^2."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6.5))
ax = fig.add_subplot(111, projection="3d")
th = np.linspace(0, 2*np.pi, 60)
r = np.linspace(0, 2, 30)
R, TH = np.meshgrid(r, th, indexing="ij")
Xs = R * np.cos(TH)
Zs = R * np.sin(TH)
Y1 = R**2          # lower paraboloid  y = x^2 + z^2
Y2 = 8 - R**2      # upper paraboloid  y = 8 - x^2 - z^2
ax.plot_surface(Xs, Y1, Zs, alpha=0.85, color="#66a3d2", rstride=2, cstride=2)
ax.plot_surface(Xs, Y2, Zs, alpha=0.85, color="#d29a66", rstride=2, cstride=2)
t = np.linspace(0, 2*np.pi, 100)
ax.plot(2*np.cos(t), np.full_like(t, 4.0), 2*np.sin(t), "r-", lw=1.8)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_title(rf"Exercise 15.7.20: $y=x^2+z^2$ (blue), $y=8-x^2-z^2$ (orange), rim $r=2, y=4$ (red)")
ax.view_init(elev=28, azim=-120)
plt.tight_layout()
plt.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.20/solution/part1_figure1.png",
            dpi=110, bbox_inches="tight")
print("saved fig1")
