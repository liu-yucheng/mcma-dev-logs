# Step 1.1: Read the bounds of the planar region $D$

## Reason

The ceiling of $E$ is $z = 1 + x + y$. It is a height above a base in the $xy$-plane. The base decides the limits of $x$ and $y$. So read the base first.

## Work

The statement bounds the base with three curves: $y = \sqrt{x}$, $y = 0$, and $x = 1$.

The curves $y = 0$ and $y = \sqrt{x}$ meet where $\sqrt{x} = 0$. That point is $x = 0$. So the base starts at $x = 0$.

The line $x = 1$ closes the base on the right. So $0 \leq x \leq 1$.

At a fixed $x$ in that interval, the base runs from the lower curve $y = 0$ to the upper curve $y = \sqrt{x}$. So $0 \leq y \leq \sqrt{x}$.

The region has one description of the form "fixed $x$, then $y$". This form is a Type I region. The same region also has the description "fixed $y$, then $x$": $0 \leq y \leq 1$ and $y^2 \leq x \leq 1$.

## Result

$D = \{(x, y) : 0 \leq x \leq 1,\ 0 \leq y \leq \sqrt{x}\}$.

The horizontal form of the same region is $0 \leq y \leq 1$ and $y^{2} \leq x \leq 1$.

Verification: `part1_verify.py` compares the two descriptions of $D$ on a grid of $2001 \times 2001$ points. The two descriptions accept the same points, away from the boundary rounding.
