# Part 2. The section of $E$ at a fixed coordinate

A section is the part of $E$ that one fixed value of one coordinate selects. Each section is a plane
figure, and the area of that figure is the length of one inner interval of an integration order. This
part derives the three shapes from the inequalities of Step 1.1. It does not take a shape from a
drawing.

## Step 2.1. Fix $x$: the section is a triangle

**Why.** The order $dz\,dy\,dx$ integrates over the section at a fixed $x$. The section supplies the
limits of $y$ and of $z$.

**Derive the shape.** Put $x = c$ in the system of Step 1.1. The system becomes
$c^{2} \leq y \leq 4$ and $0 \leq z \leq (4-y)/2$. The value of $y$ runs over an interval, and for each
$y$ the value of $z$ runs over an interval that shrinks as $y$ grows. In the plane of the section the
boundary is the line $z = 0$, the line $y = 4$, and the line $z = (4-y)/2$. These three lines cut a
triangle. Its corners are $(y,z) = (c^{2},0)$, $(4,0)$, and $(c^{2},(4-c^{2})/2)$.

**Compute the area.** The base of the triangle is $4 - c^{2}$ and its height is $(4 - c^{2})/2$. Then

$$
A_{x}(c) = \tfrac{1}{2}\,(4 - c^{2})\,\frac{4 - c^{2}}{2} = \frac{(4 - c^{2})^{2}}{4}.
$$

**Read the boundary values.** At $c = 0$ the corners are $(0,0)$, $(4,0)$, and $(0,2)$, and the area is
$4$. At $c = 1$ the corners are $(1,0)$, $(4,0)$, and $(1,1.5)$, and the area is $2.25$. At $c = 1.9$ the
corners are $(3.61,0)$, $(4,0)$, and $(3.61,0.195)$, and the area is $0.038025$. At $c = \pm 2$ the three
corners merge into the single point $(4,0)$, and the area is 0.

**Result.** The section at a fixed $x$ is a triangle with area $(4 - x^{2})^{2}/4$. At the two boundary
values $x = \pm 2$ the section is one point.

**Check.** `code/part2_verify.py` prints the corner list at each sampled value of $x$, computes the area
by the shoelace formula from those corners, and compares the result with an independent integral of the
height $(4-y)/2$ over the same interval of $y$. It prints both values at $c = 0$, $c = 1$, and $c = 1.9$.
Panel (a) of Figure 2 shows the section at $x = 0$. Panel (d) of Figure 2 marks the three sampled values
on the curve of $A_{x}$.
