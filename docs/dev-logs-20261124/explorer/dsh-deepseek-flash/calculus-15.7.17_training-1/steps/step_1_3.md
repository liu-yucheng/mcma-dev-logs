# Step 1.3 — Write the solid as one set and note its symmetry

**Part:** 1 — Describe the solid
**Verification:** `code/part1_verify.py`

## Reason

A triple integral needs explicit limits. The two surfaces give one lower limit and one upper limit
for $x$, and the projection gives the limits for $y$ and $z$. Record the symmetry first, because a
symmetry can save work, and a false symmetry gives a wrong answer.

## Computation

Join the two limits from step 1.2:

$$E = \{(x,y,z) : y^2 + z^2 \le 1,\ 4(y^2+z^2) \le x \le 4\}.$$

Every coordinate in $E$ is finite, because $0 \le x \le 4$ and $y^2 + z^2 \le 1$. The set is closed,
because all its inequalities are non-strict. Therefore the solid is closed and bounded, and the
integral is finite.

Now test the symmetry. The inequality $y^2 + z^2 \le 1$ and the equality $x = 4(y^2+z^2)$ both
contain $y$ and $z$ only as squares. Therefore the change $y \to -y$ keeps the solid in place, and
the same holds for $z \to -z$. The solid is symmetric about the planes $y = 0$ and $z = 0$.

The integrand is $f(x,y,z) = x$. This function does not contain $y$ or $z$. Therefore the symmetry in
$y$ does not pair a positive value with a negative value: the two halves give equal contributions,
and they add. The symmetry gives no cancellation for this integrand.

For reference, the volume of the solid is

$$V = \iint_D \bigl(4 - 4(y^2+z^2)\bigr) \, dA .$$

The integrand $4 - 4r^2$ runs from 4 at the centre to 0 at the rim, so the volume is half of the
cylinder with radius 1 and height 4:

$$V = \tfrac{1}{2}\,\pi \cdot 1^2 \cdot 4 = 2\pi .$$

## Result

The solid is $E = \{(x,y,z) : y^2+z^2 \le 1,\ 4(y^2+z^2) \le x \le 4\}$. It is closed and bounded,
and it is symmetric about $y = 0$ and $z = 0$. Its volume is $2\pi \approx 6.2832$. The symmetry does
not simplify the integrand $x$.

## Check

`code/part1_verify.py`, fact 3, and `code/part2_verify.py`, step 2.2:

- points where two descriptions of $E$ differ: computed `0`, expected `0`;
- volume of $E$: computed `6.283185307179586`, expected `6.283185307179586` ($2\pi$);
- volume against half of the enclosing cylinder: same value, difference `0.0`.
