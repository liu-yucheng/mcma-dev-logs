# Part 1, Step 2: Write the volume as one integral over the two angles

## Reason

A star-shaped body is the natural home of spherical coordinates: the radial variable runs from the origin to the surface, and the two angles then cover the surface once. Integrating the radius first reduces the triple integral to a double integral over the rectangle of the angles, and that double integral is what a computer algebra system can attack exactly.

## Computation

The volume element in spherical coordinates is

$$
dV = \rho^{2}\sin\varphi\,d\rho\,d\varphi\,d\theta .
$$

The inner integral runs from the origin to the surface, so for a fixed pair of angles

$$
\int_{0}^{\rho(\theta,\varphi)} \rho^{2}\,d\rho = \frac{\rho(\theta,\varphi)^{3}}{3}.
$$

The volume is therefore

$$
V = \frac{1}{3}\int_{0}^{2\pi}\int_{0}^{\pi}
\rho(\theta,\varphi)^{3}\sin\varphi\,d\varphi\,d\theta .
$$

Three facts make the next steps legal. The limits of $\varphi$ are $0$ to $\pi$ because the polar angle of a point in space never leaves that interval. The limits of $\theta$ are $0$ to $2\pi$ because the surface closes in the azimuthal direction. The integrand carries the Jacobian factor $\sin\varphi$ and no other factor, because the statement gives no density and no length unit, so the integral returns a volume in cubic length units.

## Result

The volume of the body is

$$
V = \frac{1}{3}\int_{0}^{2\pi}\int_{0}^{\pi}
\left(1 + \frac{1}{5}\sin 6\theta\,\sin 5\varphi\right)^{3}\sin\varphi\,d\varphi\,d\theta .
$$

This is the integral that the rest of the page evaluates, and every later check compares with it.

## Common mistake

A reader may put the factor $\rho^{2}$ outside the radial integral and keep $\rho^{3}$ in the integrand of the two angles, but the radial integral already consumed one power, so the integrand of the double integral holds $\rho^{3}$ and not $\rho^{2}$. A reader may also drop $\sin\varphi$, but that factor belongs to the Jacobian and its absence changes the value of the integral.

## Verification

The script `code/part1_verify.py` builds the same integral for the unit ball, where $\rho = 1$ and the double integral must return $4\pi/3$. The row `unit ball volume: quadrature against 4 pi / 3` of `code/outputs/part1_summary.md` reports $4.18879020479$ against $4.18879020479$ with a difference of $8.882 \times 10^{-16}$, so the factor $\frac{1}{3}$ and the factor $\sin\varphi$ are both in the right place.
