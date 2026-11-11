import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure(figsize=(9, 6.5))
ax = fig.add_subplot(111, projection="3d")

y = np.linspace(0, 2, 24)
s = np.linspace(0, 1, 24)

def quads(Xg, Yg, Zg):
    P = []
    for i in range(Xg.shape[0] - 1):
        for j in range(Xg.shape[1] - 1):
            P.append([(Xg[i, j], Yg[i, j], Zg[i, j]), (Xg[i + 1, j], Yg[i + 1, j], Zg[i + 1, j]),
                      (Xg[i + 1, j + 1], Yg[i + 1, j + 1], Zg[i + 1, j + 1]),
                      (Xg[i, j + 1], Yg[i, j + 1], Zg[i, j + 1])])
    return P

# base region grid in the xy-plane: x = s*(4 - y^2),  0 <= y <= 2
Yq, Sq = np.meshgrid(y, s)
Xq = Sq * (4 - Yq**2)

# Face: bottom z = 0
ax.add_collection3d(Poly3DCollection(quads(Xq, Yq, np.zeros_like(Xq)),
                                     facecolors="tab:purple", alpha=0.30, edgecolors="none"))
# Face: top plane z = 2 - y
ax.add_collection3d(Poly3DCollection(quads(Xq, Yq, 2 - Yq),
                                     facecolors="tab:green", alpha=0.60, edgecolors="none"))
# Face: parabolic surface x = 4 - y^2,  0 <= z <= 2 - y
Yp2, Sp2 = np.meshgrid(y, s)
Zp2 = Sp2 * (2 - Yp2)
Xp2 = 4 - Yp2**2
ax.add_collection3d(Poly3DCollection(quads(Xp2, Yp2, Zp2),
                                     facecolors="tab:orange", alpha=0.60, edgecolors="none"))
# Face: plane x = 0 (triangle 0<=y<=2, 0<=z<=2-y)
Yp3, Sp3 = np.meshgrid(y, s)
Zp3 = Sp3 * (2 - Yp3)
ax.add_collection3d(Poly3DCollection(quads(np.zeros_like(Yp3), Yp3, Zp3),
                                     facecolors="tab:red", alpha=0.55, edgecolors="none"))
# Face: plane y = 0 (rectangle 0<=x<=4, 0<=z<=2)
Xr, Sr = np.meshgrid(np.linspace(0, 4, 24), s)
Zr = Sr * 2
ax.add_collection3d(Poly3DCollection(quads(Xr, np.zeros_like(Xr), Zr),
                                     facecolors="tab:blue", alpha=0.35, edgecolors="none"))

ax.set_title(r"Solid $E$: $0\leq y\leq 2$, $0\leq z\leq 2-y$, $0\leq x\leq 4-y^2$  (volume $20/3$)")
ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_zlabel(r"$z$")
ax.set_box_aspect((4, 2, 2))
ax.set_xlim(0, 4.2); ax.set_ylim(0, 2.2); ax.set_zlim(0, 2.2)
ax.view_init(elev=16, azim=-55)
fig.tight_layout()
fig.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.28/solution/part1_figure1.png", dpi=150)
print("wrote part1_figure1.png (28)")
