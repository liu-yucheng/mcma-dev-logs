# Step 2.2 — Write the double integral over the disk

**Part:** 2 — Reduce the triple integral
**Verification:** `code/part2_verify.py`

## Reason

The inner integral no longer contains $x$. The outer integral therefore runs over the projection of
the solid, which is the unit disk $D$. Write the reduced integral in full, and check its order of
magnitude before you evaluate it.

## Computation

Insert the result of step 2.1 into the double integral over $D$:

$$I = \iint_D 8\left(1 - (y^2+z^2)^2\right) dA
= 8 \iint_D \left(1 - (y^2+z^2)^2\right) dA .$$

The integrand is positive on the open disk and zero on the rim. Therefore $I > 0$.

Bound the answer before the exact evaluation. On $D$ the factor $1 - r^4$ runs from $1$ to $0$, so

$$0 < I < 8 \cdot 1 \cdot \operatorname{area}(D) = 8\pi \approx 25.13 .$$

The answer must also be larger than the value at the centre multiplied by a fraction of the area,
because the function falls to zero at the rim.

## Result

$$I = 8 \iint_D \left(1 - (y^2+z^2)^2\right) dA .$$

The value lies between $0$ and $8\pi \approx 25.13$.

## Check

`code/part2_verify.py`, step 2.2:

- double integral of $8(1-r^4)$ over $D$ in polar form: computed `16.755160819145566`, expected
  `16.755160819145562` (the value of part 3), difference `3.6e-15` against a tolerance of `1.0e-8`.
  This check closes the loop between part 2 and part 3;
- volume of $E$: computed `6.283185307179586`, expected `6.283185307179586`;
- radial factor of the volume: computed `1.0`, expected `1.0`.

The value `16.755` is inside the bracket $0 < I < 8\pi = 25.13$ from this step.
