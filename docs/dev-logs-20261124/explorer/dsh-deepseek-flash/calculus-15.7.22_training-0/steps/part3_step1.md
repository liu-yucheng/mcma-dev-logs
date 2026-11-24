# Step 3.1: The shape of the slice comes from the inequalities

## Reason

A second computation checks the answer of Part 2. We cut the solid with the plane $y=c$ and take the
area $A(c)$ of the cut; then $V=\int A(c)\,dc$. The shape of the cut must come from the inequalities of
Step 1.2, and not from a figure.

## Computation

A point $(x,c,z)$ belongs to the solid exactly when both conditions hold:

$$x^2+z^2\le 4\qquad\text{and}\qquad z\le 4-c.$$

Thus the slice is the part of the disk that lies below the horizontal line $z=4-c$ of the plane of $x$
and $z$. The disk has $-2\le z\le 2$, so the position of the line gives three cases.

1. If $c\le 2$, then $4-c\ge 2$. The line misses the disk, and the slice is the full disk.
2. If $2<c\le 6$, then $-2\le 4-c<2$. The line cuts the disk, and the slice is a circular segment.
3. If $c>6$, then $4-c<-2$. The slice is empty.

The bottom plane gives $c\ge -1$. Thus the height of the solid covers $-1\le c\le 6$, and the height $6$
occurs at the single point $(0,6,-2)$.

## Check

The solid does not reach above $z=2$ and $-1$, so no slice exists for $c<-1$ or $c>6$. The line
$z=4-c$ is horizontal in the plane of $x$ and $z$, so the slice is symmetric about the $z$ axis and its
center lies on that axis.

## Result

The slice is the full disk for $-1\le c\le 2$ and a circular segment for $2<c\le 6$. The slice is empty
outside that range.

## Verification

`code/part3_verify.py` compares the closed form of Step 3.2 with an integration of the length of the
slice in the direction $z$ at nine heights from $-1$ to $6$. The largest difference is
$1.4\times10^{-14}$, against the accepted difference $10^{-8}$. The script also asserts that the area
does not increase with the height, that the area at $c=0$ and at $c=2$ equals the area of the disk, and
that the area at $c=6$ is $0$.
