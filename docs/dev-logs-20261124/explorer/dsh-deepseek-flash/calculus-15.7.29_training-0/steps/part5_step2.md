# Part 5, Step 5.2: The order $dx\,dz\,dy$

Part goal: Write the two orders whose innermost differential is $dx$, and decide whether the outer range needs a split.

## Reason

The inner limits come from step 5.1. The middle integral runs in $z$ at a fixed height, and the outer integral runs in $y$ over the full height.

## Computation

At a fixed height $y$ the variable $z$ runs from $-\frac{1}{2}\sqrt{4 - y}$ to $\frac{1}{2}\sqrt{4 - y}$. Hence

$$\iiint_E f\, dV = \int_{0}^{4} \int_{-\sqrt{4 - y}/2}^{\sqrt{4 - y}/2} \int_{-\sqrt{4 - y - 4z^{2}}}^{\sqrt{4 - y - 4z^{2}}} f(x, y, z)\, dx\, dz\, dy.$$

## Result

The fifth form. Its value for $f = 1$ is $4\pi$. For $f = z^{2}$ its value is $2\pi/3 = 2.094395102$.

## Verification

`code/part5_verify.py` compares this form with the exact values $4\pi$ and $2\pi/3$ from `code/exact_integrals.py`, and compares its limits with the defining inequality in both directions.
