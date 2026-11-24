# Part 2. The slice at a fixed height and the iterated integral

## Reason

An integral over a solid needs one order of the three variables, and each pair of limits must
come from the inequalities of Part 1. The height $z$ is the best outer variable here, because
the cylinder fixes its top and no other condition mentions it.

## Computation

Fix the height $z$ with $0\le z\le 1$. The inequality $y^{2}+z^{2}\le 1$ gives
$0\le y\le\sqrt{1-z^{2}}$, because $y\ge 0$. The inequality $x\le y$ then gives $0\le x\le y$.

The slice at the height $z$ is the triangle with the corners $(0,0)$, $(y_{\max},0)$, and
$(y_{\max},y_{\max})$ in the plane of the pair $(x,y)$, where $y_{\max}=\sqrt{1-z^{2}}$. Its
area is $y_{\max}^{2}/2=(1-z^{2})/2$.

The outer variable $z$ runs from $0$ to $1$, because $y^{2}+z^{2}\le 1$ with $y\ge 0$ needs
$z\le 1$.

The orders of the limits are $0\le z\le 1$, then $0\le y\le\sqrt{1-z^{2}}$, then $0\le x\le y$.
The volume is

$$V=\int_{0}^{1}\int_{0}^{\sqrt{1-z^{2}}}\int_{0}^{y}1\,dx\,dy\,dz .$$

Only the outer limit is a constant. The limit of $x$ is the variable $y$ of the middle
integral, so the inner two limits must be written in this order and they cannot be
interchanged.

## Common mistake

A reader may take the slice at the height $z$ as a rectangle of width $1$ and height $1$, but the
limits give the triangle $0\le x\le y\le\sqrt{1-z^{2}}$ and the area $(1-z^{2})/2$.

## Result

The slice areas at the heights {{p2_heights}} are {{p2_table_areas}}, and the widths of the slice along $y$ at those heights are
{{p2_widths}}. The integral of the slice area is {{p2_slice_integral}}. The sum of the
slice areas is the volume, so the iterated integral above is the answer to part (a).

Verification: `code/part2_verify.py` compares the closed form of the area with adaptive
quadrature and with a count of random points at each height. Figure 2 shows the two panels: the
quarter disk in the plane $x=0$ and the slice at $z=0.50$.

![figure](FIGURE:part2_figure1.png|Figure 2. Left: the quarter disk in the plane $x=0$, with the slice at $z=0.50$. Right: the slice at $z=0.50$ in the plane of the pair $(x,y)$.)
