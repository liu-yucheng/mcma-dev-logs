# Step 10 — Check the value in the order $dx\,dy\,dz$

## Reason

A limit error is the most common fault in a triple integral. A second order of integration uses different limits, so it finds such a fault. Here the natural second order takes $x$ as the outer variable: the slice of $E$ at a fixed $x$ is a disk.

## Computation

Fix $x$ with $0 \le x \le 4$. A point of the slice obeys $4\left(y^{2} + z^{2}\right) \le x$, that is

$$
y^{2} + z^{2} \le \frac{x}{4}.
$$

The slice is a disk of radius

$$
r(x) = \frac{\sqrt{x}}{2},
$$

and its area is

$$
A(x) = \pi r(x)^{2} = \frac{\pi x}{4}.
$$

On the slice, $x$ is constant, so the integral over the slice is $x \cdot A(x)$. Integrate over $x$:

$$
\iiint_{E} x \, dV = \int_{0}^{4} x \cdot \frac{\pi x}{4} \, dx
= \frac{\pi}{4}\int_{0}^{4} x^{2} \, dx
= \frac{\pi}{4} \cdot \frac{64}{3} = \frac{16\pi}{3}.
$$

At $x = 2$ the slice radius is $\sqrt{2}/2 \approx 0.7071$ and its area is $\pi/2 \approx 1.5708$.

## Result

$$
\iiint_{E} x \, dV = \int_{0}^{4} \frac{\pi x^{2}}{4} \, dx = \frac{16\pi}{3}.
$$

The two orders give the same value, so the limits of Step 4 are correct.

## Verification

`code/part4_verify.py` reports $16.755160819146$ for this order against the expected $16.755160819146$, with a difference of $0.000\mathrm{e}{+00}$. The counted slice area at $x = 2$ is $1.570488$ against $\pi/2 = 1.570796$, within four standard errors.
