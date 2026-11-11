"""Problem 15.8.26 (b): graph the sphere of radius a = 1 and the cylinder
r = a*cos(theta) on the same screen, and mark their intersection.

With a = 1 the cylinder r = cos(theta) is x^2 + y^2 = x, the circle of
radius 1/2 centred at (1/2, 0):  x = 1/2 + (1/2)cos(t), y = (1/2)sin(t).
The Viviani intersection curve is r = cos(theta), z = +/- sin(theta).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

a = 1.0
fig = plt.figure(figsize=(8.6, 6.2))
ax = fig.add_subplot(111, projection="3d")

# --- full sphere (translucent) ---
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 60)
xs = a * np.outer(np.cos(u), np.sin(v))
ys = a * np.outer(np.sin(u), np.sin(v))
zs = a * np.outer(np.ones_like(u), np.cos(v))
ax.plot_surface(xs, ys, zs, color="#9ecae1", alpha=0.25,
                rstride=3, cstride=3, shade=True)

# --- cylinder x^2 + y^2 = x, clipped to the sphere ---
t = np.linspace(0, 2 * np.pi, 160)
zc = np.linspace(-1.0, 1.0, 60)
TC, ZC = np.meshgrid(t, zc)
xc = 0.5 + 0.5 * np.cos(TC)
yc = 0.5 * np.sin(TC)
zlim = np.sqrt(np.clip(1.0 - (xc**2 + yc**2), 0.0, None))
mask = np.abs(ZC) <= zlim
xm = np.where(mask, xc, np.nan)
ym = np.where(mask, yc, np.nan)
ax.plot_surface(xm, ym, ZC, color="#4a90c4", alpha=0.55,
                rstride=2, cstride=2, shade=True)

# --- Viviani intersection curve ---
tt = np.linspace(-np.pi / 2, np.pi / 2, 300)
xi = np.cos(tt) ** 2
yi = np.cos(tt) * np.sin(tt)
zi = np.sin(tt)
ax.plot(xi, yi, zi, color="#e6550d", lw=2.2)
ax.plot(xi, yi, -zi, color="#e6550d", lw=2.2)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Part (b): sphere x^2+y^2+z^2 = 1 and cylinder x^2+y^2 = x; "
             "orange = their intersection")
ax.set_box_aspect((1, 1, 0.8))
ax.view_init(elev=18, azim=-55)
fig.tight_layout()
fig.savefig("calculus-15.8.26/solution/part2_figure1.png", dpi=150)
print("saved part2_figure1.png")
