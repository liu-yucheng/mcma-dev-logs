"""Problem 15.9.43: matplotlib 3D drawing of a silo.

Silo = cylinder radius 3, height 10 (from z = 0 to z = 10), topped by a
hemisphere of radius 3 centred at (0, 0, 10).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R, H = 3.0, 10.0

fig = plt.figure(figsize=(7.0, 8.0))
ax = fig.add_subplot(111, projection="3d")

# Cylinder wall: 0 <= z <= 10.
t = np.linspace(0, 2 * np.pi, 120)
z = np.linspace(0.0, H, 1)
TT, ZZ = np.meshgrid(t, z)
xc = R * np.cos(TT)
yc = R * np.sin(TT)
ax.plot_surface(xc, yc, ZZ, color="#8fb8de", alpha=0.9,
                rstride=3, cstride=3, shade=True)

# Bottom disk z = 0.
rd = np.linspace(0.0, R, 30)
TD, RD = np.meshgrid(t, rd)
xb = RD * np.cos(TD)
yb = RD * np.sin(TD)
zb = np.zeros_like(xb)
ax.plot_surface(xb, yb, zb, color="#6d9dc5", alpha=0.95)

# Hemisphere dome: x = R sin(phi) cos(theta), y = R sin(phi) sin(theta),
# z = H + R cos(phi),  0 <= phi <= pi/2.
phi = np.linspace(0.0, np.pi / 2, 40)
TP, RP = np.meshgrid(t, phi)
xd = R * np.sin(RP) * np.cos(TP)
yd = R * np.sin(RP) * np.sin(TP)
zd = H + R * np.cos(RP)
ax.plot_surface(xd, yd, zd, color="#b7d3ea", alpha=0.95,
                rstride=2, cstride=2, shade=True)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Silo: cylinder (radius 3, height 10) surmounted by a hemisphere (radius 3)")
ax.set_box_aspect((1, 1, 2.2))
ax.set_xlim(-3.6, 3.6)
ax.set_ylim(-3.6, 3.6)
ax.set_zlim(-0.6, 13.6)
ax.view_init(elev=16, azim=-60)
fig.tight_layout()
fig.savefig("calculus-15.9.43/solution/part1_figure1.png", dpi=150)
print("saved part1_figure1.png")
