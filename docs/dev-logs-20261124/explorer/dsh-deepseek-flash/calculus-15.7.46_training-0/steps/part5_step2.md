# Part 5, Step 2: Rewrite the answer in terms of the mass and check it

## Reason

The mass of Step 1 lets the moment of inertia take the standard form $I_{z} = c\,M h^{2}$. The
constant $c$ shows how the mass is spread, and the checks of this step catch an algebra slip in that
constant.

## Computation

Replace $M$ by $\pi k h^{3}/3$ inside the answer of Part 3:

$$\frac{3}{10}\,M\,h^{2} = \frac{3}{10} \cdot \frac{\pi k h^{3}}{3} \cdot h^{2}
= \frac{\pi k h^{5}}{10} = I_{z} .$$

Two checks follow from the same expression.

- The dimension: $k$ is a mass per unit volume, so $k h^{5}$ is a mass times a squared length, which
  is the dimension of a moment of inertia. The constant $\pi/10$ carries no dimension.
- The scaling: replace $h$ by $2h$. Then $I_{z}$ is multiplied by $2^{5} = 32$, because the answer
  holds $h^{5}$ and no other power of $h$.

## Result

$$I_{z} = \frac{\pi k h^{5}}{10} = \frac{3}{10}\,M\,h^{2},
\qquad M = \frac{\pi k h^{3}}{3} .$$

A solid cylinder of radius $h$ has $I_{z} = \tfrac{1}{2}M h^{2}$, so the cone has the smaller
constant $3/10$: its mass lies nearer the axis than the mass of the cylinder.

Verification: `code/part5_verify.py` substitutes $M = \pi k h^{3}/3$ into $(3/10)M h^{2}$ and
simplifies the result to $\pi h^{5}k/10$ by a symbolic computation. At $k = 2.3$ and $h = 1.7$ the
formula gives 10.2594083368 and triple quadrature gives 10.2594083368. The script also computes the
ratio $I_{z}(2h)/I_{z}(h)$ by quadrature as 32.0000000000 and from the formula as 32.0000000000,
against the expected value 32.

> **Final answer.** $I_{z} = \dfrac{\pi k h^{5}}{10} = \dfrac{3}{10}\,M h^{2}$, with
> $M = \dfrac{\pi k h^{3}}{3}$ the mass of the cone. At $k = 2.3$ and $h = 1.7$ the value is
> $10.2594083368$.
