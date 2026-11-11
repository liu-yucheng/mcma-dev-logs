"""Sketch the solid E of problem 15.7.17.

E lies between the paraboloid x = 4*y**2 + 4*z**2 (opening toward +x)
and the plane x = 4.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d proj)

y_grid, z_grid = np.meshgrid(np.linspace(-1, 1, 60), np.linspace(-1, 1, 60))
x_paraboloid = 4 * (y_grid**2 + z_grid**2)

# Clip to the solid (x <= 4) so the plot shows only the bounded solid.
x_paraboloid = np.clip(x_paraboloid, None, 4.0)

fig = plt.figure(figsize=(7.2, 5.4))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(y_grid, z_grid, x_paraboloid, cmap="viridis",
                alpha=0.85, rstride=2, cstride=2)

# Plane x = 4 cap (the disk y**2 + z**2 <= 1).
theta_grid = np.linspace(0, 2 * np.pi, 80)
rho_grid, theta_grid2 = np.meshgrid(np.linspace(0, 1, 40), theta_grid)
y_cap = rho_grid * np.cos(theta_grid2)
z_cap = rho_grid * np.sin(theta_grid2)
x_cap = np.full_like(y_cap, 4.0)
ax.plot_surface(x_cap, y_cap, z_cap, color="#4a6fa5", alpha=0.9)

# Axes and labels (axes: x right, y toward viewer, z up).
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("E: paraboloid $x=4y^{2}+4z^{2}$ capped by plane $x=4$")
ax.set_box_aspect((4.4, 2.2, 2.2))
fig.tight_layout()
fig.savefig("calculus-15.7.17/solution/part1_figure1.png", dpi=150)
print("saved figure 1")
