# Step 4.2 - Check the volume with slices at a fixed $y$

Part 4: the volume and its checks.

## Reason

A result that comes from one order of integration can be wrong in the same way twice. A second order cuts the solid the other way, so it exercises a different derivation. If the two orders agree, an arithmetic error in one of them is unlikely.

## Computation

Fix $y$ with $0 \leq y \leq 1$. The chain of Step 1.1 gives

$$-1 \leq x \leq 1 \quad\text{with}\quad x^{2} \leq y, \qquad 0 \leq z \leq 1 - y.$$

The condition $x^{2} \leq y$ bounds $x$ by $\pm\sqrt{y}$, so the slice is a rectangle: its width in $x$ is $2\sqrt{y}$ and its height in $z$ is $1 - y$. Its area is

$$B\left(y\right) = 2\sqrt{y}\,\left(1 - y\right).$$

Integrate that area over $y$:

$$V = \int_{0}^{1} 2\sqrt{y}\,\left(1 - y\right) dy = 2\left[\frac{2y^{3/2}}{3} - \frac{2y^{5/2}}{5}\right]_{0}^{1} = 2\left(\frac{2}{3} - \frac{2}{5}\right) = \frac{8}{15}.$$

## Result

The slices at a fixed $y$ give the same volume $8 / 15$. The slice area is largest where the product $\sqrt{y}\left(1 - y\right)$ is largest, at $y = 1 / 3$, and it vanishes at $y = 0$ and at $y = 1$.

## Check

`code/part4_verify.py` measures the slice area at $y = 0.25$, $y = 0.5$, and $y = 0.75$ by sampling the box $-1 \leq x \leq 1$, $0 \leq z \leq 1$. It prints `0.75027` against `0.75`, `0.7072` against `0.707106781186548`, and `0.432431` against `0.433012701892219`. Each difference is below its standard error times four. The script integrates the slice area with adaptive quadrature and with exact rational arithmetic, and both give `0.533333333333333`.
