# Step 8 — Integrate over $r$

## Reason

The integrand is a sum of two powers of $r$. The power rule applies to each term separately: the antiderivative of $r^{n}$ is $r^{n+1}/(n+1)$ for $n \neq -1$.

## Computation

$$
\int_{0}^{1} \left(8r - 8r^{5}\right) dr
= \left[4r^{2} - \frac{8r^{6}}{6}\right]_{0}^{1}
= 4 - \frac{8}{6}.
$$

Reduce the fraction and subtract:

$$
4 - \frac{4}{3} = \frac{12 - 4}{3} = \frac{8}{3}.
$$

The same value comes from the separate terms:

$$
8 \cdot \frac{1}{2} - 8 \cdot \frac{1}{6} = 4 - \frac{4}{3} = \frac{8}{3}.
$$

## Result

$$
\int_{0}^{1} \left(8r - 8r^{5}\right) dr = \frac{8}{3} \approx 2.666666666667 .
$$

This number is the value of the integral of $x$ per radian of angle.

## Verification

`code/part3_verify.py` reports $2.666666666667$ from adaptive quadrature and the exact rational number $8/3$ from `Fraction` arithmetic. The two results agree.
