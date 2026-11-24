# Part 2, Step 2.2: The section at a fixed height

Part goal: Describe the projection that the two orders with an outer integral in $x$ or in $z$ need, and describe the section at a fixed height.

## Reason

At a fixed height $y$ the section is the set of positions where the upper bound reaches at least that height. The section is a set in a plane of constant $y$, so it keeps the coordinates $x$ and $z$.

## Computation

Set $y$ to a constant in the chain: $x^{2} + 4z^{2} \leq 4 - y$. This is a filled ellipse with semi-axes $\sqrt{4 - y}$ and $\frac{1}{2}\sqrt{4 - y}$, so its area is

$$A(y) = \pi \cdot \sqrt{4 - y} \cdot \frac{\sqrt{4 - y}}{2} = \frac{\pi (4 - y)}{2}.$$

The section is filled, not a ring: the inequality has the form $x^{2} + 4z^{2} \leq$ a number, so it holds at the center $(0, y, 0)$ and along every radial line from the center to the outline.

## Result

The area falls from $2\pi = 6.283185307$ at $y = 0$ to $0$ at $y = 4$. At $y = 2$ the area is $\pi = 3.141592654$.

## Verification

`code/part2_verify.py` measures the area at seven heights by three methods: a quadrature of the half width, the ellipse formula with the measured semi-axes, and the closed form $\pi (4 - y)/2$. The largest difference is below $1.1 \times 10^{-14}$. The same script walks 720 radial directions at the heights $0$, $2$, and $3.9$ and tests a point at half the radius: a ring would fail that test, and it never fails.
