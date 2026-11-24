## Step 2.2. Fix $y$: the section is a rectangle

**Why.** Four of the six orders integrate over the section at a fixed $y$. The section supplies the
limits of $x$ and of $z$.

**Derive the shape.** Put $y = d$ in the system of Step 1.1. The first inequality becomes $x^{2} \leq d$,
so $|x| \leq \sqrt{d}$. The second inequality becomes $0 \leq z \leq (4-d)/2$. Neither limit of $x$
depends on $z$, and neither limit of $z$ depends on $x$. The section is therefore a rectangle with
corners $(-\sqrt{d},0)$, $(\sqrt{d},0)$, $(\sqrt{d},(4-d)/2)$, and $(-\sqrt{d},(4-d)/2)$ in the plane of
$x$ and $z$.

**Compute the area.** The width is $2\sqrt{d}$ and the height is $(4-d)/2$, so

$$
A_{y}(d) = 2\sqrt{d} \cdot \frac{4-d}{2} = \sqrt{d}\,(4 - d).
$$

**Read the boundary values.** At $d = 0.5$ the corners are $(-0.707107,0)$, $(0.707107,0)$,
$(0.707107,1.75)$, $(-0.707107,1.75)$, and the area is $2.474873734$. At $d = 2$ the corners are
$(-1.414214,0)$, $(1.414214,0)$, $(1.414214,1)$, $(-1.414214,1)$, and the area is $2.828427125$. At
$d = 3.5$ the area is $0.935414347$. At $d = 0$ the width is 0, so the section is the segment from
$(0,0)$ to $(0,2)$ along the $z$-axis. At $d = 4$ the height is 0, so the section is the segment from
$(-2,0)$ to $(2,0)$ along the direction of $x$. Each of these two sections is a segment, and neither is
a point.

**Result.** The section at a fixed $y$ is a rectangle with area $\sqrt{y}\,(4-y)$. At $y = 0$ and at
$y = 4$ the section is a segment.

**Check.** `code/part2_verify.py` prints the corner list at each sampled value of $y$, computes the area
by the shoelace formula, and compares the result with the independent product of the two interval
lengths. The script also prints the number of distinct corners at $y = 0$ and at $y = 4$, and that number
is 2 at each value. Panel (b) of Figure 2 shows the section at $y = 2$.
