# Step 7 — Integrate over $\theta$

## Reason

The integrand after Step 6 has no $\theta$. The integral of a constant over an interval is the constant times the length of the interval. A full turn has length $2\pi$.

## Computation

$$
\int_{0}^{2\pi} d\theta = \left[\theta\right]_{0}^{2\pi} = 2\pi .
$$

This factor is the total angle of the solid. It does not depend on $r$ or on $x$.

## Result

$$
\iiint_{E} x \, dV = 2\pi \int_{0}^{1} \left(8r - 8r^{5}\right) dr .
$$

The angle contributes the factor $2\pi \approx 6.283185307180$.

## Verification

`code/part3_verify.py` evaluates the angle integral with adaptive quadrature. It reports $6.283185307180$ against the expected $2\pi$, with a difference of $0.000\mathrm{e}{+00}$.
