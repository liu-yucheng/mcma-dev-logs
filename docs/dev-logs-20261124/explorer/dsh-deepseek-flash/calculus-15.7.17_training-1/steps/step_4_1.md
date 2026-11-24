# Step 4.1 — Integrate with x outermost

**Part:** 4 — Check the answer
**Verification:** `code/part4_verify.py`

## Reason

A second integration order uses a different set of limits and a different integrand. When two
independent orders give the same number, an error in the setup of one order is unlikely. Here the
variable $x$ goes outermost, so the inner integral runs over a section of the solid at a fixed $x$.

## Computation

Fix $x$ with $0 \le x \le 4$. On that plane the solid satisfies

$$4(y^2+z^2) \le x \iff y^2 + z^2 \le \frac{x}{4} .$$

Therefore the section is a disk of radius $\dfrac{\sqrt{x}}{2}$, and its area is

$$A(x) = \pi \left(\frac{\sqrt{x}}{2}\right)^2 = \frac{\pi x}{4} .$$

The integrand is constant on the section, so the inner integral is $x A(x)$. Then

$$I = \int_{0}^{4} x \cdot \frac{\pi x}{4} \, dx = \frac{\pi}{4} \int_{0}^{4} x^2 \, dx
= \frac{\pi}{4} \cdot \frac{64}{3} = \frac{16\pi}{3} .$$

The same sections give the volume:

$$\int_{0}^{4} A(x) \, dx = \frac{\pi}{4} \cdot \frac{16}{2} = 2\pi ,$$

which agrees with step 1.3.

## Result

$$I = \frac{16\pi}{3} \approx 16.7552 .$$

The second order gives the same answer as part 3.

## Check

`code/part4_verify.py`, step 4.1:

- volume from the section areas: computed `6.283185307179586`, expected `6.283185307179586`
  ($2\pi$);
- area of the section at $x = 4$: computed `3.141592653589793`, expected `3.141592653589793`
  ($\pi$);
- integral with $x$ outermost: computed `16.755160819145562`, expected `16.755160819145562`,
  difference `0.0`;
- closed form $\frac{\pi}{4}\cdot\frac{4^3}{3}$: computed `16.755160819145562`, difference `0.0`.
