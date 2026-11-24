# Part 1. The region and its three projections

The problem gives three surfaces and no figure. This part turns the three surfaces into one system of
inequalities. Every later limit follows from that system.

## Step 1.1. Read the three surfaces as one system of inequalities

**Why.** A solid that three surfaces close is the set of points that lie on the inner side of each
surface. The problem supplies no fourth surface, so no extra bound is available. Each bound must come
from the three equations.

**Reason about each surface.** The equation $y = x^{2}$ does not contain $z$. It is therefore a
parabolic cylinder whose axis is parallel to the $z$-axis. For a point of the solid the relation is
$y \geq x^{2}$, because the other two surfaces meet the cylinder at $y = x^{2}$ and at $y = 4$, and the
solid lies between them.

The equation $z = 0$ is the floor. The solid lies above it, so $z \geq 0$.

The equation $y + 2z = 4$ gives $z = (4 - y)/2$. The solid lies below this plane, so
$z \leq (4 - y)/2$.

**Combine the three relations.** The floor and the plane together force $y \leq 4$. The reason is that
$z \geq 0$ and $z \leq (4 - y)/2$ hold at the same time. The system is therefore

$$
E = \left\{(x,y,z) : x^{2} \leq y \leq 4, \quad 0 \leq z \leq \frac{4-y}{2}\right\}.
$$

**Result.** The region $E$ is the set above the parabolic cylinder, above the floor, and below the
slanted plane. The two inequalities $x^{2} \leq y$ and $0 \leq z \leq (4-y)/2$ define it completely.

**Check.** `code/part1_verify.py` draws 20000 random points in the box
$[-2,2] \times [0,4] \times [0,2]$. It tests each point against the three surfaces directly
($y \geq x^{2}$, $z \geq 0$, $y + 2z \leq 4$) and against the bound chain. The script prints the count
of points that the two tests classify differently, and the count is 0. The script also tests the
rejected orientation $y \leq x^{2}$ and prints that this orientation admits the point with
$|x| = 1000$, so the interior side of the cylinder is fixed.
