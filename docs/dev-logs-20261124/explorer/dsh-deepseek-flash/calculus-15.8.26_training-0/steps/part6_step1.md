## Step 6.1: Draw the sphere and the cylinder on one screen

**Reason.** Part (b) asks for one figure of both surfaces. Each surface needs its own parameters: the
sphere is $\left(a\sin\varphi\cos\psi,\ a\sin\varphi\sin\psi,\ a\cos\varphi\right)$ with
$\varphi \in [0, \pi]$ and $\psi \in [0, 2\pi]$, and the cylinder is
$\left(a\cos^{2}\theta,\ a\cos\theta\sin\theta,\ t\,a|\sin\theta|\right)$ with
$\theta \in [-\pi/2, \pi/2]$ and $t \in [-1, 1]$. The third coordinate of the cylinder stops at the
heights that step 1.3 gives, so the drawn sheet is the wall of the solid and not a cylinder with flat
caps. The two surfaces meet where both descriptions hold: the curve
$\left(a\cos^{2}\theta,\ a\cos\theta\sin\theta,\ \pm a|\sin\theta|\right)$.

**Computation.** Take $a = 1$. The worst residual of the drawn sphere over its sample points is
$2.22\times10^{-16}$, and the worst residual of the drawn wall against $r = a\cos\theta$ is
$1.11\times10^{-16}$. The drawn wall stays inside the sphere to $5.00\times10^{-16}$. The drawn cut
lies on the sphere to $2.22\times10^{-16}$ and on the cylinder to $1.11\times10^{-16}$, and its
height runs from $0$ to $1.0$. The label of the sphere sits at the distance $0.999953$ from the
origin. The label of the cylinder sits at the radius $0.408487440884$, which is $a\cos(1.15)$, and
at a height below the bound $0.912763940261$.

**Common mistake.** A reader may draw the cylinder as a full tube with flat top and bottom, but the
solid stops at the heights $\pm\sqrt{a^{2} - r^{2}}$: `code/part6_verify.py` prints the excess of
the drawn wall over the sphere bound as $5.00\times10^{-16}$, so a flat cap would lie outside the
sphere.

**Result.** Figure 3 shows the sphere, the wall of the solid, the curve where the two surfaces meet,
and the body $E$ between them. The drawn cylinder wall is the wall of the solid, and its upper and
lower edges are the cut curve.

**Verification.** `code/part6_verify.py` prints `drawn_sphere_on_surface`, `drawn_wall_on_cylinder`,
`drawn_wall_inside_sphere`, `cut_curve_on_sphere`, and `cut_curve_on_cylinder` as the residuals
above, `sphere_label_on_sphere` as $0.9999532139055307$ against $1.0$, and
`cylinder_label_on_cylinder` as $0.40848744088415734$ against $a\cos(1.15)$.

![Figure 3: the sphere $x^{2} + y^{2} + z^{2} = a^{2}$ and the cylinder $r = a\cos\theta$ on one screen, with the curve where they meet](figures/part6_figure1.png)
