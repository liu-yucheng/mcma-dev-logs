# Step 2.1 The inner interval of $z$ over the projection $D_{xy}$

**Reason.** The order $dz\,dx\,dy$ fixes $x$ and $y$ first and then integrates along a
vertical line. The two ends of that line are the two surfaces that the line meets, and the
length of the line must be the difference of the two bounding surfaces of Step 1.2.

**Computation.** For a fixed pair $(x, y)$ of the projection $D_{xy}$, the line parallel to
the $z$-axis enters the solid on the face $z = 0$ and leaves it on the face
$x + y - 2z = 2$. The face equation gives $z = (x + y - 2)/2$, so the inner interval is

$$0 \le z \le \frac{x + y - 2}{2}.$$

The length of the interval is $(x + y - 2)/2$, and its integral over the projection
$D_{xy}$ must be the volume. The length is negative outside $D_{xy}$, so the projection is
the set where the length is not negative.

**Result.** The inner interval of the order $dz\,dx\,dy$ is
$0 \le z \le (x + y - 2)/2$. The area of $D_{xy}$ is {{p2.projection_area}}, and the
integral of the length of the vertical segments over $D_{xy}$ is {{p2.value_dzdxdy}}, which
is the volume of Step 1.3.

**A common mistake.** A reader may take the whole square $0 \le x \le 2$, $0 \le y \le 2$
as the projection, but the limits give the triangle $x + y \ge 2$, and the check `full
square [0, 2] x [0, 2] as the projection: its signed integral differs from the volume`
prints {{p2.wrong_full_square}} against {{p2.volume_reference}}.

**Check.** `code/part2_verify.py` integrates the length of the strips over the projection and
compares the result with the area of the corner list; it prints
{{p2.projection_area}} for both numbers.
