# Part 4, Step 4.3: The order $dz\,dx\,dy$

Part goal: Write the two orders whose innermost differential is $dz$, and decide whether the outer range needs a split.

## Reason

The inner integral still runs in $z$. The outer variable is now $y$, because $y$ runs over the full height of the solid and $x$ is narrower at each height.

## Computation

The height runs from $0$ to $4$. At a fixed height the variable $x$ runs from $-\sqrt{4 - y}$ to $\sqrt{4 - y}$. Hence

$$\iiint_E f\, dV = \int_{0}^{4} \int_{-\sqrt{4 - y}}^{\sqrt{4 - y}} \int_{-\sqrt{4 - y - x^{2}}/2}^{\sqrt{4 - y - x^{2}}/2} f(x, y, z)\, dz\, dx\, dy.$$

## Result

The fourth form. Its value for $f = 1$ is $4\pi$, the same as the third form.

## Verification

`code/part4_verify.py` compares this form with the exact values $4\pi$ and $8\pi/3$, and compares its limits with the defining inequality in both directions.
