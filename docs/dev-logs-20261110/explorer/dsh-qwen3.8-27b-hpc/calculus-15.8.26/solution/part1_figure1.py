"""Problem 15.8.26 (a): 3D picture of the solid cut out of the sphere of
radius a = 1 by the cylinder r = cos(theta) (the Viviani solid).

Solid:  -pi/2 <= theta <= pi/2,  0 <= r <= cos(theta),
        -sqrt(1 - r^2) <= z <= sqrt(1 - r^2).

Boundary surfaces:
  * spherical caps:  part of the sphere x^2+y^2+z^2 = 1 inside the cylinder,
                     parameterised by (theta, r), z = +/-(sqrt(1 - r^2)).
  * cylindrical side: part of the cylinder x^2+y^2 = x inside the sphere,
                     parameterised by (theta, z), r = cos(theta).
The Viviani curve r = cos(theta), z = +/- sin(theta) joins them.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

a = 1.0
fig = plt.figure(figsize=(8.4, 6.2))
ax = fig.add_subplot(111, projection="3d")

# --- spherical caps (top and bottom) ---
th = np.linspace(-np.pi / 2, np.pi / 2, 90)
rr = np.linspace(0.0, 1.0, 60)
TH, RR = np.meshgrid(th, rr)                 # shape (60, 90)
r = RR * np.cos(TH)                          # 0 <= r <= cos(theta)
xs = r * np.cos(TH)
ys = r * np.sin(TH)
zcap = np.sqrt(np.clip(1.0 - r**2, 0.0, None))
ax.plot_surface(xs, ys, zcap, color="#f4a582", alpha=0.72,
                rstride=2, cstride=2, shade=True)
ax.plot_surface(xs, ys, -zcap, color="#f4a582", alpha=0.72,
                rstride=2, cstride=2, shade=True)

# --- cylindrical side (r = cos(theta), |z| <= sin(theta)) ---
th2 = np.linspace(-np.pi / 2, np.pi / 2, 90)
zz = np.linspace(-1.0, 1.0, 60)
TH2, ZZ2 = np.meshgrid(th2, zz)              # shape (60, 90)
zlim = np.abs(np.sin(TH2))
x2 = np.cos(TH2) ** 2
y2 = np.cos(TH2) * np.sin(TH2)
xm = np.where(np.abs(ZZ2) <= zlim, x2, np.nan)
ym = np.where(np.abs(ZZ2) <= zlim, y2, np.nan)
ax.plot_surface(xm, ym, ZZ2, color="#fdd0a2", alpha=0.85,
                rstride=2, cstride=2, shade=True)

# --- Viviani boundary curve ---
t = np.linspace(-np.pi / 2, np.pi / 2, 300)
xv = np.cos(t) ** 2
yv = np.cos(t) * np.sin(t)
zv = np.sin(t)
ax.plot(xv, yv, zv, color="#a50f15", lw=2.0)
ax.plot(xv, yv, -zv, color="#a50f15", lw=2.0)

# --- faint full sphere for orientation ---
u = np.linspace(0, 2 * np.pi, 80)
v = np.linspace(0, np.pi, 40)
ax.plot_surface(a * np.outer(np.cos(u), np.sin(v)),
                a * np.outer(np.sin(u), np.sin(v)),
                a * np.outer(np.ones_like(u), np.cos(v)),
                color="gray", alpha=0.08, rstride=4, cstride=4)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Part (a) solid: 0 <= r <= cos(theta), inside the unit sphere (a = 1)")
ax.set_box_aspect((1, 1, 0.8))
ax.view_init(elev=22, azim=60)
fig.tight_layout()
fig.savefig("calculus-15.8.26/solution/part1_figure1.png", dpi=150)
print("saved part1_figure1.png")
