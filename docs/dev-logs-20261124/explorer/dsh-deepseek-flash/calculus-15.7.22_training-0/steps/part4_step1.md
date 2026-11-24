# Step 4.1: Evaluate the double integral in polar coordinates

## Reason

The disk is a circle about the origin of the plane of $x$ and $z$, so polar coordinates give constant
limits in the angle and simple limits in the radius.

## Computation

Put $x=r\cos\theta$ and $z=r\sin\theta$. The disk becomes $0\le r\le 2$ and $0\le\theta\le 2\pi$, and
the area element is $dA=r\,dr\,d\theta$. Thus

$$V=\int_{0}^{2\pi}\int_{0}^{2}(5-r\sin\theta)\,r\,dr\,d\theta.$$

The inner integral is

$$\int_{0}^{2}(5r-r^2\sin\theta)\,dr=\Big[\frac{5r^2}{2}-\frac{r^3}{3}\sin\theta\Big]_{0}^{2}
=10-\frac{8}{3}\sin\theta,$$

and

$$V=\int_{0}^{2\pi}\left(10-\frac{8}{3}\sin\theta\right)d\theta
=10\cdot 2\pi-\frac{8}{3}\cdot 0=20\pi.$$

## Check

The constant term $10$ is $5$ times the radius $2$, and its integral over the angle gives the volume
of a cylinder of radius $2$ and height $5$, which is $5\cdot 4\pi=20\pi$. The term with $\sin\theta$
integrates to $0$ over one full period, because the tilt adds the same volume on the side $z<0$ that it
removes on the side $z>0$.

## Result

$$V=20\pi.$$

## Verification

`code/part4_verify.py` evaluates the polar integral by nested adaptive quadrature and prints
$62.831853071796$. The closed form $20\pi$ prints $62.831853071796$, and the difference is $0$. The
accepted difference is $10^{-9}$.
