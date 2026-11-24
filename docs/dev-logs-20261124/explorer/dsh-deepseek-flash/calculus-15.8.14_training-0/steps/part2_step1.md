## Step 2.1 - Find the footprint of the body on the plane $z = 0$

**Reason.** The drawing needs the outline of the body seen from above, because that outline is the region where the body stands.
A vertical line through a point of the plane $z = 0$ meets the body only when the two surfaces leave a gap at that point.
The gap is the difference of Step 1.3, so its sign decides the footprint.

**Computation.** A vertical line above the point $(x, y)$ meets the body when at least one height $z$ satisfies both surface inequalities.

$$ x^{2} + y^{2} \le z \le 5 - x^{2} - y^{2} $$

Such a height exists exactly when the lower bound does not exceed the upper bound.

$$ x^{2} + y^{2} \le 5 - x^{2} - y^{2} \quad \Longrightarrow \quad r^{2} \le \frac{5}{2} $$

So the footprint is the closed disk $\{(x, y) : x^{2} + y^{2} \le \frac{5}{2}\}$ in the plane $z = 0$.
Every point of that disk carries a vertical bar of the body, and no point outside it does.

**Result.** A grid of $801 \times 801$ points of the square $|x| \le 2$, $|y| \le 2$ tests the two conditions separately: the inequality on the squared distance and the existence of a height [scan [[check:part2:projection_membership]]].
The number of points where the two tests disagree is $0$, and the share of the feasible points whose middle height lies between the two surfaces is $1.000000$.
The largest radius of a feasible grid point is $1.581139$ against $\sqrt{\frac{5}{2}} = 1.581139$, and the smallest gap of the upper bound below the lower bound outside the disk is $-11.000000$, so no outside point is feasible.

**Common mistake.** A reader may take the footprint for a square, because the grid of the check is a square, but the grid is only the test region, and the footprint itself is the disk $r^{2} \le \frac{5}{2}$.
