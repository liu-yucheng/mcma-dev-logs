"""Problem 15.9.45: plot the bumpy sphere
rho = 1 + (1/5) sin(6 theta) sin(5 phi)  (m = 6, n = 5).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

m, n = 6, 5

theta = np.linspace(0, 2 * np.pi, 160)
phi = np.linspace(0, np.pi, 120)
TH, PH = np.meshgrid(theta, phi)
rho = 1 + 0.2 * np.sin(m * TH) * np.sin(n * PH)

x = rho * np.sin(PH) * np.cos(TH)
y = rho * np.sin(PH) * np.sin(TH)
z = rho * np.cos(PH)

fig = plt.figure(figsize=(7.6, 6.4))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(x, y, z, cmap="viridis", alpha=0.95,
                rstride=2, cstride=2, shade=True, antialiased=False)
ax.plot_wireframe(x, y, z, color="k", alpha=0.08,
                  rstride=8, cstride=8, linewidth=0.3)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Bumpy sphere: rho = 1 + (1/5) sin(6 theta) sin(5 phi), m = 6, n = 5")
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=20, azim=-60)
fig.tight_layout()
fig.savefig("calculus-15.9.45/solution/part1_figure1.png", dpi=150)
print("saved part1_figure1.png")
