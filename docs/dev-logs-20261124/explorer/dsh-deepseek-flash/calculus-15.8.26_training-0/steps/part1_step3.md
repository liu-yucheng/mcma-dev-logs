## Step 1.3: The sphere gives the two heights above one base point

**Reason.** A base point at distance $r$ from the $z$-axis belongs to the solid only at the heights
that the sphere allows. Put $x^{2} + y^{2} = r^{2}$ in $x^{2} + y^{2} + z^{2} \le a^{2}$ and the
bound becomes $z^{2} \le a^{2} - r^{2}$. The two heights are therefore
$z = \pm\sqrt{a^{2} - r^{2}}$. The upper surface $z = +\sqrt{a^{2} - r^{2}}$ falls away from the
$z$-axis, because its slope $-r/\sqrt{a^{2} - r^{2}}$ is negative. The lower surface
$z = -\sqrt{a^{2} - r^{2}}$ rises toward the $z$-axis, because its slope
$+r/\sqrt{a^{2} - r^{2}}$ is positive.

**Computation.** Take $a = 1$. The slope of the upper surface is $-0.314485$ at $r = 0.3$, $-0.75$
at $r = 0.6$, and $-2.064742$ at $r = 0.9$. The slope of the lower surface has the same magnitude
with the opposite sign at each of the three radii. The residual of $z^{2} + r^{2} - a^{2}$ at the
upper surface is $2.22\times10^{-16}$.

**Common mistake.** A reader may take the vertical extent above a base point for the constant $2a$,
but the sphere gives $2\sqrt{a^{2} - r^{2}}$, which falls to $0$ at $r = a$.

**Result.** Over a base point at distance $r$ the solid is the single vertical segment from
$-\sqrt{a^{2} - r^{2}}$ to $+\sqrt{a^{2} - r^{2}}$, of length $2\sqrt{a^{2} - r^{2}}$. The right
panel of Figure 2 draws this segment and names both of its ends.

**Verification.** `code/part1_verify.py` prints `vertical_extent_on_sphere` as
$2.220446049250313\times10^{-16}$ against $0.0$, and `upper_surface_slope_at_r_0` with
`lower_surface_slope_at_r_0` at the radii $0.3$, $0.6$, and $0.9$ with a tolerance of
$1.0\times10^{-6}$.
