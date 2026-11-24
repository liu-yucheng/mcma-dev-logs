# Part 1, Step 1.2: The trace on the plane $y = 0$

Part goal: Turn the two surface equations into one inequality chain, then read the base and the top of the solid from that chain. No figure takes part in this reading.

## Reason

The lower wall is the plane $y = 0$. A point of that plane belongs to the solid exactly when the upper bound at its position is not negative.

## Computation

Set $y = 0$ in the chain: $0 \leq 4 - x^{2} - 4z^{2}$, which is the same statement as

$$x^{2} + 4z^{2} \leq 4.$$

This is an ellipse with semi-axis $2$ along $x$ and semi-axis $1$ along $z$. Its area is $\pi \cdot 2 \cdot 1 = 2\pi = 6.283185307$. The four extreme points are $(\pm 2, 0, 0)$ and $(0, 0, \pm 1)$.

## Result

The base of the solid is a filled ellipse of area $2\pi$. The solid stands on the plane $y = 0$.

## Verification

`code/part1_verify.py` compares a quadrature of the base area with the product of the two semi-axes, and both with a Monte Carlo estimate that carries its standard error. The three values agree within one standard error.
