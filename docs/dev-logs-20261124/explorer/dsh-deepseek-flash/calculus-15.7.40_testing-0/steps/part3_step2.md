## Step 3.2 The moments about the planes y = 0 and z = 0

**Reason.** The moment about the plane $y = 0$ weighs each point by $y$. The solid and the density are unchanged by
the reflection $y \to -y$, and the weight is odd under that reflection, so the integral is $0$. The moment about the
plane $z = 0$ weighs each point by $z$; the inner integral over $x$ gives $1 - z$ and the length in $y$ is
$2\sqrt{1 - z}$.

$$M_{xz} = 0, \qquad M_{xy} = \int_{0}^{1} 4 z \cdot 2(1 - z)^{3/2} dz$$

**Computation.** The substitution $u = 1 - z$ turns the integral into $8 \int_{0}^{1} (1 - u) u^{3/2} du$. With
$\int_{0}^{1} u^{3/2} du = \frac{2}{5}$ and $\int_{0}^{1} u^{5/2} du = \frac{2}{7}$ the value is
$8\left(\frac{2}{5} - \frac{2}{7}\right)$.

**Result.** The moment about the plane $y = 0$ is {{p3_m_xz}} and the moment about the plane $z = 0$ is
{{p3_m_xy}} = {{p3_m_xy_decimal}}. The sampling gives {{p3_sampled_y}} and {{p3_sampled_z}}, and the membership test
of each mirrored pair of sampled points gives the same answer. Verified by `code/part3_verify.py`.
