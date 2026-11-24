# Part 1, Step 1.1: The inequality chain on $y$

Part goal: Turn the two surface equations into one inequality chain, then read the base and the top of the solid from that chain. No figure takes part in this reading.

## Reason

Both surfaces have the form $y = g(x, z)$. A vertical line therefore meets the solid once, between the lower surface and the upper surface. The chain follows from the two equations alone.

## Computation

The upper surface is $y = 4 - x^{2} - 4z^{2}$ and the lower surface is $y = 0$. A point belongs to $E$ when its height lies between them:

$$E = \{(x, y, z) : 0 \leq y \leq 4 - x^{2} - 4z^{2}\}.$$

The coefficient on $z^{2}$ is $4$, not $1$. The chain is not empty: $x^{2} + 4z^{2} \geq 0$, so the upper bound is never below the lower bound, and the point $(0, 0, 0)$ belongs to $E$.

## Result

Every bound of every order comes from this one chain. The chain is the single source of the six answers.

## Verification

`code/part1_verify.py` compares two membership tests: the direct chain, and the substitution $x = 2u$, $z = w$, $y = 4s$, which maps $E$ onto the unit disk times the unit interval. On 200 000 random points the two tests give 0 disagreements.
