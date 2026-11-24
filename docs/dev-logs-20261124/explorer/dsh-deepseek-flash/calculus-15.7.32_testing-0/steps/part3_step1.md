# Step 3.1 The inner interval of $y$ over the projection $D_{xz}$

**Reason.** The order $dy\,dx\,dz$ fixes $x$ and $z$ first and then integrates along a line
parallel to the $y$-axis. The two ends of that line are the two faces that the line meets,
so the interval follows from the face equations of Step 1.1 and not from the drawing.

**Computation.** For a fixed pair $(x, z)$ of the projection on the plane $y = 0$, the line
parallel to the $y$-axis enters the solid on the slanted face $x + y - 2z = 2$ and leaves it
on the face $y = 2$. The slanted face gives $y = 2 - x + 2z$, so the inner interval is

$$2 - x + 2z \le y \le 2.$$

The length of the interval is $x - 2z$, which is not negative exactly when $z \le x/2$, that
is exactly on the projection of Step 1.4.

**Result.** The inner interval of the order $dy\,dx\,dz$ is $2 - x + 2z \le y \le 2$, and the
projection $D_{xz}$ has the area {{p3.projection_area}}.

**A common mistake.** A reader may take the inner interval as $0 \le y \le 2$, but the limits
give $2 - x + 2z \le y \le 2$, because the lower end is the slanted face and not the plane
$y = 0$; the plane $y = 0$ meets the solid only at the point $(2, 0, 0)$.

**Check.** `code/part3_verify.py` integrates the length of the strips over the projection and
compares the result with the area of the corner list; it prints
{{p3.projection_area}} for both numbers and {{p3.check_passed}} passing checks out of
{{p3.check_count}}.
