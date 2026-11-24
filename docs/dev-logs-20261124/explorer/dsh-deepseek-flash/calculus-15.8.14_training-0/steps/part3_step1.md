## Step 3.1 - Write the inequality description of the body

**Reason.** The problem asks for a drawing, and a drawing of a solid is only as good as the description that it shows.
An inequality description lists the points of the body in one line, so a reader can test any point against it.
The description follows from the two surface inequalities together with the footprint of Step 2.1.

**Computation.** The body is the set of points between the two surfaces.

$$ E = \left\{(x, y, z) : x^{2} + y^{2} \le z \le 5 - x^{2} - y^{2}\right\} $$

The two outer inequalities already force the footprint, because the lower bound must not exceed the upper bound.
With $r^{2} = x^{2} + y^{2}$ the same set reads as follows.

$$ E = \left\{(r, \theta, z) : r^{2} \le \frac{5}{2}, \ r^{2} \le z \le 5 - r^{2}\right\} $$

The set is closed, it is bounded, and it holds the meeting circle of Step 1.2 on its boundary.

**Result.** The check tests 200000 random points of a box that holds the body against both forms of the description [scan [[check:part3:description_matches_forms]]].
The number of points where the two forms disagree is $0$.
The share of the sampled box that the body holds is $0.320165$, which lies between $0$ and $1$, so the sampled box holds both points of the body and points outside it.

**Common mistake.** A reader may take the condition $r^{2} \le \frac{5}{2}$ for an extra restriction that the cartesian form does not carry, but the cartesian form implies it, because the lower bound must not exceed the upper bound.
