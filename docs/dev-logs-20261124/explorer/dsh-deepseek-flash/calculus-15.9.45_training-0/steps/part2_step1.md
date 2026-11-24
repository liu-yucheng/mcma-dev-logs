# Part 2, Step 1: Expand the cube and read its four terms

## Reason

The integrand is a cube of a sum, and a cube of a sum is a polynomial of degree three. Expanding it turns one hard integral into four easy integrals, one for each power of the bump. The expansion also shows which terms can survive: a term with an odd power of $\sin 6\theta$ integrates to zero over a full turn, so the reader learns before any integration which two of the four terms must vanish.

## Computation

Write the bump as one letter:

$$
t = \frac{1}{5}\sin 6\theta\,\sin 5\varphi,
\qquad \rho = 1 + t .
$$

The binomial expansion gives

$$
(1+t)^{3} = 1 + 3t + 3t^{2} + t^{3}.
$$

Insert the expansion into the integral of Step 1.2 and split the integral into four terms:

$$
V = \frac{1}{3}\iint (1 + 3t + 3t^{2} + t^{3})\sin\varphi\,d\varphi\,d\theta
= T_{0} + T_{1} + T_{2} + T_{3}.
$$

The linear term carries the factor $\int_{0}^{2\pi}\sin 6\theta\,d\theta$, which is zero because the sine completes three full periods over one turn. The cubic term carries the factor $\int_{0}^{2\pi}\sin^{3}6\theta\,d\theta$, which is also zero because the odd power of a sine completes three full periods as well. So only the constant term and the quadratic term can contribute a nonzero volume.

## Result

The four terms are $T_{0} = 4.18879020479$, $T_{1} = 0$, $T_{2} = 0.126933036509$, and $T_{3} = 0$. Figure 2 draws them as bars and shows their sum $4.3157232413$. The constant term is the volume of the unit ball and the quadratic term is the whole excess of the bumpy body over that ball.

## Common mistake

A reader may keep the linear term, but the azimuthal factor makes it zero, and the printed value $2.419 \times 10^{-18}$ of the row `linear term of the cube: exact against quadrature` of `code/outputs/part2_summary.md` is the residue of the floating point sum and not a small volume. A reader may also treat the quadratic term as the excess of the peaks alone, but the valleys enter the same term with the same weight, because the square of a negative bump is positive.

## Verification

The script `code/part2_verify.py` computes each of the four terms twice. The exact route builds the product of trigonometric polynomials and integrates each term analytically, and the numerical route integrates the same product with adaptive quadrature. The rows of `code/outputs/part2_summary.md` report $0.126933036509$ against $0.126933036509$ for the quadratic term with a difference of $1.110 \times 10^{-16}$, and $4.3157232413$ against $4.3157232413$ for the sum of the four terms with a difference of $8.882 \times 10^{-16}$.
