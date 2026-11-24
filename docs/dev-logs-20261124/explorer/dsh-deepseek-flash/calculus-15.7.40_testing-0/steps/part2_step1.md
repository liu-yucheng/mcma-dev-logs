## Step 2.1 Build the mass integral and evaluate it four ways

**Reason.** The mass is the integral of the density over the solid. The density is the constant $4$, so the mass is
$4$ times the volume, and the order of integration is free. The order $dx\,dz\,dy$ integrates $x$ first, which
leaves the factor $1 - z$; the next integral over $z$ has the variable upper bound $1 - y^{2}$.

$$M = \int_{-1}^{1} \int_{0}^{1 - y^{2}} \int_{0}^{1 - z} 4 \, dx \, dz \, dy$$

**Computation.** The inner integral over $x$ gives $4(1 - z)$. The next integral over $z$ gives
$2 - 2y^{4}$, which the print of `code/part2_verify.py` states as the equal form $4u - 2u^{2}$ with
$u = 1 - y^{2}$, and the last integral over $y$ gives the mass. Four independent routes agree: the
symbolic order $dy\,dx\,dz$, the symbolic order $dx\,dz\,dy$, the substitution $u = 1 - y^{2}$, and the single
integral of the section area $4 \cdot 2(1 - z)^{3/2}$ over $0 \le z \le 1$.

**Result.** The mass is {{p2_mass_exact}} = {{p2_mass_decimal}}. The volume is {{p2_volume_exact}} =
{{p2_volume_decimal}}, and the density times the volume equals the mass. The single integral of the section area
prints {{p2_area_integral_mass}} and the integral of the $y$ sections prints {{p2_y_section_mass}}. A sampling of
{{p2_sampling_points}} points gives {{p2_sampling_mass}} with a standard error of {{p2_sampling_error}}, which is
within four standard errors of the mass. Verified by `code/part2_verify.py`.
