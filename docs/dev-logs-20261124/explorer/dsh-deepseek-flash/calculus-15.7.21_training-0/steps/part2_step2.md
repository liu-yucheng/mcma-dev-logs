# Step 2.2 - State the volume as an integral over the shadow

Part 2: the projection and the vertical column.

## Reason

For each point of the shadow the solid is one vertical segment. A segment from $z = 0$ to $z = 1 - y$ has length $1 - y$. The volume of a stack of segments is the integral of the length over the base, so the triple integral collapses into a double integral of a known function.

## Computation

Fix $\left(x, y\right)$ in $D$. The vertical line through that point meets the floor at $z = 0$ and the roof at $z = 1 - y$. The length of the segment is

$$\int_{0}^{1 - y} dz = 1 - y.$$

Because $y \leq 1$ on $D$, the length is never negative. It is zero on the edge $y = 1$ and it is largest on the parabola $y = x^{2}$, where it equals $1 - x^{2}$.

## Result

$$V = \iint_{D} \left(1 - y\right) dA = \int_{-1}^{1} \int_{x^{2}}^{1} \left(1 - y\right) dy\, dx.$$

## Check

`code/part2_verify.py` scans $z$ at three points of the shadow. At $\left(0, 0.5\right)$ and at $\left(0.6, 0.5\right)$ it prints the admissible interval `0` to `0.5`, which is $0 \leq z \leq 1 - 0.5$. At $\left(-0.9, 0.95\right)$ it prints `0` to `0.05`, which is $0 \leq z \leq 1 - 0.95$. The script also prints the smallest roof height on the whole shadow, `0` at $y = 1$, so no column has a negative length.
