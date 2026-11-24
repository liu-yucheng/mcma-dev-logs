# Part 5, Step 1: Compute the mass of the cone

## Reason

The answer of Part 3 holds the density $k$ and the height $h$. A textbook answer often states the
moment of inertia in terms of the mass $M$, so this part computes the mass first. The density is
constant, so the mass is the density multiplied by the volume of the body.

## Computation

The volume of a cone with base radius $R$ and height $H$ is $\pi R^{2}H/3$. Here the base radius is
$h$ and the height is $h$, so the volume is

$$V = \frac{\pi h^{2} \cdot h}{3} = \frac{\pi h^{3}}{3},
\qquad M = k\,V = \frac{\pi k h^{3}}{3} .$$

The same value comes from the integral form $M = \iiint_{E} k\,dV$ with the limits of Part 2:

$$M = \int_{0}^{2\pi}\int_{0}^{h}\int_{r}^{h} k\,r\,dz\,dr\,d\theta
= 2\pi k \int_{0}^{h} r\,(h - r)\,dr = 2\pi k \cdot \frac{h^{3}}{6} = \frac{\pi k h^{3}}{3} .$$

## Result

$$M = \frac{\pi k h^{3}}{3} .$$

Verification: `code/part5_verify.py` computes the mass at $k = 1$, $h = 1$ by three methods. The
symbolic triple integral gives $\pi h^{3}k/3$, the stack of the slice masses gives 1.047197551, and
the formula $\pi k h^{3}/3$ gives 1.047197551. Monte Carlo sampling of the volume gives 1.045362 plus
or minus 0.001243, which is 1.477 standard errors from 1.047198.
