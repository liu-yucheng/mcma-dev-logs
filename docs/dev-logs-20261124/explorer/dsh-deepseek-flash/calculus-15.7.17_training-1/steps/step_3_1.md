# Step 3.1 — Use polar coordinates in the disk

**Part:** 3 — Evaluate the integral
**Verification:** `code/part3_verify.py`

## Reason

The integrand depends on $y$ and $z$ only through $y^2 + z^2$, and the region is a disk. Polar
coordinates match both facts at the same time. They turn the two-dimensional integral into a
product of one integral in $r$ and one integral in $\theta$.

## Computation

Put

$$y = r\cos\theta, \qquad z = r\sin\theta, \qquad dA = r \, dr \, d\theta .$$

The disk $D$ becomes $0 \le r \le 1$ and $0 \le \theta \le 2\pi$. The integrand becomes
$8(1 - r^4)$, and the area element adds the factor $r$. Therefore

$$I = \int_{0}^{2\pi} \int_{0}^{1} 8\left(1 - r^4\right) r \, dr \, d\theta .$$

The inner integral is

$$\int_{0}^{1} 8\left(r - r^5\right) dr
= 8\left[ \frac{r^2}{2} - \frac{r^6}{6} \right]_{0}^{1}
= 8\left(\frac{1}{2} - \frac{1}{6}\right) = 8 \cdot \frac{1}{3} = \frac{8}{3} .$$

The factor $r$ is necessary. Without it the inner integral would be $\int_0^1 8(1-r^4)dr = 6.4$,
which is the value for a square region, not for a disk.

## Result

$$I = \frac{8}{3} \int_{0}^{2\pi} d\theta .$$

The radial part of the integral is $\frac{8}{3} \approx 2.6667$.

## Check

`code/part3_verify.py`, step 3.1:

- radial integral from `scipy.integrate.quad`: computed `2.6666666666666665`, expected
  `2.6666666666666665` ($8/3$), difference `0.0`;
- the same value against the fraction $8/3$: difference `0.0`, tolerance `1.0e-9`.
