# Part 5. The two orders with $z$ outermost

The outer variable is $z$, so the section is the one at a fixed $z$. Step 2.3 gives its shape: a
parabolic segment. The values of $z$ run from 0 to 2, and the top value 2 is the value at which the
segment shrinks to one point.

## Step 5.1. Write the order $dy\,dx\,dz$

**Why.** The inner integral is in $y$ and the middle integral is in $x$. In the segment at a fixed $z$
the value of $y$ runs from the parabola to the horizontal line, and the limits of $y$ depend on $x$. The
inner integral is therefore a single integral, and the middle interval of $x$ is set by the widest row
of the segment.

**Derive the limits from the outside inward.** The outer variable is $z$. Step 1.2 gives $0 \leq z \leq 2$.
The middle variable is $x$. The section at a fixed $z$ has $x^{2} \leq 4 - 2z$, so
$-\sqrt{4-2z} \leq x \leq \sqrt{4-2z}$. The inner variable is $y$, and $x^{2} \leq y \leq 4 - 2z$. The
order is

$$
\iiint_{E} f\,dV = \int_{0}^{2}\int_{-\sqrt{4-2z}}^{\sqrt{4-2z}}\int_{x^{2}}^{4-2z} f(x,y,z)\,dy\,dx\,dz.
$$

**Read the inner piece.** At a fixed $x$ and a fixed $z$ the inner piece is a vertical segment of length
$4 - 2z - x^{2}$. That length is 0 at the two ends of the interval of $x$.

**Result.** The fifth order is
$\int_{0}^{2}\int_{-\sqrt{4-2z}}^{\sqrt{4-2z}}\int_{x^{2}}^{4-2z} f\,dy\,dx\,dz$. Its value for $f = 1$
is $8.5333333333$.

**Check.** `code/part5_verify.py` compares this order with the order of Step 5.2 for three integrands. It
prints the value of each order, the absolute difference, and the smallest length of an inner interval
over a grid of the section. That smallest length is $3.960000 \times 10^{-3}$, so no inner interval
collapses. Panel (a) of Figure 4 draws the vertical inner pieces at $z = 0.5$.
