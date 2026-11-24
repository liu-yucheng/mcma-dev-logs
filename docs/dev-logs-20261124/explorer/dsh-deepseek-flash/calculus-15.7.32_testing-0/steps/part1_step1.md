# Step 1.1 The four surfaces and the four vertices

**Reason.** The statement names four surfaces and no other surface, so every point of the
solid $E$ obeys the four conditions $x \le 2$, $y \le 2$, $z \ge 0$, and $x + y - 2z \ge 2$.
A vertex of a solid that four planes bound is the meeting point of three of them, so the
candidate vertices are the solutions of the four triples of planes.

**Computation.** Each triple of the four planes has one meeting point:

| Triple of planes | Meeting point |
| --- | --- |
| $x = 2$, $y = 2$, $z = 0$ | $(2, 2, 0)$ |
| $x = 2$, $y = 2$, $x + y - 2z = 2$ | $(2, 2, 1)$ |
| $x = 2$, $z = 0$, $x + y - 2z = 2$ | $(2, 0, 0)$ |
| $y = 2$, $z = 0$, $x + y - 2z = 2$ | $(0, 2, 0)$ |

The four points are distinct, and their list is $(2, 2, 0)$, $(2, 2, 1)$, $(2, 0, 0)$, and
$(0, 2, 0)$. The count of the vertices is {{p1.vertex_count}}.

**Result.** The solid $E$ has {{p1.vertex_count}} vertices: $(2, 2, 0)$, $(2, 2, 1)$,
$(2, 0, 0)$, and $(0, 2, 0)$. The point $(1.5, 1.5, 0.25)$ lies inside $E$.

**A common mistake.** A reader may take the plane $x = 0$ or the plane $y = 0$ as a fifth
face of $E$, but the four half-spaces give a single point on each of those planes, and the
check `in the plane x = 0 the largest z equals 0` prints {{p1.z_on_x_zero_large}}.

**Check.** `code/part1_verify.py` solves the four triples and tests each point against the
four half-spaces; it prints the vertex list and the interior point among the {{p1.check_count}} checks
of the part, and {{p1.check_passed}} of them pass.
