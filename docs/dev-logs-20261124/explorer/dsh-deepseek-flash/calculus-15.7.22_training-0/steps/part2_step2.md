# Step 2.2: Integrate the inner variable

## Reason

The inner integral has the constant integrand $1$, so its value is the length of the interval of $y$,
and that length is already known from Part 1.

## Computation

$$\int_{-1}^{4-z}dy=(4-z)-(-1)=5-z.$$

Thus the triple integral becomes a double integral over the disk:

$$V=\int_{-2}^{2}\int_{-\sqrt{4-x^2}}^{\sqrt{4-x^2}}(5-z)\,dz\,dx=\iint_{D}(5-z)\,dA,\qquad
D=\{(x,z):x^2+z^2\le 4\}.$$

## Check

The integrand $5-z$ is exactly the thickness $h$ of Step 1.3. The integration in $y$ removed the two
planes and left one function over the disk. The integrand is positive on the disk, because
$5-z\ge 3$, so the double integral is positive and no sign error can hide in it.

## Result

$$V=\iint_{D}(5-z)\,dA.$$

## Verification

`code/part2_verify.py` computes the double integral of $5-z$ over the disk with adaptive quadrature.
The value is $62.831853071796$, and $20\pi$ is $62.831853071796$; the accepted difference is $10^{-8}$.
The script also computes the same double integral by a second route in Step 2.3, and the two values
agree to $10^{-8}$.
