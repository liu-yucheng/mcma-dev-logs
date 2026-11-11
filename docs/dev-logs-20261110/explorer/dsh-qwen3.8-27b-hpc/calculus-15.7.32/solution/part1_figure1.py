"""Part 1, Figure 1 - 3D sketch of the solid E for exercise 15.7.32.

E is the tetrahedron with vertices A(2,0,0), B(0,2,0), C(2,2,0), D(2,2,1).
Faces: z=0 (triangle ABC), x=2 (triangle A C D... check), y=2, and the
slanted plane x+y-2z=2 (triangle ABD).

Face check on x=2: z = (2+y-2)/2 = y/2 -> corners (2,0,0), (2,2,0), (2,2,1).
Face check on y=2: z = x/2 -> corners (0,2,0), (2,2,0), (2,2,1).
Slanted face: triangle A B D (at z=1 only (2,2) satisfies x+y=4).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

A = np.array([2, 0, 0]); B = np.array([0, 2, 0])
C = np.array([2, 2, 0]); D = np.array([2, 2, 1])

fig = plt.figure(figsize=(8.6, 7.0))
ax = fig.add_subplot(111, projection="3d")

faces = [
    ([A, B, C], "orange", 0.55, "z = 0"),
    ([A, C, D], "lightblue", 0.55, "x = 2"),
    ([B, C, D], "lightgreen", 0.55, "y = 2"),
    ([A, B, D], "plum", 0.65, "x + y - 2z = 2"),
]
for tri, color, alpha, _ in faces:
    ax.add_collection3d(Poly3DCollection([tri], color=color, alpha=alpha))

edges = [(A, B), (B, C), (C, A), (A, D), (D, C), (B, D)]
for P, Q in edges:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], [P[2], Q[2]], "k-", lw=1.2)

for P, name in [(A, "A (2,0,0)"), (B, "B (0,2,0)"), (C, "C (2,2,0)"), (D, "D (2,2,1)")]:
    ax.scatter(*P, color="r", s=26, zorder=5)
    ax.text(P[0] + 0.08, P[1] + 0.08, P[2] + 0.04, name, fontsize=9)

ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 2.7); ax.set_ylim(0, 2.7); ax.set_zlim(0, 1.3)
ax.view_init(elev=22, azim=-115)
ax.set_title(rf"Solid $E$: planes $x=2$, $y=2$, $z=0$, $x+y-2z=2$ (a tetrahedron)",
             fontsize=12)
fig.tight_layout()
fig.savefig("calculus-15.7.32/solution/part1_figure1.png", dpi=140)
print("saved part1_figure1.png")
