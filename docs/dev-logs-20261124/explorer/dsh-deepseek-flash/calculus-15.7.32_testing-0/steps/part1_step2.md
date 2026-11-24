# Step 1.2 The coordinate inequalities and the closure of the solid

**Reason.** An order of integration needs one variable between two functions of the other
two. The four conditions of Step 1.1 give the height $z$ between two functions of $x$ and
$y$, and they give the range of $x$ and of $y$ on their own. A lower bound of an integral
must come from a surface that belongs to the solid, so the bound $z \ge 0$ comes from the
face $z = 0$ and the bound $x + y \ge 2$ comes from the face $x + y - 2z = 2$.

**Computation.** Divide the fourth condition by two and move the terms:

$$x + y - 2z \ge 2 \iff z \le \frac{x + y - 2}{2}.$$

The condition $z \ge 0$ together with this bound forces $x + y \ge 2$, because a height
that is at least zero and at most $(x + y - 2)/2$ exists only when $(x + y - 2)/2 \ge 0$.
The two conditions $x \le 2$ and $y \le 2$ need no partner from below, since the condition
$x + y \ge 2$ with $x \le 2$ and $y \le 2$ already gives $x \ge 0$ and $y \ge 0$. Hence

$$E = \{(x, y, z) : 0 \le x \le 2,\ 0 \le y \le 2,\ 0 \le z \le \tfrac{1}{2}(x + y - 2)\}.$$

The lower bounds $x \ge 0$ and $y \ge 0$ are consequences and not faces: the plane $x = 0$
meets $E$ only at $(0, 2, 0)$, and the plane $y = 0$ meets $E$ only at $(2, 0, 0)$.

**Result.** The solid is the set of the points with $0 \le x \le 2$, $0 \le y \le 2$, and
$0 \le z \le (x + y - 2)/2$. The four named planes are the four faces, and no fifth surface
is needed.

**A common mistake.** A reader may take the box $0 \le x \le 2$, $0 \le y \le 2$,
$0 \le z \le 1$ as the solid, but the slanted plane cuts that box along the diagonal, and the
check `base times height without the factor one third differs from the volume of E` prints
{{p1.volume_without_third}} against the volume ${{p1.volume_latex}}$.

**Check.** `code/part1_verify.py` takes random points and boundary points, tests them
against the four half-spaces, tests them against the inequalities above, and reports the
number of disagreeing points; it also solves four linear programs for the extreme values of
$x$, $y$, and $z$ and prints the largest height {{p1.z_largest}}.
