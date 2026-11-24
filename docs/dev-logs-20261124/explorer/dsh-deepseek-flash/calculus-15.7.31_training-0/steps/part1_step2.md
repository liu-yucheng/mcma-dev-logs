## Step 1.2. Project the region on each coordinate plane

**Why.** An integration order needs the projection of $E$ on the plane of its two outer coordinates.
The projection supplies the outer limits. A projection that drops the coordinate $y$ lies on the plane
$y = 0$, and a projection that drops $x$ lies on the plane $x = 0$.

**Project on the plane $z = 0$, which keeps $x$ and $y$.** Remove $z$ from the system. The result is
$x^{2} \leq y \leq 4$. The largest value of $|x|$ is 2, and it comes from $x^{2} \leq y \leq 4$. The
area of this region is

$$
\int_{-2}^{2} (4 - x^{2})\,dx = \left[4x - \frac{x^{3}}{3}\right]_{-2}^{2} = \frac{32}{3}.
$$

**Project on the plane $x = 0$, which keeps $y$ and $z$.** Remove $x$ from the system. The result is
$0 \leq y \leq 4$ and $0 \leq z \leq (4-y)/2$. This region is the triangle with corners $(0,0)$,
$(4,0)$, and $(0,2)$. Its area is $\frac{1}{2} \cdot 4 \cdot 2 = 4$.

**Project on the plane $y = 0$, which keeps $x$ and $z$.** Remove $y$ from the system. The relation
$x^{2} \leq y \leq 4$ gives $x^{2} \leq 4$, so $|x| \leq 2$. The plane gives
$z \leq (4 - y)/2$, and the smallest value of $y$ is $x^{2}$. The largest value of $z$ at a fixed $x$
is therefore $(4 - x^{2})/2$. The region is

$$
0 \leq z \leq \frac{4 - x^{2}}{2}, \qquad -2 \leq x \leq 2,
$$

and its area is $\int_{-2}^{2} \frac{4 - x^{2}}{2}\,dx = \frac{16}{3}$.

**Result.** The three projections have the areas $32/3$, $4$, and $16/3$. The coordinate ranges are
$|x| \leq 2$, $0 \leq y \leq 4$, and $0 \leq z \leq 2$. Every integration limit of this tutorial comes
from one of these three regions.

**Check.** `code/part1_verify.py` computes each area twice: once by a quadrature of the region and once
by the closed form above. It prints both values for each plane. Figure 1 shows the solid and the three
projections side by side, and panel (b), panel (c), and panel (d) of Figure 1 carry the titles
"Projection on the plane $z = 0$", "Projection on the plane $x = 0$", and
"Projection on the plane $y = 0$" with the two coordinates that each panel keeps.
