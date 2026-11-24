# Step 1.4 The three projections

**Reason.** An order of integration is a description of the solid by three nested intervals,
and the two outer intervals are the projection of the solid on a coordinate plane. A point
lies in the projection on the plane $z = 0$ when some point of the solid has that pair
$(x, y)$, so the projection is the set of the pairs that the inequalities of Step 1.2 admit
for some $z$.

**Computation.** The pair $(x, y)$ is admissible when $0 \le x \le 2$, $0 \le y \le 2$, and
$(x + y - 2)/2 \ge 0$, that is $x + y \ge 2$. So the projection on the plane $z = 0$ is the
triangle with the corners $(2, 0)$, $(0, 2)$, and $(2, 2)$, and its area is
{{p1.projection_xy_area}}.

The pair $(x, z)$ is admissible when $0 \le x \le 2$ and some $y$ in the interval
$0 \le y \le 2$ obeys $y \ge 2 - x + 2z$. Such a $y$ exists exactly when
$2 - x + 2z \le 2$, that is $z \le x/2$. So the projection on the plane $y = 0$ keeps the
coordinates $x$ and $z$, and it is the triangle with the corners $(0, 0)$, $(2, 0)$, and
$(2, 1)$, whose area is {{p1.projection_xz_area}}.

The pair $(y, z)$ is admissible when $0 \le y \le 2$ and $z \le y/2$, because the same
argument with the roles of $x$ and $y$ exchanged applies. So the projection on the plane
$x = 0$ keeps the coordinates $y$ and $z$, and it is the triangle with the corners
$(0, 0)$, $(2, 0)$, and $(2, 1)$, whose area is {{p1.projection_yz_area}}.

Figure 2 draws the three projections.

!figure part1_figure2.png | The three projections of $E$: $D_{xy}$ on the plane $z = 0$ with area {{p1.projection_xy_area}}, $D_{xz}$ on the plane $y = 0$ with area {{p1.projection_xz_area}}, and $D_{yz}$ on the plane $x = 0$ with area {{p1.projection_yz_area}}.

**Result.** The projection on the plane $z = 0$ is the triangle of the corners
{{p1.projection_xy_corners}} with area {{p1.projection_xy_area}}. The projection on the
plane $y = 0$ is the triangle of the corners {{p1.projection_xz_corners}} with area
{{p1.projection_xz_area}}. The projection on the plane $x = 0$ is the triangle of the
corners {{p1.projection_yz_corners}} with area {{p1.projection_yz_area}}. Figure 2 shows
all three projections.

**A common mistake.** A reader may take the projection on the plane $y = 0$ for the
rectangle $0 \le x \le 2$, $0 \le z \le 1$, but the slanted plane gives the upper bound
$z \le x/2$, and the corner list of the check holds only three corners.

**Check.** `code/part1_verify.py` compares each projection area from its corner list with
the fraction of random points that the projection admits; it prints
{{p1.projection_xy_area}}, {{p1.projection_xz_area}}, and {{p1.projection_yz_area}}.
