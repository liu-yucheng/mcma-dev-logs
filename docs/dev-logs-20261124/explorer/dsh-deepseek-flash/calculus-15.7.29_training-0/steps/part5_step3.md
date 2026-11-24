# Part 5, Step 5.3: The order $dx\,dy\,dz$

Part goal: Write the two orders whose innermost differential is $dx$, and decide whether the outer range needs a split.

## Reason

The inner integral still runs in $x$. The outer variable is now $z$, because $z$ runs over the full width of the base and $y$ is narrower at each $z$.

## Computation

The variable $z$ runs from $-1$ to $1$. At a fixed $z$ the height $y$ runs from $0$ to $4 - 4z^{2}$. Hence

$$\iiint_E f\, dV = \int_{-1}^{1} \int_{0}^{4 - 4z^{2}} \int_{-\sqrt{4 - 4z^{2} - y}}^{\sqrt{4 - 4z^{2} - y}} f(x, y, z)\, dx\, dy\, dz.$$

## Result

The sixth form. Its value for $f = 1$ is $4\pi$, the same as the fifth form.

## Verification

`code/part5_verify.py` compares this form with the exact values $4\pi$ and $2\pi/3$, and compares its limits with the defining inequality in both directions.
