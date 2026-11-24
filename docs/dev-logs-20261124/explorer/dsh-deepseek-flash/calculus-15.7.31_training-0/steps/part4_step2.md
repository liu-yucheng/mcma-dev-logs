## Step 4.2. Write the order $dx\,dz\,dy$

**Why.** The outer variable is $y$ again, so the section is the same rectangle. The inner integral is now
in $x$, and the interval of $x$ does not depend on $z$, so the inner integral is again a single integral.

**Derive the limits from the outside inward.** The outer variable is $y$, and $0 \leq y \leq 4$. The
middle variable is $z$, and $0 \leq z \leq (4 - y)/2$. The inner variable is $x$, and the parabola gives
$-\sqrt{y} \leq x \leq \sqrt{y}$. The order is

$$
\iiint_{E} f\,dV = \int_{0}^{4}\int_{0}^{(4-y)/2}\int_{-\sqrt{y}}^{\sqrt{y}} f(x,y,z)\,dx\,dz\,dy.
$$

**Compare the two orders of this part.** Both orders integrate over the same rectangle. The order
$dz\,dx\,dy$ cuts the rectangle into vertical pieces and the order $dx\,dz\,dy$ cuts it into horizontal
pieces. Because the rectangle is a product of two intervals, each order factors into a product of two
integrals when the integrand is a product of a function of one variable and a function of another
variable.

**Result.** The fourth order is
$\int_{0}^{4}\int_{0}^{(4-y)/2}\int_{-\sqrt{y}}^{\sqrt{y}} f\,dx\,dz\,dy$. Its value for $f = 1$ is
$8.5333333333$, which is the value of the order of Step 4.1.

**Check.** `code/part4_verify.py` prints the value of both orders for the three integrands and the
absolute difference of each pair. Each difference is below $10^{-12}$. The corner list of the section
at $y = 2$ is in the printout of `code/part2_verify.py` that Step 2.2 cites: the interval of $x$ is
$[-1.414214, 1.414214]$ and the interval of $z$ is $[0, 1]$, and the four corners give a rectangle.
