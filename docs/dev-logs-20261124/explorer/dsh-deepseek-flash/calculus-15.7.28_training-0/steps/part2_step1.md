# Part 2, Step 1: Cut the solid at a fixed height, and name the shape of the cut

## The reason

A three dimensional solid is hard to read from its limits directly. A cut at one fixed height
turns the solid into a flat region. A flat region has a shape, and a shape has a name, a boundary,
and an area. The shape is the first thing that a reader must see in the sketch.

## The computation

Fix $y = c$ with $0 \le c \le 2$. The three pairs of Part 1, Step 1 become two conditions on $x$
and $z$, because the condition on $y$ is now true:

$$
0 \le z \le 2-c, \qquad 0 \le x \le 4-c^{2}.
$$

The condition on $z$ holds the number $c$ and does not hold $x$. The condition on $x$ holds the
number $c$ and does not hold $z$. So the value of $x$ is free inside its interval, whatever the
value of $z$ may be. The cut is therefore the set of all pairs $(x,z)$ with $x$ in one interval
and $z$ in another interval. That set is the product of the two intervals:

$$
\text{cut}(c) = [0,\,4-c^{2}] \times [0,\,2-c].
$$

A product of two closed intervals is a rectangle. Its four sides lie on the lines $x = 0$,
$x = 4-c^{2}$, $z = 0$, and $z = 2-c$. Its four corners are

$$
(0,c,0), \quad (0,c,2-c), \quad (4-c^{2},c,0), \quad (4-c^{2},c,2-c).
$$

The cut is a rectangle and it is not a disk. The reason is the structure of the limits: no limit
ties $x$ to $z$. A disk would need a limit of the form $x \le \sqrt{\rho^{2}-z^{2}}$, and no such
limit appears here.

## The result

For every $c$ with $0 \le c < 2$, the cut of the solid at the height $y = c$ is the rectangle
$[0,4-c^{2}] \times [0,2-c]$ in the plane $y = c$. Its sides are $4-c^{2}$ and $2-c$.

## The check

`code/part2_verify.py`, section "shape". For each of five heights, the script tests the sampled
points of the cut against the rectangle and against the disk of the same corner. It reports $0$
disagreements with the rectangle at every height, and it reports more than 1000 disagreements with
the disk at every height. So the test separates the two shapes, and the rectangle survives.
