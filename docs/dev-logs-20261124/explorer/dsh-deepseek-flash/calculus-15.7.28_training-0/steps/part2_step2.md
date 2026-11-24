# Part 2, Step 2: Compute the area of the cut at five heights, and read the top of the solid

## The reason

The area of the cut is a function of the height. This function tells the reader how the solid
narrows as it rises. The same function later checks the drawing, because the drawn cuts must have
these areas.

## The computation

The cut is a rectangle with sides $4-y^{2}$ and $2-y$. The area of a rectangle is the product of
its two sides, so

$$
A(y) = (4-y^{2})(2-y), \qquad 0 \le y \le 2 .
$$

Then:

| $y$ | $4-y^{2}$ | $2-y$ | $A(y) = (4-y^{2})(2-y)$ |
| --- | --- | --- | --- |
| $0$ | $4$ | $2$ | $8$ |
| $0.5$ | $3.75$ | $1.5$ | $5.625$ |
| $1$ | $3$ | $1$ | $3$ |
| $1.5$ | $1.75$ | $0.5$ | $0.875$ |
| $2$ | $0$ | $0$ | $0$ |

Each value is smaller than the value below it. So each cut sits inside the cut below it, and the
solid narrows at every step upward.

At $y = 2$ both sides are $0$. The rectangle becomes the single point $(0,2,0)$, which is the
corner $T$ of Part 3. The point is the whole cut, and its area is $0$. The printed corner list of
the check gives one corner at that height and four corners at every lower height, so the collapse
is a collapse to a point and not to a segment.

## The result

The area of the cut is $A(y) = (4-y^{2})(2-y)$. Its values at the heights $0$, $0.5$, $1$, $1.5$,
and $2$ are $8$, $5.625$, $3$, $0.875$, and $0$. The highest cut is the single point
$T = (0,2,0)$.

## The check

`code/part2_verify.py`, section "area". For each height, the script measures the area of the cut in
two ways. The first way multiplies the two sides of the rectangle. The second way draws a large
random sample in the box $[0,4] \times [0,2]$, keeps the points that satisfy the two limits, and
counts them. The relative gap of the two ways is at most $4.71\times10^{-4}$, and the script
asserts a gap below $5\times10^{-3}$.

`code/part2_verify.py`, section "misreading". The script also computes the area of the cut that the
misreading $0 \le x \le 4-z^{2}$ would give. At $y = 0$ that area is $5.333\ldots$ and the correct
area is $8$. At $y = 1$ that area is $3.666\ldots$ and the correct area is $3$. The two readings
differ, so the checks of this part can tell them apart.
