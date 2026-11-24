# Part 2, Step 1: The horizontal section at a height, and its radius

## Reason

The volume of any solid follows from the areas of its horizontal sections, because a thin slab
of thickness $\Delta z$ has volume close to $A(z)\,\Delta z$. The area of a section is
$\pi$ times the square of its radius, so the work is to find that radius at each height from the
inequalities and not from the picture.

## Computation

Fix a height $z$ with $0\le z\le 10$. The cylinder allows every point with $x^{2}+y^{2}\le 9$
at that height, and the cap allows nothing, since the cap starts at $z=10$. The section is the
disk of radius $3$.

Fix a height $z$ with $10<z\le 13$. The cylinder allows nothing at that height. The cap allows
the points that satisfy $x^{2}+y^{2}\le 9-(z-10)^{2}$. The section is again a disk, and its
radius is

$$s(z)=\sqrt{9-(z-10)^{2}},\qquad 10\le z\le 13 .$$

## Result

The section at the height $z$ is a disk, and its radius is

$$s(z)=\begin{cases}3, & 0\le z\le 10,\\ \sqrt{9-(z-10)^{2}}, & 10\le z\le 13 .\end{cases}$$

A section is never an annulus, because the body has no inner void: the axis $r=0$ belongs to
every section. The area of the section is $A(z)=\pi s(z)^{2}$.

## Common mistake

A reader may take every section of the cap as a disk of radius $3$, but the inequality gives a
shrinking radius; Figure 2 shows the area falling to zero at $z=13$.

## Verification

Verification script: `code/part2_verify.py` check C1 compares the formula above with a bisection search on the
membership test at the nine heights $0,2,6,10,10.2,11,11.5,12.5,12.95$ and prints a maximum
difference of $5.662\times 10^{-15}$. That search uses no formula: it moves the end points of
an interval until the interval is shorter than $10^{-12}$.
