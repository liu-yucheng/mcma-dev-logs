# Step 3.2 — Multiply the two factors

**Part:** 3 — Evaluate the integral
**Verification:** `code/part3_verify.py`

## Reason

The integrand of step 3.1 is a product of a function of $r$ and the constant $1$. The two integrals
therefore separate, and the answer is the product of two numbers.

## Computation

The angular integral is the length of the full turn:

$$\int_{0}^{2\pi} d\theta = 2\pi .$$

Multiply the two factors:

$$I = \frac{8}{3} \cdot 2\pi = \frac{16\pi}{3} .$$

A numerical value:

$$I = \frac{16\pi}{3} = 16.755160819145562\ldots \approx 16.7552 .$$

Check against the bracket of step 2.2: $0 < 16.7552 < 25.13$. The value is close to two thirds of
the upper bracket, and that is plausible, because the integrand falls from 8 at the centre to 0 at
the rim.

## Result

$$I = \frac{16\pi}{3} \approx 16.7552 .$$

The exact answer of the problem is $\dfrac{16\pi}{3}$.

## Check

`code/part3_verify.py`, step 3.2:

- angular integral: computed `6.283185307179586`, expected `6.283185307179586`;
- product of the two factors: computed `16.755160819145562`, expected `16.755160819145562`;
- `scipy.integrate.dblquad` of $8(1-r^4)r$ over $0 \le r \le 1$ and $0 \le \theta \le 2\pi$:
  computed `16.755160819145566`, difference `3.6e-15` against a tolerance of `1.0e-8`;
- the script prints the exact value as `answer 16 pi / 3 = 16.755160819145562`.
