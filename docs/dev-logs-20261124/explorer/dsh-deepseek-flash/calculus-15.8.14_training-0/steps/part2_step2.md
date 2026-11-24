## Step 2.2 - Find the shape and the area of one horizontal section

**Reason.** The drawing shows the body from the outside, so the reader needs the shape of a slice to trust the drawn outline.
A horizontal section at a fixed height is the set of points of the plane at that height that lie inside the body.
The two surface inequalities then reduce to one inequality on the squared distance, and the section is a disk.

**Computation.** Fix the height $z$ between $0$ and $5$. A point of the plane at that height lies in the body when both surface inequalities hold.

$$ x^{2} + y^{2} \le z \quad \text{and} \quad z \le 5 - x^{2} - y^{2} $$

The two inequalities give one upper bound on the squared distance.

$$ r^{2} \le z \quad \text{and} \quad r^{2} \le 5 - z \quad \Longrightarrow \quad r^{2} \le \min(z, 5 - z) $$

So the section is the closed disk of radius $\sqrt{\min(z, 5 - z)}$, and its area is the following.

$$ A(z) = \pi \min(z, 5 - z) $$

The area grows with $z$ below the meeting height and falls above it, because the smaller of the two bounds changes at $z = \frac{5}{2}$.

**Result.** The check computes the area of the section at three heights in two ways: an integral of $2 \pi r$ over the radius that the inequalities allow, and a count of cells of a fine grid [scan [[check:part2:section_area_three_heights]]].
At $z = 0.5$ the integral gives $1.570796327$ and the formula $\pi \min(z, 5 - z)$ gives $1.570796327$, and the cell count gives $1.570900$.
At $z = 2.5$ the two values are $7.853981634$ and $7.853981634$, and the cell count gives $7.854725$.
At $z = 4.5$ the two values are $1.570796327$ and $1.570796327$, and the cell count gives $1.570900$.
The cell count is larger than the integral at every row because a cell counts as inside when its centre is inside.

**Common mistake.** A reader may take every section for a disk of the same radius, because the formula has one symbol $z$, but the radius follows $\min(z, 5 - z)$, so the sections below the meeting height grow and the sections above it shrink.
