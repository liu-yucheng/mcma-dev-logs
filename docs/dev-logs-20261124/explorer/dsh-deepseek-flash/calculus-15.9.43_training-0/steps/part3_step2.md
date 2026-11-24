# Part 3, Step 2: The cap in spherical coordinates, and the wrong single ball

## Reason

The cap is half of a sphere, and a sphere is the shape that spherical coordinates describe with
constant limits. The silo as a whole is not a sphere, so the coordinates must be centered on the
cap and must cover the cap only. A reader who centers one ball on the origin and uses the
largest distance of the body as its radius obtains a ball that is far larger than the silo, and
this step measures how far.

## Computation

Center spherical coordinates on the cap center $(0,0,10)$: a point is
$(x,y,z)=(0,0,10)+(\rho\sin\varphi\cos\theta,\rho\sin\varphi\sin\theta,\rho\cos\varphi)$.
The Jacobian is $\rho^{2}\sin\varphi$, so $dV=\rho^{2}\sin\varphi\,d\rho\,d\varphi\,d\theta$.
The cap is the half ball $0\le\rho\le 3$, $0\le\varphi\le\frac{\pi}{2}$,
$0\le\theta\le 2\pi$.

Integrate each factor over its own limit:

$$\int_{0}^{3}\rho^{2}d\rho=9,\qquad
\int_{0}^{\pi/2}\sin\varphi\,d\varphi=1,\qquad
\int_{0}^{2\pi}d\theta=2\pi .$$

The three factors multiply, because each limit is constant:

$$V_{\text{cap}}=9\cdot 1\cdot 2\pi=18\pi .$$

## Result

$$V_{\text{cap}}=18\pi=56.5486677646,\qquad V=90\pi+18\pi=108\pi .$$

The factors are $9$ for $\rho$, $1$ for $\varphi$, and $2\pi$ for $\theta$. A single ball of
radius $13$ about the origin has the volume $4601.38603996$, which is $13.561728$ times the
volume of the silo; the silo is not that ball.

## Common mistake

A reader may replace the silo by one ball of radius $13$ about the origin, but the ball is not
the body: check C4 of `code/part3_verify.py` prints $4601.38603996$ for the ball against
$339.292006588$ for the silo, and the two values differ by more than a factor of thirteen.

## Verification

Verification script: `code/part3_verify.py` check C3 computes the three Jacobian factors as separate numerical
integrals, prints them as $6.283185307$, $1.000000000$, and $9.000000000$, and prints their
product $56.5486677646$ against $18\pi$. Check C5 estimates the cap volume by random sampling
and prints $56.578392$ against $56.5486677646$ with a standard error of $0.053938$, so three
standard errors cover the difference. Check C6 maps 3000 points of the cap through the
parametrization above and prints 0 points outside the body. Check C4 prints the volume of the
single ball of radius $13$ as $4601.38603996$ against $339.292006588$.
