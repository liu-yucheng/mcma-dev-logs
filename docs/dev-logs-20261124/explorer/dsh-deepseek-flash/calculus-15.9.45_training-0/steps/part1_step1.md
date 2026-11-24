# Part 1, Step 1: Read the surface and find the bounds of its radius

## Reason

The statement gives a radius as a function of two angles, so the first job is to learn where that radius can go. The bounds of the radius decide whether the body is a sphere with bumps on the outside only, or a body that also sinks inside the unit sphere. The bounds also give the size of the box that a drawing needs, and they show that every ray from the origin meets the surface exactly once, which the volume integral of Step 1.2 requires.

## Computation

The surface is a graph in spherical coordinates:

$$
\rho(\theta,\varphi) = 1 + \frac{1}{5}\sin 6\theta\,\sin 5\varphi,
\qquad 0 \le \theta \le 2\pi, \qquad 0 \le \varphi \le \pi .
$$

The product $\sin 6\theta\,\sin 5\varphi$ takes every value between $-1$ and $1$, so

$$
\min \rho = 1 - \frac{1}{5} = \frac{4}{5},
\qquad \max \rho = 1 + \frac{1}{5} = \frac{6}{5}.
$$

The two extremes do not sit on the poles: at $\varphi = 0$ and at $\varphi = \pi$ the factor $\sin 5\varphi$ is zero, so $\rho = 1$ on the whole polar axis. The extremes sit on the two families of directions where $\sin 6\theta\,\sin 5\varphi = \pm 1$, and Part 5 counts those directions.

Because $\rho$ stays positive, the surface closes around the origin, and every ray from the origin crosses it once. That is why the body is star shaped and why one triple integral covers it without a split.

## Result

The smallest radius is $0.8 = \frac{4}{5}$ and the largest radius is $1.2 = \frac{6}{5}$. Figure 1 draws the body inside the unit sphere and the radius over the whole rectangle of the angles. The seam $\theta = 0$ against $\theta = 2\pi$ closes to $3.331 \times 10^{-16}$, and every one of $256$ sampled rays crosses the surface once.

## Common mistake

A reader may take the body for the unit ball with bumps added on the outside, but the valleys sink below $\rho = 1$ and reach [CORRECT_VALUE], so the body is not a superset of the unit ball. A reader may also expect the extremes on the polar axis, but the factor $\sin 5\varphi$ removes the bump there, and the radius on the axis is exactly $1$.

## Verification

The script `code/part1_verify.py` checks the two bounds against the constants of `code/bumpy_sphere.py`, compares the radius at both poles from the scalar function with the radius from the vectorised function, measures the seam difference, counts the crossings of $256$ rays, and checks the volume of the unit ball by quadrature. The last row of `code/outputs/part1_summary.md` reports $4.18879020479$ against $4\pi/3$ with a difference of $8.882 \times 10^{-16}$, which shows that the quadrature routine of the later parts is sound before it meets the bumpy surface.
