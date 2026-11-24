## Step 2.3 Two wrong masses that the limits reject

**Reason.** A reader may take the solid as a prism of thickness $1$ over the triangle of the projection on the plane
$y = 0$, but the limits give the depth $1 - z$ and the height $1 - y^{2}$, so the solid narrows in both $z$ and $y$.
A reader may also take the half width in $y$ as $1 - z$, but the limits give the half width $\sqrt{1 - z}$, which is
larger everywhere except at the two ends of the interval of $z$.

**Computation.** The prism value is the density times the area of the triangle, that is $4 \cdot \frac{1}{2} = 2$.
The narrow value replaces $2\sqrt{1 - z}$ by $2(1 - z)$ in the section area.

**Result.** The prism mass is {{p2_naive_prism_mass}} and the narrow mass is {{p2_naive_narrow_mass}}. Both are
smaller than the mass {{p2_mass_exact}}, and `code/part2_verify.py` prints both values and asserts that each one
differs from the mass by more than one percent. Verified by `code/part2_verify.py`.
