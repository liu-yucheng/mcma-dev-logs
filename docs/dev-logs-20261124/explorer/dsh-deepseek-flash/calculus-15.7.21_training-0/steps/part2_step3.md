# Step 2.3 - Choose the order of integration

Part 2: the projection and the vertical column.

## Reason

The value of a multiple integral does not depend on the order of integration, but the work does. A good order makes every inner limit a single formula on the whole domain. A poor order splits the domain into two pieces or puts a square root in a limit. The chain of Step 1.1 already has $z$ between two functions of $y$, so $z$ must be the innermost variable.

## Computation

Write the three integrals from the inside out.

1. Innermost, $z$: from $0$ to $1 - y$. The bounds depend on $y$ only.
2. Middle, $y$: at a fixed $x$ the shadow runs from the parabola to the line, so from $x^{2}$ to $1$. The bounds depend on $x$ only.
3. Outermost, $x$: the shadow ends where the parabola meets the line, at $x = -1$ and $x = 1$.

This gives

$$V = \int_{-1}^{1} \int_{x^{2}}^{1} \int_{0}^{1 - y} dz\, dy\, dx.$$

For comparison, the order $dz\, dx\, dy$ splits the integral. At a fixed $y$ the width in $x$ is $2\sqrt{y}$, so that order needs the square root $\sqrt{y}$ but no split. The order $dy\, dz\, dx$ needs a split at $z = 1 - x^{2}$ in the middle limit, so we do not use it.

## Result

The nested integral above is the working form of the volume. Every limit is one of the three walls of Step 1.3: the inner limits are the floor and the roof, the middle limits are the cylinder and the sharp edge, and the outer limits are the two ends of the sharp edge.

## Check

`code/part2_verify.py` prints the three scans that these limits come from. The inner scan gives $0 \leq z \leq 1 - y$, the middle scan gives $x^{2} \leq y \leq 1$, and the outer scan gives $-1 \leq x \leq 1$. The script prints `0.99989` as the largest $x$ that still admits a point at $y = 0.9998$, and that value agrees with $\sqrt{0.9998}$ to the grid tolerance.
