## Step 1.2 The section at a fixed height is a rectangle

**Reason.** Set $z = z_{0}$ in the inequalities of Step 1.1. The bound of $x$ becomes $0 \le x \le 1 - z_{0}$, which
does not mention $y$. The bound of $y$ is $|y| \le \sqrt{1 - z_{0}}$, which does not mention $x$. Two independent
intervals of constant endpoints give a rectangle, and its sides are $1 - z_{0}$ and $2\sqrt{1 - z_{0}}$.

A reader may take the horizontal slice as an annulus, but the limits give a rectangle, because the same interval of
$x$ serves every $y$ of the slice.

**Computation.** The area is the product of the two sides:

$$A(z_{0}) = (1 - z_{0}) \cdot 2\sqrt{1 - z_{0}} = 2(1 - z_{0})^{3/2}$$

At $z_{0} = 0.5$ the four corners are {{p1_corners_at_z_half}}, and Figure 1 draws this rectangle in red.

**Result.** The section is {{p1_shape_at_z}} with the area {{p2_section_area_latex}}. The areas print
{{p1_area_at_z_table}}, and the shoelace area of the printed corners equals the closed form at each of these three
heights. Verified by `code/part1_verify.py`.
