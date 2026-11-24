## Step 5.2. Write the order $dx\,dy\,dz$

**Why.** The outer variable is $z$ again, so the section is the same parabolic segment. The inner
integral is now in $x$. The segment is symmetric about the plane $x = 0$, so the limits of $x$ are
$-\sqrt{y}$ and $\sqrt{y}$ for every fixed $y$.

**Derive the limits from the outside inward.** The outer variable is $z$, and $0 \leq z \leq 2$. The
middle variable is $y$. In the segment at a fixed $z$ the value of $y$ runs from 0 to $4 - 2z$. The inner
variable is $x$, and $x^{2} \leq y$ gives $-\sqrt{y} \leq x \leq \sqrt{y}$. The order is

$$
\iiint_{E} f\,dV = \int_{0}^{2}\int_{0}^{4-2z}\int_{-\sqrt{y}}^{\sqrt{y}} f(x,y,z)\,dx\,dy\,dz.
$$

**Compare the two orders of this part.** Both orders integrate over the same segment. Each order has one
inner integral and one middle integral, and neither order splits an inner integral into two integrals. The
order $dy\,dx\,dz$ cuts the segment into vertical pieces and the order $dx\,dy\,dz$ cuts it into
horizontal pieces. The horizontal pieces have length $2\sqrt{y}$, and that length grows with $y$, so the
widest piece is at $y = 4 - 2z$.

**Result.** The sixth order is
$\int_{0}^{2}\int_{0}^{4-2z}\int_{-\sqrt{y}}^{\sqrt{y}} f\,dx\,dy\,dz$. Its value for $f = 1$ is
$8.5333333333$, which is the value of the order of Step 5.1.

**Check.** `code/part5_verify.py` prints the value of both orders for the three integrands and the
absolute difference of each pair. Each difference is below $10^{-12}$. The script
`code/part5_figure4.py` prints the interval of $x$ at $y = 0.5$, $y = 1.5$, and $y = 2.5$ when it draws
panel (b) of Figure 4, and these intervals are $[-0.707107, 0.707107]$, $[-1.224745, 1.224745]$, and
$[-1.581139, 1.581139]$.
