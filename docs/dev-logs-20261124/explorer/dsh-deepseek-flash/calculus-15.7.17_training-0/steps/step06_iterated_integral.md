# Step 6 — Assemble the two outer integrals

## Reason

The inner integral is done. The remaining work is the integral of its value over the disk. The value $8(1 - r^{4})$ depends on $r$ only, so the disk integral becomes two one-variable integrals after you insert the area element $r \, dr \, d\theta$.

## Computation

Insert the result of Step 5 into the iterated integral of Step 4:

$$
\iiint_{E} x \, dV
= \int_{0}^{2\pi} \int_{0}^{1} \underbrace{8\left(1 - r^{4}\right)}_{\text{inner integral}} \; r \; dr \, d\theta .
$$

Collect the factors that depend on $r$:

$$
8\left(1 - r^{4}\right) r = 8r - 8r^{5}.
$$

Thus

$$
\iiint_{E} x \, dV = \int_{0}^{2\pi} \int_{0}^{1} \left(8r - 8r^{5}\right) dr \, d\theta .
$$

The integrand has no $\theta$, and the limits of the two integrals are constants. The double integral is therefore the product of two single integrals.

## Result

$$
\iiint_{E} x \, dV
= \left(\int_{0}^{2\pi} d\theta\right)\left(\int_{0}^{1} \left(8r - 8r^{5}\right) dr\right).
$$

The problem is now two one-variable integrals. The first is the length of a full turn. The second is the area under the curve $8r - 8r^{5}$.

## Verification

`code/part2_verify.py` evaluates the inner integral from random points $(y, z)$ and compares it with the form in $r$. The largest difference over $20000$ points is $5.3\mathrm{e}{-15}$.
