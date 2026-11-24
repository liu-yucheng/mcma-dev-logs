## Step 2.3: The inner integral gives $2r\sqrt{a^{2} - r^{2}}$

**Reason.** The integrand $r$ does not contain $z$, so the inner integral is the integrand multiplied
by the length of the segment of $z$. Step 1.3 gives the length $2\sqrt{a^{2} - r^{2}}$, so the inner
integral is $r \cdot 2\sqrt{a^{2} - r^{2}}$.

**Computation.** Take $a = 1$ and $r = 0.5$. Bisection gives the length of the segment as
$1.732050807569$, so the inner integral is $0.5 \times 1.732050807569 = 0.866025403785$.

**Common mistake.** A reader may integrate $z$ from $0$ to $\sqrt{a^{2} - r^{2}}$, but the limits are
$-\sqrt{a^{2} - r^{2}}$ and $+\sqrt{a^{2} - r^{2}}$, so the length is $2\sqrt{a^{2} - r^{2}}$ and the
factor $2$ belongs to the value.

**Result.** After the inner integration,
$$V = \int_{-\pi/2}^{\pi/2}\int_{0}^{a\cos\theta} 2r\sqrt{a^{2} - r^{2}}\,dr\,d\theta.$$

**Verification.** `code/part2_verify.py` prints `vertical_length_by_bisection` with an error of
$1.44\times10^{-15}$ against the closed length, and `single_vertical_segment` as $1.0$ for the count
of segments along a ray.
