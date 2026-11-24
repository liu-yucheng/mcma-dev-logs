# Part 2, Step 2: Reduce the double integral to a product of two single integrals

## Reason

The surviving integrand is the product of a function of $\theta$ and a function of $\varphi$. A product of that shape splits into the product of two single integrals, and each single integral has its own exact value. The split is the reason a computer algebra system returns a short closed form instead of a long expression.

## Computation

The quadratic term of Step 2.1 is

$$
T_{2} = \frac{1}{3}\iint 3t^{2}\sin\varphi\,d\varphi\,d\theta
= \frac{1}{25}\int_{0}^{2\pi}\sin^{2}6\theta\,d\theta
\int_{0}^{\pi}\sin^{2}5\varphi\,\sin\varphi\,d\varphi .
$$

The two factors separate because the limits of each integral are constants and the integrand is a product. Write

$$
A = \int_{0}^{2\pi}\sin^{2}6\theta\,d\theta,
\qquad
B = \int_{0}^{\pi}\sin^{2}5\varphi\,\sin\varphi\,d\varphi,
\qquad
T_{2} = \frac{AB}{25}.
$$

The constant term follows the same split with $\sin^{2}$ replaced by $1$:

$$
T_{0} = \frac{1}{3}\cdot 2\pi \cdot 2 = \frac{4\pi}{3}.
$$

## Result

The constant term is $\frac{4\pi}{3} = 4.18879020479$, which is the volume of the unit ball, as it must be, because at $t = 0$ the surface is the unit sphere. The quadratic term is $\frac{AB}{25}$, and Part 3 evaluates $A$ and $B$ exactly. The printed value of the quadratic term is $0.126933036509$, and Part 3 shows that this number equals $\frac{4\pi}{99}$.

## Common mistake

A reader may split the integral before checking that the limits of $\varphi$ do not depend on $\theta$, but a split needs constant limits, and here both pairs of limits are constant, which is why the split is legal. A reader may also carry the factor $\frac{1}{3}$ into only one of the two factors, but that factor multiplies the whole product, so it appears once in the final value and not twice.

## Verification

The script `code/part2_verify.py` compares the exact split with a numerical quadrature of the same product. The rows `constant term of the cube: exact against quadrature` and `quadratic term of the cube: exact against quadrature` of `code/outputs/part2_summary.md` report differences of $8.882 \times 10^{-16}$ and $1.110 \times 10^{-16}$, so the split and the coefficient $\frac{1}{25}$ are both right. The row `share of the quadratic term: exact against quadrature` reports $0.030303030303$ against $0.030303030303$, which is the $\frac{1}{33}$ of Part 5.
