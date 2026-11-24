## Step 1.3 - Decide which surface is on top

**Reason.** The body is the set of points between the two surfaces, so the drawing needs to know which surface is above the other.
The difference of the two heights answers that question at every squared distance, and its sign classifies each point of the plane $z = 0$.
The circle of Step 1.2 is where the sign changes.

**Computation.** Subtract the lower height from the upper height.

$$ z_{\text{upper}} - z_{\text{lower}} = (5 - r^{2}) - r^{2} = 5 - 2 r^{2} $$

The difference is positive exactly when $r^{2} < \frac{5}{2}$, it is zero at $r^{2} = \frac{5}{2}$, and it is negative outside that circle.
So the upper surface is above the lower surface inside the circle, the two surfaces meet on the circle, and the upper surface is below the lower surface outside the circle.
No point outside the circle lies between the two surfaces.

**Result.** The check prints the difference at six squared radii: $5, 3, 1, 0, -1, -3$ at $r^{2} = 0, 1, 2, 2.5, 3, 4$ [scan [[check:part1:above_below_order]]].
Inside the circle the smallest printed difference is $1.000000$, and outside the circle the largest printed difference is $-1.000000$, so the two signs are opposite.
Figure 1 draws the two paraboloids and the circle where they meet.

FIGURE: part1_figure1.png | The paraboloid $z = x^{2} + y^{2}$ (blue) and the paraboloid $z = 5 - x^{2} - y^{2}$ (orange), with the circle $x^{2} + y^{2} = \frac{5}{2}$, $z = \frac{5}{2}$ where they meet. One grid step is one unit on each axis.

**Common mistake.** A reader may take the whole upper paraboloid and the whole lower paraboloid as the boundary of the body, but the two surfaces cross on the circle, so only the part inside the circle bounds a body.

**Answer of Part 1.** The two paraboloids meet on the circle $x^{2} + y^{2} = \frac{5}{2}$ in the plane $z = \frac{5}{2}$, and the upper surface lies above the lower surface exactly inside that circle.
