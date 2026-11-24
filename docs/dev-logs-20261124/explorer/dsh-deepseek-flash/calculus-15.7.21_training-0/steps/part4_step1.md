# Step 4.1 - Integrate the slice area over $x$

Part 4: the volume and its checks.

## Reason

The slice area is a function of one variable, and the solid is the union of its slices. Therefore the volume is the integral of the slice area over the range of $x$. The integrand is a polynomial, so the integral is exact and needs no numerical method.

## Computation

From Step 3.2, $A\left(x\right) = \frac{1}{2}\left(1 - 2x^{2} + x^{4}\right)$. Integrate term by term on the symmetric interval:

$$V = \int_{-1}^{1} \frac{1}{2}\left(1 - 2x^{2} + x^{4}\right) dx = \frac{1}{2}\left[x - \frac{2x^{3}}{3} + \frac{x^{5}}{5}\right]_{-1}^{1}.$$

The integrand is even, so the integral over the symmetric interval is twice the integral over $\left[0, 1\right]$:

$$V = 1 - \frac{2}{3} + \frac{1}{5} = \frac{15 - 10 + 3}{15} = \frac{8}{15}.$$

The same number comes from the double integral of Step 2.2, because the inner integral is the slice area:

$$\int_{x^{2}}^{1} \left(1 - y\right) dy = \frac{1}{2} - x^{2} + \frac{x^{4}}{2} = A\left(x\right).$$

## Result

$$V = \frac{8}{15} = 0.533333\ldots$$

## Check

`code/part4_verify.py` computes the antiderivative with exact rational arithmetic and prints `0.533333333333333`. It also integrates the slice area with adaptive quadrature and prints `0.533333333333333`. The difference is `0` and the tolerance is `0`. The script integrates the double integral of Step 2.2 as well and prints the same value with a difference of `1.110e-16`.
