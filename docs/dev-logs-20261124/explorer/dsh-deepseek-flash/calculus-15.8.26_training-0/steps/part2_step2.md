## Step 2.2: The volume element carries the factor $r$

**Reason.** A volume integral in cylindrical coordinates adds the small cells of the grid. A cell
between the radii $r$ and $r + dr$ and between the angles $\theta$ and $\theta + d\theta$ has the
area $r\,dr\,d\theta$, because the arc length at distance $r$ is $r\,d\theta$ and the radial width is
$dr$. The height of the cell is $dz$. The volume element is therefore $dV = r\,dz\,dr\,d\theta$, and
the factor $r$ is part of the geometry and not of the integrand.

**Computation.** Take $a = 1$. The polar cell of the figure has the computed area $0.2371875$, and a
grid count of the same cell gives $0.23718736$. The volume computed without the factor $r$ is
$3.467401100272$, and the volume computed with the factor $r$ is $1.205506213504$.

**Common mistake.** A reader may drop the factor $r$ from the volume element, but the cell area is
$r\,dr\,d\theta$: `code/part2_verify.py` prints $3.467401100272$ for that integral against
$1.205506213504$ for the integral with the factor $r$.

**Result.** The volume is $V = \int_{-\pi/2}^{\pi/2}\int_{0}^{a\cos\theta}\int_{-\sqrt{a^{2}-r^{2}}}^{\sqrt{a^{2}-r^{2}}} r\,dz\,dr\,d\theta$.

**Verification.** `code/part2_verify.py` prints `jacobian_cell_area` as $0.2371875$ against the grid
value $0.23718736$ with a tolerance of $1.0\times10^{-4}$, and it prints the two volumes above as
the control of the factor $r$.
