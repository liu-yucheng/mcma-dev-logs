# Part 1, Step 2: Find the extent of the solid and the faces of the box that it touches

## The reason

A sketch needs a frame. The frame is the box that holds the solid. To find the box, we need the
largest and the smallest value of each of the three variables on the solid. The limits give these
values without a computation of an area or a volume.

## The computation

The outer pair gives $0 \le y \le 2$ at once, so the solid stays between the planes $y = 0$ and
$y = 2$.

For a fixed $y$, the pair of $z$ gives $0 \le z \le 2-y$. Because $y \ge 0$, the largest value of
$2-y$ is $2$, at $y = 0$. So $0 \le z \le 2$ on the whole solid.

For a fixed $y$, the pair of $x$ gives $0 \le x \le 4-y^{2}$. Because $y^{2} \ge 0$, the largest
value of $4-y^{2}$ is $4$, at $y = 0$. So $0 \le x \le 4$ on the whole solid.

The solid therefore lies in the box $[0,4] \times [0,2] \times [0,2]$. Each of the six faces of
this box meets the solid in a non-empty set:

| Face of the box | Set that the solid shares with the face |
| --- | --- |
| $y = 0$ | the whole rectangle $0 \le x \le 4$, $0 \le z \le 2$ |
| $y = 2$ | the single point $(0,2,0)$ |
| $z = 0$ | the region $0 \le y \le 2$, $0 \le x \le 4-y^{2}$ |
| $z = 2$ | the segment from $(0,0,2)$ to $(4,0,2)$ |
| $x = 0$ | the triangle $0 \le y \le 2$, $0 \le z \le 2-y$ |
| $x = 4$ | the segment from $(4,0,0)$ to $(4,0,2)$ |

So the box is the smallest box with faces parallel to the coordinate planes that holds the solid.
Every one of its faces touches the solid, and no smaller box does.

## The result

The extent of the solid is $4$ in the direction of $x$, $2$ in the direction of $y$, and $2$ in the
direction of $z$. The smallest box is $[0,4] \times [0,2] \times [0,2]$.

## The check

`code/part1_verify.py`, section "extent". The script computes the extent two ways: from the limits
by the argument above, and from the smallest and largest coordinates of the sampled points that
satisfy the limits. It reports the same triple $(4, 2, 2)$ from both ways.

`code/part1_verify.py`, section "volume". The script evaluates the integral in three different
orders of integration. The three values agree to the last digit, with a largest gap of $0$. The
script then evaluates the same integral a fourth time with exact rational arithmetic: it
multiplies the two sides $4-y^{2}$ and $2-y$ as polynomials with rational coefficients, and it
evaluates the antiderivative at the two ends of the interval. The exact value is $20/3$, and each
of the three numeric values agrees with it to $10^{-9}$. A numeric method and an exact method are
independent, so this comparison can fail. The problem asks for no number. This section is a check
of the reading of the limits, and it is not the answer to the exercise.
