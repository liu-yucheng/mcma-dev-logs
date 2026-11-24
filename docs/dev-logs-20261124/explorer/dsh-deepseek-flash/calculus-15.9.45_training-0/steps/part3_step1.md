# Part 3, Step 1: Evaluate the azimuthal integral

## Reason

The azimuthal integral counts how much of the turn carries a bump. A sine squared over a whole number of periods has the average value one half, and the integral is that average times the length of the interval. The result must be exactly $\pi$, with no residue, because the integrand is a square and the interval is a whole number of periods.

## Computation

Use the identity $\sin^{2}u = \frac{1 - \cos 2u}{2}$ with $u = 6\theta$:

$$
A = \int_{0}^{2\pi}\sin^{2}6\theta\,d\theta
= \int_{0}^{2\pi}\frac{1 - \cos 12\theta}{2}\,d\theta
= \frac{1}{2}\cdot 2\pi - \frac{1}{2}\int_{0}^{2\pi}\cos 12\theta\,d\theta .
$$

The cosine completes six full periods over the interval $0 \le \theta \le 2\pi$, so its integral is zero:

$$
\int_{0}^{2\pi}\cos 12\theta\,d\theta
= \left[\frac{\sin 12\theta}{12}\right]_{0}^{2\pi} = 0 .
$$

Therefore

$$
A = \pi .
$$

## Result

The azimuthal integral is $A = \pi = 3.14159265359$. The value does not depend on the harmonic $6$ as long as the harmonic is a positive whole number, because every harmonic completes a whole number of periods over the full turn. That independence is why the printed check over the harmonics $1$ to $7$ departs from $\pi$ by at most $6.661 \times 10^{-16}$.

## Common mistake

A reader may take $A = 2\pi$ because the integrand is a square and the interval is long, but the square has the average one half and not one, so the integral is $\pi$ and not $2\pi$. A reader may also keep the cosine term, but its integral over a whole number of periods is zero, so the cosine leaves no residue.

## Verification

The script `code/part3_verify.py` compares the exact value $\pi$ with an adaptive quadrature of the same integrand, and it repeats the comparison for the harmonics $1$ to $7$. The row `azimuthal integral: pi times the exact factor against quadrature` of `code/outputs/part3_summary.md` reports $3.14159265359$ against $3.14159265359$ with a difference of $2.220 \times 10^{-15}$, and the row `azimuthal factor over harmonics 1 to 7: largest departure from 1` reports $6.661 \times 10^{-16}$ against $0$.
