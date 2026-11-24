## Step 2.1 — Integrate the two inner variables of the mass

**Reason.** The mass is the integral of the density $\rho = x^{2} + y^{2}$ over the solid. The inner integral runs along a line of constant $y$ and $z$, and the density is a quadratic in $x$ on that line, so the inner integral is a polynomial in $y$ and $z$ that we can write explicitly. A reader may take the inner integral for $x^{2} + y^{2}$ times the length $y/3$, but the limits $0 \le x \le y/3$ give $\int_{0}^{y/3} (x^{2} + y^{2}) \, dx = \frac{y^{3}}{81} + \frac{y^{3}}{3}$.

**Computation.** The inner integral is

$$ \int_{0}^{y/3} \left(x^{2} + y^{2}\right) dx = \frac{1}{3}\left(\frac{y}{3}\right)^{3} + y^{2}\frac{y}{3} = \frac{28 y^{3}}{81}. $$

The middle integral multiplies this value by the length of the $z$ interval, $\sqrt{9 - y^{2}}$, because $28y^{3}/81$ does not depend on $z$:

$$ \int_{0}^{\sqrt{9-y^{2}}} \frac{28 y^{3}}{81} \, dz = \frac{28 y^{3}}{81}\sqrt{9 - y^{2}}. $$

**Verification.** `code/part2_verify.py` compares the formula $28y^{3}/81$ with a direct antiderivative at three values of $y$ and with a Gauss rule on the $x$ interval. The printed rows are

{{table:inner_x}}

Each row prints the formula, the direct antiderivative, the Gauss rule, and the largest difference between them.

**Result.** The middle row of the table gives the inner integral ${{inner_x_at_1_5|6}}$, and the middle integral at the same $y$ is ${{middle_integral_at_1_5|6}}$, which is the inner value times the height $\sqrt{9 - y^{2}}$.
