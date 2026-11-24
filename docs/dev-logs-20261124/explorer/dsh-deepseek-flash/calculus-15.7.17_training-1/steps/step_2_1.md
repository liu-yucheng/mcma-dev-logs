# Step 2.1 — Integrate along x first

**Part:** 2 — Reduce the triple integral
**Verification:** `code/part2_verify.py`

## Reason

Choose the inner variable first. The variable $x$ has an explicit lower limit $4(y^2+z^2)$ and an
explicit upper limit $4$. Therefore fix $y$ and $z$, and integrate $x$ along one straight segment.
This choice turns the triple integral into a double integral with no square roots.

## Computation

Fix a point $(y,z)$ in the disk $D$ and write $r^2 = y^2 + z^2$. The variable $x$ runs from $4r^2$ to
$4$ on that segment. The integrand is $x$.

$$\int_{4r^2}^{4} x \, dx = \left[ \frac{x^2}{2} \right]_{4r^2}^{4}
= \frac{16}{2} - \frac{(4r^2)^2}{2} = 8 - 8r^4 .$$

The result is

$$\int_{4r^2}^{4} x \, dx = 8\left(1 - r^4\right) = 8\left(1 - (y^2+z^2)^2\right).$$

Check the two ends of the disk. At the centre $r = 0$ the segment is the full height, and the value
is $8$. At the rim $r = 1$ the segment has zero length, and the value is $0$. The result decreases
as $r$ grows, and it is never negative, because $r \le 1$ on $D$.

## Result

For a fixed point $(y,z)$ in $D$, the integral along the segment is
$8\left(1 - (y^2+z^2)^2\right)$.

## Check

`code/part2_verify.py`, step 2.1, compares `scipy.integrate.quad` of $x$ on the segment with
$8(1-r^4)$ at five radii. The tolerance is `1.0e-9`, and every difference is `0.0`:

| $r$ | segment | computed | expected |
| --- | --- | --- | --- |
| 0.00 | $[0, 4]$ | 8.0 | 8.0 |
| 0.25 | $[0.25, 4]$ | 7.96875 | 7.96875 |
| 0.50 | $[1, 4]$ | 7.5 | 7.5 |
| 0.75 | $[2.25, 4]$ | 5.46875 | 5.46875 |
| 1.00 | $[4, 4]$ | 0.0 | 0.0 |
