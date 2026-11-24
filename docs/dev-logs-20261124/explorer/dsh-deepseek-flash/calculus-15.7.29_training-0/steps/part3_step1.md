# Part 3, Step 3.1: The order $dy\,dz\,dx$

Part goal: Write the two orders whose innermost differential is $dy$, and check each one against the exact value of a test integral.

## Reason

The chain gives the limits in $y$ at once, for each position in the projection. The remaining two integrals run over the projection $D$, and the outer one is the widest.

## Computation

At a fixed $(x, z)$ the chain reads $0 \leq y \leq 4 - x^{2} - 4z^{2}$. Then $(x, z)$ runs over $D$, where $x$ is the widest variable: $x$ from $-2$ to $2$, and at a fixed $x$ the variable $z$ runs from $-\frac{1}{2}\sqrt{4 - x^{2}}$ to $\frac{1}{2}\sqrt{4 - x^{2}}$. Hence

$$\iiint_E f\, dV = \int_{-2}^{2} \int_{-\sqrt{4 - x^{2}}/2}^{\sqrt{4 - x^{2}}/2} \int_{0}^{4 - x^{2} - 4z^{2}} f(x, y, z)\, dy\, dz\, dx.$$

The order is not the order $dz\,dy\,dx$: here the innermost integral is the one in $y$, and the outermost is the one in $x$.

## Result

The first form. For $f = 1$ its value is $4\pi = 12.566370614$.

## Verification

`code/part3_verify.py` compares the adaptive quadrature of this form with the exact value $4\pi$ from `code/exact_integrals.py`, and with the exact value $16\pi/3$ of the integral of $f = y$. It also compares the printed limits with the defining inequality in both directions.
