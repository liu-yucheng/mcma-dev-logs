# Step 9 — Multiply the two factors

## Reason

The double integral of Step 6 is the product of a function of $\theta$ and a function of $r$ over a rectangle of limits. Such an integral equals the product of the two single integrals. Each single integral is known from Step 7 and Step 8, so the final value is one multiplication.

## Computation

$$
\iiint_{E} x \, dV
= \left(2\pi\right)\left(\frac{8}{3}\right)
= \frac{16\pi}{3}.
$$

A decimal check:

$$
\frac{16\pi}{3} = \frac{16 \cdot 3.141592653589793}{3} = 16.755160819146\ldots
$$

The value is positive, as it must be, because $x \ge 0$ on $E$ and the volume of $E$ is positive.

## Result

$$
\boxed{\;\iiint_{E} x \, dV = \frac{16\pi}{3} \approx 16.7552\;}
$$

## Verification

`code/part3_verify.py` reports four results for this value. The product of the one-dimensional integrals is $16.755160819146$. The nested adaptive quadrature is $16.755160819146$. The point sample of four million points is $16.772078$ with a standard error of $0.009369$, which is within four standard errors. The expected value is $16.755160819146$.
