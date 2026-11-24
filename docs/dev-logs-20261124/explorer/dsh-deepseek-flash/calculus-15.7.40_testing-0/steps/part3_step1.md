## Step 3.1 The moment about the plane x = 0

**Reason.** The first moment about the plane $x = 0$ weighs each point by its distance $x$. The inner integral of
the weight $x$ over the interval $[0, 1 - z]$ gives $\frac{(1 - z)^{2}}{2}$, the length of the section in $y$ is
$2\sqrt{1 - z}$, and one integral over $z$ remains.

$$M_{yz} = \int_{0}^{1} 4 \cdot \frac{(1 - z)^{2}}{2} \cdot 2\sqrt{1 - z} \, dz
        = \int_{0}^{1} 4(1 - z)^{5/2} dz$$

**Computation.** With the substitution $u = 1 - z$ the integral is $4 \int_{0}^{1} u^{5/2} du = 4 \cdot \frac{2}{7}$.

**Result.** The moment is {{p3_m_yz}} = {{p3_m_yz_decimal}}. The sampling of the solid gives the same moment,
{{p3_sampled_x}}. Verified by `code/part3_verify.py`, which compares the closed form with a symbolic integral and
with the sampling.
