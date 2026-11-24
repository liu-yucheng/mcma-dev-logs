# Part 2, Step 3: The volume by slicing

## Reason

A solid of known section area has volume equal to the integral of that area, because the sum of
the slab volumes tends to the integral as the thickness tends to zero. The two branches of the
area give two integrals, and each integral is a polynomial, so both are exact.

## Computation

Integrate the first branch over its own range, from $z=0$ to $z=10$:

$$\int_{0}^{10}9\pi\,dz=9\pi\cdot 10=90\pi .$$

Integrate the second branch over its own range, from $z=10$ to $z=13$. The substitution
$u=z-10$ carries the interval to $0\le u\le 3$ and the differential to $du=dz$:

$$\int_{10}^{13}\pi\bigl(9-(z-10)^{2}\bigr)dz=\pi\int_{0}^{3}(9-u^{2})\,du
=\pi\Bigl[9u-\frac{u^{3}}{3}\Bigr]_{0}^{3}=\pi(27-9)=18\pi .$$

Add the two parts. The ranges $0\le z\le 10$ and $10\le z\le 13$ share only the single plane
$z=10$, and a plane has zero volume, so the sum is the whole volume:

$$V=90\pi+18\pi=108\pi .$$

## Result

$$V=108\pi=339.292006588 .$$

The cap contributes $18\pi=56.5486677646$ and the cylinder contributes
$90\pi=282.743338823$.

## Common mistake

A reader may carry the second integrand from $z=0$ to $z=13$, but each branch keeps its own
range; the second branch over $10\le z\le 13$ gives $18\pi$, and the check prints that value.

## Verification

Verification script: `code/part2_verify.py` check C4 compares a Simpson integral of the section area over the
cylinder with $\pi R^{2}H$ and prints $282.743338822$ against $282.743338823$. Check C5
compares the same integral over the cap with $\frac{2}{3}\pi R^{3}$ and prints $56.5486677646$
against $56.5486677646$. Check C6 prints the whole volume as $339.292006587$ against
$339.292006588$. Check C7 estimates the same volume by random sampling and prints $339.265602$
with a standard error of $0.147775$, against the exact value; the difference $2.640\times 10^{-2}$
is far inside three standard errors. Check C8 adds the two exact solids and prints
$339.292006588$. The three methods share no integrand: one integrates the section area, one
multiplies closed forms, and one samples the body.
