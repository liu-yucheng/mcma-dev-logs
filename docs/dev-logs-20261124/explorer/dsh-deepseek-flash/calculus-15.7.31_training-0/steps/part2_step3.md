## Step 2.3. Fix $z$: the section is a parabolic segment

**Why.** The two orders with $z$ outermost integrate over the section at a fixed $z$. The section
supplies the limits of $x$ and of $y$.

**Derive the shape.** Put $z = e$ in the system of Step 1.1. The second inequality becomes
$0 \leq e \leq (4-y)/2$, which is the same as $y \leq 4 - 2e$. Together with $x^{2} \leq y$ the section is

$$
x^{2} \leq y \leq 4 - 2e, \qquad -\sqrt{4-2e} \leq x \leq \sqrt{4-2e}.
$$

The lower boundary is the parabola $y = x^{2}$. The upper boundary is the horizontal line
$y = 4 - 2e$. The section is the part of the parabolic region that lies below that line.

**Compute the area.** Integrate the height $4 - 2e - x^{2}$ over the interval of $x$:

$$
A_{z}(e) = \int_{-\sqrt{4-2e}}^{\sqrt{4-2e}} \left(4 - 2e - x^{2}\right) dx
         = \frac{4}{3}\,(4 - 2e)^{3/2}.
$$

**Read the boundary values.** At $e = 0$ the limits of $x$ are $\pm 2$, and the area is
$10.666666667$. At $e = 1$ the limits of $x$ are $\pm 1.414214$, and the area is $3.771236166$. At
$e = 1.5$ the limits of $x$ are $\pm 1$, and the area is $1.333333333$. At $e = 2$ the limits of $x$
merge at 0 and the upper line meets the parabola at $y = 0$, so the section is the single point
$(0,0)$ in the plane of $x$ and $y$.

**Result.** The section at a fixed $z$ is a parabolic segment with area
$\frac{4}{3}(4 - 2z)^{3/2}$. At $z = 2$ the section is one point.

**Check.** `code/part2_verify.py` computes the area at each sampled value of $z$ in two ways: by an
adaptive quadrature of the height (4 - 2e - x squared) over the interval of $x$, and by the closed form
above. It prints both values and the difference. The script also prints the number of distinct corners
at $z = 2$, and that number is 1. Panel (c) of Figure 2 shows the section at $z = 0.5$.
