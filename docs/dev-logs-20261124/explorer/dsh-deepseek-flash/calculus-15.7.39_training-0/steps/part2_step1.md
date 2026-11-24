# Step 2.1: Read the height of the solid at a fixed $x$

## Reason

The solid $E$ sits between the floor $z = 0$ and the ceiling $z = 1 + x + y$. A vertical slice at a fixed $x$ has an area. The volume is the integral of that area. So compute the area of the slice first.

## Work

Fix $x$ in $[0, 1]$. The slice is the part of $E$ with that value of $x$. Its base is the segment $0 \leq y \leq \sqrt{x}$. Its height at the point $y$ is $1 + x + y$.

The area of the slice is therefore

$$s(x) = \int_{0}^{\sqrt{x}} (1 + x + y)\, dy .$$

The integrand is linear in $y$, so

$$s(x) = (1 + x)\sqrt{x} + \frac{1}{2}\left(\sqrt{x}\right)^{2} = \sqrt{x} + x^{3/2} + \frac{x}{2}.$$

Three checks of this closed form:

- At $x = \frac{1}{4}$: $s = \frac{1}{2} + \frac{1}{8} + \frac{1}{8} = \frac{3}{4}$.
- At $x = \frac{1}{2}$: $s = 0.707107 + 0.353553 + 0.25 = 1.310660$.
- At $x = 1$: $s = 1 + 1 + \frac{1}{2} = \frac{5}{2}$.

The ceiling stays positive on $D$ because $1 + x + y \geq 1$. Its smallest value is $1$ at $(0, 0)$, and its largest value is $3$ at $(1, 1)$. So the solid has no part below the floor.

## Result

$s(x) = \sqrt{x} + x^{3/2} + \frac{x}{2}$ on $0 \leq x \leq 1$.

The ceiling runs from $z = 1$ to $z = 3$ over $D$.

Verification: `part2_verify.py` compares the closed form with a symbolic integral and with quadrature at $x = 0.25$, $x = 0.5$, and $x = 1$.
