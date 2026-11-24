# Step 2.1 Choose the order of the three integrations

## Reason

A triple integral adds the volume of small boxes $dx\,dy\,dz$ over the solid.
The order of the integrations must follow the shape of the solid.
For a fixed horizontal point, the solid starts on the lower surface and ends on the upper surface.
So the inner integration runs in the vertical direction first.

## Computation

The statement gives the two surfaces as functions of $x$ and $z$:

$$
y_{\text{lower}}=x^{2}+z^{2}, \qquad y_{\text{upper}}=8-x^{2}-z^{2}.
$$

For a fixed point $(x,z)$ of the disk $D$, the height $y$ runs from $y_{\text{lower}}$ to $y_{\text{upper}}$.
The order of the differentials is therefore $dy\,dA$, where $dA$ is the area element of the disk.
The volume is

$$
V=\iint_{D}\left[\int_{x^{2}+z^{2}}^{\,8-x^{2}-z^{2}} dy\right] dA
=\iint_{D}\left(8-2x^{2}-2z^{2}\right) dA .
$$

## Result

The inner integral removes the variable $y$ and leaves the thickness $8-2x^{2}-2z^{2}$ as the integrand
of a double integral over the disk $D$.
One triple integral over the solid becomes one double integral over the projection.

## Check

`code/part2_verify.py` integrates the constant $1$ over the segment $\left[r^{2},\,8-r^{2}\right]$ for five radii.
It prints `inner integral over y at radius 0.5: computed = 7.500000000000, expected = 7.500000000000`,
which is the thickness $8-2(0.25)$.
The largest gap over the five radii is $4.4\times10^{-16}$, and the script asserts that this gap is below $10^{-8}$.
