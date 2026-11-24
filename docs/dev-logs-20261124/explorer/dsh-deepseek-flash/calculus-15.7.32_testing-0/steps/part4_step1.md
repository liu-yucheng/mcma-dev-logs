# Step 4.1 The inner interval of $x$ over the projection $D_{yz}$

**Reason.** The order $dx\,dy\,dz$ fixes $y$ and $z$ first and then integrates along a line
parallel to the $x$-axis. As in Part 3, the two ends of the line are the two faces that the
line meets, and these faces are read from the equations of Step 1.1.

**Computation.** For a fixed pair $(y, z)$ of the projection on the plane $x = 0$, the line
parallel to the $x$-axis enters the solid on the slanted face $x + y - 2z = 2$ and leaves it
on the face $x = 2$. The slanted face gives $x = 2 - y + 2z$, so the inner interval is

$$2 - y + 2z \le x \le 2.$$

The length of the interval is $y - 2z$, which is not negative exactly when $z \le y/2$, that
is exactly on the projection of Step 1.4.

**Result.** The inner interval of the order $dx\,dy\,dz$ is $2 - y + 2z \le x \le 2$, and the
projection $D_{yz}$ has the area {{p4.projection_area}}.

**A common mistake.** A reader may take the inner interval as $0 \le x \le 2$, but the limits
give $2 - y + 2z \le x \le 2$, because the plane $x = 0$ meets the solid only at the point
$(0, 2, 0)$ and does not bound a face.

**Check.** `code/part4_verify.py` integrates the length of the strips over the projection and
compares the result with the area of the corner list; it prints
{{p4.projection_area}} for both numbers and {{p4.check_passed}} passing checks out of
{{p4.check_count}}.
