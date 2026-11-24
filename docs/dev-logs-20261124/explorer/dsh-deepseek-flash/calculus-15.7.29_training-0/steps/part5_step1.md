# Part 5, Step 5.1: The interval in $x$, and the question of a split

Part goal: Write the two orders whose innermost differential is $dx$, and decide whether the outer range needs a split.

## Reason

When the innermost integral is the one in $x$, the limits follow from the chain solved for $x$. A split is necessary only when the remaining region has two separate pieces at one value of the outer variable.

## Computation

Solve the chain for $x$: $x^{2} \leq 4 - y - 4z^{2}$, so

$$-\sqrt{4 - y - 4z^{2}} \leq x \leq \sqrt{4 - y - 4z^{2}}.$$

The full width in $x$ is $2\sqrt{4 - y - 4z^{2}}$. The remaining variables $(y, z)$ run over the set $0 \leq y \leq 4 - 4z^{2}$ and $-1 \leq z \leq 1$. At a fixed $z$ that set is one interval in $y$, so no split is needed.

## Result

The interval in $x$ is one interval, and the region of $(y, z)$ is one piece at every $z$. Neither of the two orders needs a split.

## Verification

`code/part5_verify.py` finds the half width in $x$ by a root search on the upper surface and compares it with the closed form $\sqrt{4 - y - 4z^{2}}$ at six positions. It then walks a line across the region of $(y, z)$ at 41 positions and counts the separate runs: the count is $1$ everywhere.
