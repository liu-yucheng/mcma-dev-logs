# Step 5 — Integrate $x$ from $4r^{2}$ to $4$

## Reason

In the inner integral the variables $r$ and $\theta$ are constant. Only $x$ changes. The integrand is $x$, so the antiderivative is $x^{2}/2$ and the fundamental theorem of calculus gives the value at the two bounds.

## Computation

$$
\int_{4r^{2}}^{4} x \, dx
= \left[\frac{x^{2}}{2}\right]_{4r^{2}}^{4}
= \frac{16}{2} - \frac{\left(4r^{2}\right)^{2}}{2}.
$$

Simplify each term:

$$
\frac{16}{2} = 8, \qquad \frac{16r^{4}}{2} = 8r^{4}.
$$

Therefore

$$
\int_{4r^{2}}^{4} x \, dx = 8 - 8r^{4} = 8\left(1 - r^{4}\right).
$$

Two values act as checks. At $r = 0$ the segment is $0 \le x \le 4$ and the integral is $8$. At $r = 0.5$ the segment is $1 \le x \le 4$ and the integral is $8 - 0.5 = 7.5$. At $r = 1$ the segment has zero length and the integral is $0$.

## Result

$$
\int_{4r^{2}}^{4} x \, dx = 8\left(1 - r^{4}\right).
$$

The inner integral is largest at the axis and it decreases to zero at the rim of the cap.

## Verification

`code/part2_verify.py` compares the closed form with adaptive quadrature at $r = 0,\; 0.25,\; 0.5,\; 0.75,\; 1$. All five differences are $0.000\mathrm{e}{+00}$. The same script confirms the value $15/2$ at $r = 1/2$ with exact rational arithmetic.
