"""Fig 1: 3D solid for 15.7.22: cylinder x^2+z^2=4 (axis = y), caps y=-1 and y+z=4."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6.5))
ax = fig.add_subplot(111, projection="3d")
th = np.linspace(0, 2*np.pi, 60)
ys = np.linspace(-1, 5, 50)
TH, YS = np.meshgrid(th, ys, indexing="ij")
Xs = 2 * np.cos(TH)
Zs = 2 * np.sin(TH)
# keep only the part with -1 <= y <= 4 - z  (NaN elsewhere)
keep = (YS >= -1) & (YS <= 4 - Zs)
Xf = np.where(keep, Xs, np.nan)
Yf = np.where(keep, YS, np.nan)
Zf = np.where(keep, Zs, np.nan)
ax.plot_surface(Xf, Yf, Zf, alpha=0.85, color="#66a3d2", rstride=2, cstride=2)
# back cap y = -1: disk x^2+z^2<=4
r = np.linspace(0, 2, 30)
R, TH2 = np.meshgrid(r, th, indexing="ij")
ax.plot_surface(2*np.cos(TH2), np.full_like(TH2, -1.0), 2*np.sin(TH2),
                alpha=0.85, color="#9ad0a0", rstride=2, cstride=2)
# slant cap y = 4 - z
ax.plot_surface(2*np.cos(TH2), 4 - 2*np.sin(TH2), 2*np.sin(TH2),
                alpha=0.6, color="#c98ab8", rstride=2, cstride=2)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_title(rf"Exercise 15.7.22: cylinder $x^2+z^2=4$ (blue), caps $y=-1$ (green) and $y+z=4$ (purple)")
ax.view_init(elev=18, azim=-60)
plt.tight_layout()
plt.savefig("D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261110/dsh-qwen3.8-27b-hpc/calculus-15.7.22/solution/part1_figure1.png",
            dpi=110, bbox_inches="tight")
print("saved fig1")
