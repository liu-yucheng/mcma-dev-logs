# Step 2.3: write a second order for the check of Part 4

## Reason

A second order gives a second set of limits for the same solid. The check of Part 4 uses it to reach the answer by another route, because two orders that agree on the value test the limits as well as the algebra.

A reader may write $0 \le z \le 3$ for every $x$ in this order, but the cylinder caps $z$ at $3\sqrt{1 - x^{2}}$, which falls to zero at $x = 1$.

## Computation

Take the outer variable $x$. The projection on the plane $y = 0$ gives $0 \le x \le 1$. At a fixed $x$ the cylinder gives $0 \le z \le 3\sqrt{1 - x^{2}}$. At a fixed pair $(x, z)$ the plane gives $3x \le y$, and the cylinder gives $y \le \sqrt{9 - z^{2}}$, which equals $3\sqrt{1 - x^{2}}$.

The volume of the solid in this order is

$$\int_{0}^{1} \int_{0}^{3\sqrt{1 - x^{2}}} \int_{3x}^{3} 1\,dy\,dz\,dx = {{p2_volume}}.$$

## Result

The order $dy\,dz\,dx$ gives the limits $3x \le y \le 3$, $0 \le z \le 3\sqrt{1 - x^{2}}$ and $0 \le x \le 1$, and its volume is ${{p2_volume}}$, which equals the volume of Part 1.

## Verification

`code/part2_verify.py` integrates all six orders with the same nested quadrature and compares each result with the volume of Part 1. Every order agrees within $10^{-7}$.
