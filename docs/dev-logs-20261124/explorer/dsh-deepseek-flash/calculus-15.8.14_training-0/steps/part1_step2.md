## Step 1.2 - Find the circle where the two surfaces meet

**Reason.** The two surfaces meet where they give the same height above the same point of the plane $z = 0$.
Setting the two heights equal turns the pair of equations into one equation in the squared distance $r^{2}$.
That equation decides the size of the circle, and the common height then follows from either surface.

**Computation.** Set the two heights equal and collect the squared distance on one side.

$$ r^{2} = 5 - r^{2} \quad \Longrightarrow \quad 2 r^{2} = 5 \quad \Longrightarrow \quad r^{2} = \frac{5}{2} $$

The common height follows from either surface at $r^{2} = \frac{5}{2}$.

$$ z = r^{2} = \frac{5}{2}, \qquad z = 5 - r^{2} = 5 - \frac{5}{2} = \frac{5}{2} $$

So the meeting set is the circle $x^{2} + y^{2} = \frac{5}{2}$ in the plane $z = \frac{5}{2}$.
Its radius is $\sqrt{\frac{5}{2}}$, which is about $1.5811$.

**Result.** A root search on the difference of the two heights returns the squared radius $2.500000000$ against the exact value $\frac{5}{2} = 2.5$ [scan [[check:part1:meeting_curve_root]]].
The same check walks 72 points of the circle: the two heights differ by at most $1.776 \times 10^{-15}$, and every common height differs from $\frac{5}{2}$ by at most $8.882 \times 10^{-16}$.
The check also prints the largest slope of the difference $5 - 2 r^{2}$ away from the axis, and that slope is $-0.030000$, which is negative, so the difference falls at every sampled point and the root is the only root.

**Common mistake.** A reader may take the radius of the circle for $\frac{5}{2}$, but the equation fixes the squared radius, so the radius is $\sqrt{\frac{5}{2}}$ and the squared radius is $\frac{5}{2}$.
