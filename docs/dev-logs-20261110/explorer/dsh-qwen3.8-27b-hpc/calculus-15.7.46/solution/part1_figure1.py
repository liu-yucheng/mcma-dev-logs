"""Part 1, Figure 1 - 3D sketch of the solid cone for exercise 15.7.46.

Cone: sqrt(x^2 + y^2) <= z <= h. Vertex at the origin, circular base of
radius h in the plane z = h.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

h = 2.0
fig = plt.figure(figsize=(8.2, 7.0))
ax = fig.add_subplot(111, projection="3d")

th = np.linspace(0, 2*np.pi, 90)
zgrid = np.linspace(0, h, 40)
TH, Z = np.meshgrid(th, zgrid)
R = Z                      # r = z on the cone surface
X = R * np.cos(TH); Y = R * np.sin(TH)
ax.plot_surface(X, Y, Z, color="lightblue", alpha=0.8, edgecolor="none")

# base disk at z = h, radius h
Rb, Tb = np.meshgrid(np.linspace(0, h, 40), np.linspace(0, 2*np.pi, 90))
Xb = Rb * np.cos(Tb); Yb = Rb * np.sin(Tb)
ax.plot_surface(Xb, Yb, np.full_like(Rb, h), color="orange", alpha=0.85)

# base circle edge
ax.plot(h*np.cos(th), h*np.sin(th), np.full_like(th, h), "k-", lw=1.6)
# generator lines from vertex
for ang in np.linspace(0, 2*np.pi, 8, endpoint=False):
    ax.plot([0, h*np.cos(ang)], [0, h*np.sin(ang)], [0, h], "k--", lw=0.6, alpha=0.5)

# z-axis
ax.plot([0, 0], [0, 0], [0, h], "g-", lw=1.4)
ax.text(0.1, 0.1, 0.15, "vertex $(0,0,0)$", fontsize=9)
ax.text(0.1, 0.1, h + 0.05, rf"base: $z = h$, radius $h$", fontsize=9)

ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6); ax.set_zlim(0, 2.6)
ax.view_init(elev=18, azim=-65)
ax.set_title(rf"Solid cone $sqrt{{x^2+y^2}} le z le h$"
             rf"  (density $k$)", fontsize=12)
fig.tight_layout()
fig.savefig("calculus-15.7.46/solution/part1_figure1.png", dpi=140)
print("saved part1_figure1.png")
