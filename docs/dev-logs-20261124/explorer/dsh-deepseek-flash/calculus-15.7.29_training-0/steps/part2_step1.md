# Part 2, Step 2.1: The outline of the projection

Part goal: Describe the projection that the two orders with an outer integral in $x$ or in $z$ need, and describe the section at a fixed height.

## Reason

A projection drops the coordinate that the plane does not keep. Here the coordinate $y$ drops. A position $(x, z)$ belongs to the projection when at least one height $y$ belongs to the solid at that position.

## Computation

The chain allows a height at $(x, z)$ exactly when $4 - x^{2} - 4z^{2} \geq 0$. So the projection is

$$D = \{(x, z) : x^{2} + 4z^{2} \leq 4\}$$

on the plane $y = 0$, with area $2\pi$. The projection keeps the coordinates $x$ and $z$, so its plane is $y = 0$.

## Result

The projection is one filled ellipse. It is the same set as the base, because the tallest wall stands directly above the base.

## Verification

`code/part2_verify.py` compares three descriptions of $D$: the inequality, a sweep in $x$, and a sweep in $z$. On 200 000 random points of the plane $y = 0$ the three descriptions give 0 disagreements.
