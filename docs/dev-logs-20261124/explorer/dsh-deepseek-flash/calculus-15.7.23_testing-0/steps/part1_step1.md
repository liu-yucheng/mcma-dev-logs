# Part 1. The inequality description of the wedge

## Reason

A solid that three surfaces bound needs one inequality for each surface, and the first octant
adds three sign conditions. Write the conditions before any integral, because every limit of
the integral comes from one inequality.

## Computation

The cylinder $y^{2}+z^{2}=1$ has the axis $x$ and the radius $1$. The solid lies inside it, so
$y^{2}+z^{2}\le 1$.

The plane $y=x$ has two sides. The solid is the part of the cylinder that the two planes cut off
between them, so the point stays on the side $x\le y$. The condition $x\le y$ is the statement
that the point is on the far side of the plane $y=x$ from the $x$ axis.

The plane $x=1$ gives $x\le 1$. Inside the cylinder $y^{2}+z^{2}\le 1$ with $z\ge 0$ the
coordinate $y$ obeys $0\le y\le 1$, so $x\le y$ already gives $x\le 1$. The plane $x=1$
therefore adds no new point; it touches the wedge at the single corner $(1,1,0)$.

The first octant gives $x\ge 0$, $y\ge 0$, and $z\ge 0$.

The four conditions are

$$0\le x\le y,\qquad y^{2}+z^{2}\le 1,\qquad z\ge 0.$$

## Common mistake

A reader may take the condition of the plane $y=x$ as $y\le x$ and then read the base triangle
as the one with the corners $(0,0)$, $(1,0)$, and $(1,1)$. The inequality $x\le y$ gives the base
triangle with the corners $(0,0)$, $(0,1)$, and $(1,1)$; the two triangles are mirror images and
they give different volumes.

## Result

The wedge is the set of points with $0\le x\le y$, $y^{2}+z^{2}\le 1$, and $z\ge 0$. Figure 1
shows the four faces: the cylinder, the two planes, and the base.

The random sample of {{p1_sample_size}} points finds {{p1_hits}} points inside the solid, and the
two descriptions of the set agree on every point of the sample. The Monte Carlo volume is
{{p1_monte_carlo}} with a standard error of {{p1_monte_carlo_error}}, which is
{{p1_monte_carlo_z}} standard errors from the exact value of Part 3.

Verification: `code/part1_verify.py`.

![figure](FIGURE:part1_figure1.png|Figure 1. The wedge of Part 1. The cylinder and the two planes bound a solid with the base triangle $0\le x\le y\le 1$.)
