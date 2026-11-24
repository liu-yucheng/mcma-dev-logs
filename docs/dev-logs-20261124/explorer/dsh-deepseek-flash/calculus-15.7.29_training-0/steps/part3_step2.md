# Part 3, Step 3.2: The order $dy\,dx\,dz$

Part goal: Write the two orders whose innermost differential is $dy$, and check each one against the exact value of a test integral.

## Reason

The inner integral still runs in $y$, so its limits do not change. Only the two outer integrals change place, and the wider of the two variables must be the outer one.

## Computation

The projection is $x^{2} + 4z^{2} \leq 4$. Sweep $z$ first: $z$ lies between $-1$ and $1$, and at a fixed $z$ the variable $x$ runs between $-2\sqrt{1 - z^{2}}$ and $2\sqrt{1 - z^{2}}$. Hence

$$\iiint_E f\, dV = \int_{-1}^{1} \int_{-2\sqrt{1 - z^{2}}}^{2\sqrt{1 - z^{2}}} \int_{0}^{4 - x^{2} - 4z^{2}} f(x, y, z)\, dy\, dx\, dz.$$

## Result

The second form. Its value for $f = 1$ is $4\pi$, the same as the first form.

## Verification

`code/part3_verify.py` compares this form with the exact values $4\pi$ and $16\pi/3$, and compares its limits with the defining inequality in both directions.
