# Part 3, Step 1: The volume in cylindrical coordinates

## Reason

The body is round about the vertical axis, so cylindrical coordinates match its shape: one
coordinate runs along the axis and one runs around it. In those coordinates the triple integral
collapses to a single integral of one variable, because the two other integrations have constant
limits.

## Computation

Write $x=r\cos\theta$, $y=r\sin\theta$, $z=z$. The Jacobian of this map is $r$, so
$dV=r\,dz\,dr\,d\theta$. The body is $0\le r\le 3$, $0\le z\le 10+\sqrt{9-r^{2}}$, and
$0\le\theta\le 2\pi$; the ceiling of Step 1.2 is the upper limit of $z$ for every pair
$(r,\theta)$.

Integrate over $z$ first. The ceiling depends on $r$ and not on $\theta$, so the inner integral
is the ceiling itself:

$$V=\int_{0}^{2\pi}\int_{0}^{3}\int_{0}^{10+\sqrt{9-r^{2}}}r\,dz\,dr\,d\theta
=2\pi\int_{0}^{3}r\bigl(10+\sqrt{9-r^{2}}\bigr)dr .$$

Split the radial integral into its two terms. The first term is
$10\int_{0}^{3}r\,dr=10\cdot\frac{9}{2}=45$. The second term is
$\int_{0}^{3}r\sqrt{9-r^{2}}\,dr=\Bigl[-\frac{1}{3}(9-r^{2})^{3/2}\Bigr]_{0}^{3}=9$. The sum is
$54$, and the volume is $2\pi\cdot 54$.

## Result

$$V=2\pi\cdot 54=108\pi=339.292006588 .$$

The integral $\int_{0}^{3}r(10+\sqrt{9-r^{2}})\,dr$ has the value $54$, and the angle
$0\le\theta\le 2\pi$ contributes the factor $2\pi$.

## Common mistake

A reader may drop the Jacobian factor $r$, but the limits give a different value without it; the
radial integral with the factor $r$ is $54$, and the check prints that number.

## Verification

Verification script: `code/part3_verify.py` check C1 compares a Simpson integral of $r(10+\sqrt{9-r^{2}})$ with the
closed value $45+9$ and prints $53.9999999653$ against $54$, a difference of
$3.466\times 10^{-8}$; the integrand has an infinite second derivative at $r=3$, so a small
difference is expected and the check allows $10^{-6}$. Check C2 multiplies the radial integral by
$2\pi$ and prints $339.292006588$ against $108\pi$. Check C7 samples 40 points of the lower
branch $z=10-\sqrt{9-r^{2}}$ and prints 40 of 40 inside the body, so no volume is missed below
the plane $z=10$.
