# Part 4, Step 1: Check the closed form by four numerical methods

## Reason

A closed form that rests on one chain of algebra deserves an independent measurement, and the statement asks for a computer algebra system, which means the reader must be able to trust the algebra. Four methods with different failure modes give that trust: an adaptive quadrature of the two-angle integral, a midpoint sum that samples the integrand at a fixed grid, a random sampler whose error the script can estimate, and a volume count on a Cartesian grid that never uses spherical coordinates at all.

## Computation

The four methods compute a value of $V$ and one error estimate each:

$$
\text{adaptive: } \left|\hat V - V\right| \le 10^{-10},
\qquad
\text{midpoint: } \left|\hat V - V\right| = O(h^{2}),
$$

$$
\text{random: } \left|\hat V - V\right| \le 3\,\sigma,
\qquad
\text{grid count: } \left|\hat V - V\right| = O(h),
$$

In these expressions $\sigma$ is the standard error of the random estimate and $h$ is the step of the grid. The random method draws points in the cube $\left[-1.3, 1.3\right]^{3}$ and counts the share that falls inside the surface, so it uses the inequality $\rho \le$ the surface and no angle at all. The grid count tests the same inequality at the nodes of a Cartesian mesh and multiplies the share by the volume of the cube.

## Result

The adaptive quadrature returns $4.3157232413$ against the exact $4.3157232413$, with a difference of $8.882 \times 10^{-16}$. The midpoint sum over $2000$ cells per angle returns $4.31572367194$, with a difference of $4.306 \times 10^{-7}$. The random sample of $8000000$ points returns $4.318276001$ with a standard error of $0.00267513$, a distance of $0.954$ standard errors from the exact value. The Cartesian count on $261$ points per axis returns $4.315427$, with a difference of $2.962 \times 10^{-4}$. Every method agrees with the closed form within its own error.

## Common mistake

A reader may compare the random estimate with the exact value without its standard error and read the third decimal as an error of the algebra, but the difference lies inside one standard error, so the sample says nothing against the closed form. A reader may also expect the Cartesian count to converge as fast as the midpoint sum, but the count has an error of order $h$ against the order $h^{2}$ of the sum, because the count decides membership at a point and not on a cell.

## Verification

The script `code/part4_verify.py` runs the four methods and compares each with the exact value from `code/bumpy_sphere.py`. The rows of `code/outputs/part4_summary.md` report the four differences above, and the rows `volume over pi: expansion against (4/3)(34/33)` and `ratio to the unit ball: exact against the quotient of the volumes` report $\frac{136}{99}$ against $\frac{136}{99}$ and $1.0303030303$ against $1.0303030303$.
