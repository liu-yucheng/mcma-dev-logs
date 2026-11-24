# Part 4, Step 4.1: The interval in $z$, and the question of a split

Part goal: Write the two orders whose innermost differential is $dz$, and decide whether the outer range needs a split.

## Reason

When the innermost integral is the one in $z$, the limits follow from the chain solved for $z$. A split is necessary only when the remaining region has two separate pieces at one value of the outer variable.

## Computation

Solve the chain for $z$: $4z^{2} \leq 4 - x^{2} - y$, so

$$-\frac{1}{2}\sqrt{4 - x^{2} - y} \leq z \leq \frac{1}{2}\sqrt{4 - x^{2} - y}.$$

The full width in $z$ is $\sqrt{4 - x^{2} - y}$. The remaining variables $(x, y)$ run over the set $0 \leq y \leq 4 - x^{2}$. At a fixed $x$ that set is one interval in $y$, so no split is needed.

## Result

The interval in $z$ is one interval, and the region of $(x, y)$ is one piece at every $x$. Neither of the two orders needs a split.

## Verification

`code/part4_verify.py` finds the half width in $z$ by a root search on the upper surface and compares it with the closed form $\sqrt{4 - x^{2} - y}/2$ at five positions. It then walks a line across the region of $(x, y)$ at 41 positions of $x$ and counts the separate runs: the count is $1$ everywhere.
