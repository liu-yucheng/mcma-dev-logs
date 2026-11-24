# Step 2.2 Use polar coordinates in the horizontal plane

## Reason

The disk $D$ has a circular rim, and the integrand $8-2x^{2}-2z^{2}$ contains only the squared radius.
Polar coordinates remove the square root from the rim and turn the integrand into a polynomial.
The area element of polar coordinates needs the Jacobian factor $r$.

## Computation

Set

$$
x=r\cos\theta, \qquad z=r\sin\theta, \qquad x^{2}+z^{2}=r^{2},
$$

with $0\le r\le 2$ and $0\le \theta\le 2\pi$.
The area element is

$$
dA = r\,dr\,d\theta .
$$

The thickness becomes $8-2r^{2}$. The volume is

$$
V=\int_{0}^{2\pi}\int_{0}^{2}\int_{r^{2}}^{\,8-r^{2}} r\,dy\,dr\,d\theta
=\int_{0}^{2\pi}\int_{0}^{2} r\left(8-2r^{2}\right) dr\,d\theta .
$$

## Result

The integral now has constant limits on the two outer integrations.
The factor $r$ is the weight of one polar ring of radius $r$ and width $dr$.
The whole volume is the product of the angle integral and the radius integral, because no limit and no
integrand depends on the angle.

## Check

`code/part2_verify.py` computes the volume three times: in Cartesian order $dy\,dz\,dx$, in the reversed
horizontal order $dy\,dx\,dz$, and in polar order $r\,dy\,dr\,d\theta$.
It prints `volume from the Cartesian double integral: computed = 50.265482456768, expected = 50.265482457437`
and `volume from the polar double integral: computed = 50.265482457437, expected = 50.265482457437`.
The script also checks the Jacobian alone: the polar integral of $r$ gives $12.566370614359$, which is
the area $4\pi$ of the disk.
