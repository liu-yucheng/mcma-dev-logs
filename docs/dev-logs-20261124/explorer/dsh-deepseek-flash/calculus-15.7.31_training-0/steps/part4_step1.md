# Part 4. The two orders with $y$ outermost

The outer variable is $y$, so the section is the one at a fixed $y$. Step 2.2 gives its shape: a
rectangle. Neither limit of the rectangle depends on the other coordinate, so both orders of this part
have a product structure and neither inner integral needs a split.

## Step 4.1. Write the order $dz\,dx\,dy$

**Why.** The inner integral is in $z$ and the middle integral is in $x$. In the rectangle at a fixed $y$
the value of $z$ runs from the floor to the slanted plane, and that range does not depend on $x$. The
inner integral is therefore a single integral.

**Derive the limits from the outside inward.** The outer variable is $y$, and Step 1.2 gives
$0 \leq y \leq 4$. The middle variable is $x$. The parabola gives $x^{2} \leq y$, so
$-\sqrt{y} \leq x \leq \sqrt{y}$. The inner variable is $z$, and $0 \leq z \leq (4 - y)/2$. The order is

$$
\iiint_{E} f\,dV = \int_{0}^{4}\int_{-\sqrt{y}}^{\sqrt{y}}\int_{0}^{(4-y)/2} f(x,y,z)\,dz\,dx\,dy.
$$

**Result.** The third order is
$\int_{0}^{4}\int_{-\sqrt{y}}^{\sqrt{y}}\int_{0}^{(4-y)/2} f\,dz\,dx\,dy$. Its value for $f = 1$ is
$8.5333333333$.

**Check.** `code/part4_verify.py` compares this order with the order of Step 4.2 for three integrands. It
prints the value of each order, the absolute difference, and the smallest length of an inner interval
over a grid of the section. That smallest length is $2.500000 \times 10^{-2}$, so no inner interval
collapses. The script also prints the corner list of the section at $y = 0$ and at $y = 4$, and each
list holds 2 corners, so each of those sections is a segment.
