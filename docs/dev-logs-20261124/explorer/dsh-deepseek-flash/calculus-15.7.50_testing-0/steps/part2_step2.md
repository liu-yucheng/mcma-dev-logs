## Step 2.2 — Integrate the outer variable and read the mass

**Reason.** After Step 2.1 the mass is one integral in $y$, and that integral has a Beta form because the factor $\sqrt{9 - y^{2}}$ is the square root of a difference of squares. A reader may take the mass for the area of the projection times the mean density, but the projection has the area ${{projection_area}}$ and the density grows with $y$, so the limits $0 \le x \le y/3$ and $0 \le z \le \sqrt{9 - y^{2}}$ give the single integral $\int_{0}^{3} \frac{28 y^{3}}{81}\sqrt{9 - y^{2}}\, dy$.

**Computation.** Substitute $y = 3t$, so $dy = 3\,dt$ and $\sqrt{9 - y^{2}} = 3\sqrt{1 - t^{2}}$. The integral becomes

$$ M = \frac{28}{81}\int_{0}^{3} y^{3}\sqrt{9 - y^{2}}\, dy = \frac{28}{81}\, 3^{5}\int_{0}^{1} t^{3}\sqrt{1 - t^{2}}\, dt . $$

The remaining integral is $\frac{1}{2}B(2, \frac{3}{2}) = \frac{2}{15}$, so

$$ M = \frac{28}{81}\cdot 243 \cdot \frac{2}{15} = \frac{56}{5} = {{mass}} . $$

**Verification.** `code/part2_verify.py` computes the mass by the Beta function, by nested quadrature in the order $dx\,dz\,dy$, by quadrature in the order $dz\,dy\,dx$, and by a uniform sample of the box. The four routes print ${{mass_beta}}$, ${{mass_quadrature}}$, ${{mass_alternate}}$, and ${{mass_monte_carlo}}$ with the error ${{mass_monte_carlo_error}}$, which is ${{mass_sigma_deviation}}$ standard errors from the quadrature.

**Check of the limits against a wrong reading.** `code/part2_verify.py` prints two wrong masses that a wrong limit set produces. If $x$ runs to $1$ instead of $y/3$, the print "mass with $x \le 1$ instead of $x \le y / 3$" gives ${{mass_without_plane}}$, and that value exceeds the true mass. If the density is replaced by a constant over the projection, the print "mass of the double integral over the projection" gives ${{mass_without_z}}$. A reader may take either value for the mass, but the limits $0 \le x \le y/3$ and $0 \le z \le \sqrt{9 - y^{2}}$ give ${{mass}}$.

**Result.** The mass of the solid is $M = {{mass}}$, which is ${{mass_exact}}$ exactly, and the mean density is $M / V = {{mean_density}}$.
