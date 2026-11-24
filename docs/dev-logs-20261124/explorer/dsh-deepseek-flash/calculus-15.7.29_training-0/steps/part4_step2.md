# Part 4, Step 4.2: The order $dz\,dy\,dx$

Part goal: Write the two orders whose innermost differential is $dz$, and decide whether the outer range needs a split.

## Reason

The inner limits come from step 4.1. The middle integral runs in $y$ at a fixed $x$, and the outer integral runs in $x$ over the widest range.

## Computation

For a fixed $x$ the variable $y$ runs from $0$ to $4 - x^{2}$. Hence

$$\iiint_E f\, dV = \int_{-2}^{2} \int_{0}^{4 - x^{2}} \int_{-\sqrt{4 - x^{2} - y}/2}^{\sqrt{4 - x^{2} - y}/2} f(x, y, z)\, dz\, dy\, dx.$$

## Result

The third form. Its value for $f = 1$ is $4\pi$. For $f = x^{2}$ its value is $8\pi/3 = 8.377580410$.

## Verification

`code/part4_verify.py` compares this form with the exact values $4\pi$ and $8\pi/3$ from `code/exact_integrals.py`, and compares its limits with the defining inequality in both directions.
