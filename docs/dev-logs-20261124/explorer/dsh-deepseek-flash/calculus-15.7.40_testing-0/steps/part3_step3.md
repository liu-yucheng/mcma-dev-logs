## Step 3.3 The center of mass

**Reason.** The center of mass divides each moment by the mass, and not by the volume. The moment about the plane
$y = 0$ is $0$, so the second coordinate of the center is $0$.

$$\bar{x} = \frac{M_{yz}}{M}, \qquad \bar{y} = \frac{M_{xz}}{M}, \qquad \bar{z} = \frac{M_{xy}}{M}$$

**Computation.** With $M = \frac{16}{5}$ the two nonzero coordinates are

$$\bar{x} = \frac{8}{7} \cdot \frac{5}{16} = \frac{5}{14}, \qquad
  \bar{z} = \frac{32}{35} \cdot \frac{5}{16} = \frac{2}{7}$$

**Result.** The center of mass is {{p3_xbar}} in $x$, $0$ in $y$, and {{p3_zbar}} in $z$, that is
$({{p3_xbar_decimal}},\ 0,\ {{p3_zbar_decimal}})$. The sampling gives {{p3_sampled_center}}. A reader may divide the
moment by the volume instead of by the mass, but the definition divides by the mass, and that wrong ratio prints
{{p3_naive_ratio}}, which lies outside the range $0 \le x \le 1$ of the solid. Verified by `code/part3_verify.py`,
which asserts that each coordinate lies in the range of its axis.
