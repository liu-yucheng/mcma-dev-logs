import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(9, 6.5))
ax = fig.add_subplot(111, projection="3d")

# Parabolic cylinder y = x^2, 0 <= z <= (4 - y)/2
tt = np.linspace(-2, 2, 40)
S2, T2 = np.meshgrid(np.linspace(0, 1, 25), tt)
X = T2
Y = T2**2
Z = S2 * (4 - Y) / 2
ax.plot_surface(X, Y, Z, color="tab:orange", alpha=0.65)

# Bottom plane z = 0: region x^2 <= y <= 4
S3, T3 = np.meshgrid(np.linspace(0, 1, 25), tt)
Y3 = T3**2 + S3 * (4 - T3**2)
ax.plot_surface(T3, Y3, np.zeros_like(Y3), color="tab:purple", alpha=0.35)

# Top plane y + 2z = 4: 0 <= y <= 4, -sqrt(y) <= x <= sqrt(y)
Yt = np.linspace(0, 4, 30)
S4, T4 = np.meshgrid(np.linspace(-1, 1, 30), Yt)
X4 = S4 * np.sqrt(T4)
Z4 = (4 - T4) / 2
ax.plot_surface(X4, T4, Z4, color="tab:blue", alpha=0.45)

ax.set_title(r"Solid $E$: $x^2\leq y\leq 4$, $0\leq z\leq (4-y)/2$")
ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_zlabel(r"$z$")
ax.set_box_aspect((4, 4, 2))
ax.view_init(elev=18, azim=-60)
fig.tight_layout()
fig.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.31/solution/part1_figure1.png", dpi=150)
print("wrote part1_figure1.png (31)")
