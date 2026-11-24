## Step 2.2 The integral of the section area gives the same mass

**Reason.** The same mass has a second form as a single integral over $z$. Its integrand is the density times the
area of the section at height $z$, which Step 1.2 derives from the same inequalities. Both forms add the same slices,
so they must agree, and the check tests the derivation of the section rather than the algebra of one integral.

$$M = \int_{0}^{1} 4 \cdot 2(1 - z)^{3/2} \, dz$$

**Computation.** The factor $4 \cdot 2 = 8$ and the substitution $u = 1 - z$ give
$8 \int_{0}^{1} u^{3/2} du = 8 \cdot \frac{2}{5} = \frac{16}{5}$.

**Result.** The section area is {{p2_section_area_latex}}, the length of the section in $y$ is
{{p2_inner_integral_latex}}, and the mass is {{p2_symbolic_mass}}. The integral of the section area prints
{{p2_area_integral_mass}}. Verified by `code/part2_verify.py`, which compares this single integral with the triple
integral of Step 2.1.
