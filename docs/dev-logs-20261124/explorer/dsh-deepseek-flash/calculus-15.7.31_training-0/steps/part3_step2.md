## Step 3.2. Write the order $dy\,dz\,dx$

**Why.** The outer variable is again $x$, so the section is the same triangle. The inner integral is now
in $y$, so the section is cut into horizontal pieces: a fixed value of $z$ selects one horizontal piece
that runs from the parabola to the plane.

**Derive the limits from the outside inward.** The outer variable is $x$, and $-2 \leq x \leq 2$. The
middle variable is $z$. In the section at a fixed $x$ the largest value of $z$ is at $y = x^{2}$, so
$0 \leq z \leq (4 - x^{2})/2$. The inner variable is $y$. At a fixed $x$ and a fixed $z$ the plane gives
$y \leq 4 - 2z$, and the parabola gives $y \geq x^{2}$. The order is

$$
\iiint_{E} f\,dV = \int_{-2}^{2}\int_{0}^{(4-x^{2})/2}\int_{x^{2}}^{4-2z} f(x,y,z)\,dy\,dz\,dx.
$$

**Read the inner piece.** At a fixed $x$ and a fixed $z$ the inner piece is a horizontal segment of
length $4 - 2z - x^{2}$. That length is 0 at $z = (4 - x^{2})/2$, which is the top corner of the
triangle.

**Compare the two orders of this part.** The two orders cover the same triangle, because Step 2.1 gives
one shape at a fixed $x$ and both orders use that shape. One order cuts the triangle into vertical
pieces and the other order cuts it into horizontal pieces. Each of the two orders has one inner integral,
and neither order splits an inner integral into two integrals.

**Result.** The second order is
$\int_{-2}^{2}\int_{0}^{(4-x^{2})/2}\int_{x^{2}}^{4-2z} f\,dy\,dz\,dx$. Its value for $f = 1$ is
$8.5333333333$, which is the value of the order of Step 3.1.

**Check.** `code/part3_verify.py` prints the value of both orders for three integrands and the absolute
difference of each pair. Each difference is below $10^{-12}$. The script also tests 5000 random points
against the limits of both orders of this part and prints the count of disagreements, and that count is
0 for each of the two orders. The six limit sets together are tested in Step 6.1.
Panel (b) of Figure 3 draws the horizontal inner pieces at $x = 1$, and the panel title of Figure 3
states that each piece runs from $x^{2}$ to $4 - 2z$.
