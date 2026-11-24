# Step 2.1 - Find the shadow of the solid in the $xy$ plane

Part 2: the projection and the vertical column.

## Reason

The chain of Step 1.1 gives $z$ between two functions of $y$ alone. A limit that does not mention $x$ or $z$ is the mark of a vertical column: at a fixed point of the $xy$ plane the solid occupies one interval of $z$. Therefore the volume is the integral over the shadow of the column height. The shadow is the set of points of the $xy$ plane where at least one $z$ exists.

## Computation

A pair $\left(x, y\right)$ belongs to the shadow when some $z$ satisfies $z \geq 0$ and $y + z \leq 1$. The two conditions on $z$ are compatible exactly when the lower limit does not exceed the upper limit:

$$0 \leq 1 - y \quad\Longleftrightarrow\quad y \leq 1.$$

Add the condition that comes from the cylinder, and the shadow is

$$D = \left\{(x, y) : -1 \leq x \leq 1,\; x^{2} \leq y \leq 1\right\}.$$

The roof passes through the shadow boundary $y = 1$, so the shadow contains that boundary and the column height there is zero.

## Result

The shadow is the region between the parabola $y = x^{2}$ and the line $y = 1$, from $x = -1$ to $x = 1$. Its area is

$$\int_{-1}^{1} \left(1 - x^{2}\right) dx = \left[x - \frac{x^{3}}{3}\right]_{-1}^{1} = \frac{4}{3}.$$

## Check

`code/part2_verify.py` scans $y$ at the fixed abscissas $x = 0$, $x = 0.6$, and $x = -0.9$. It prints the smallest and the largest admissible $y$ at each abscissa: `0` and `0.99999` at $x = 0$, `0.36` and `0.99999` at $x = 0.6$, `0.81` and `0.99999` at $x = -0.9$. These values agree with $y = x^{2}$ and $y = 1$ to the grid tolerance $2 \times 10^{-5}$.
