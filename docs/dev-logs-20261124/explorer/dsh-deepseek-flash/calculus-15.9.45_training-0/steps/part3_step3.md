# Part 3, Step 3: Assemble the volume in closed form

## Reason

Each factor of the quadratic term now has an exact value, so the term itself has an exact value, and the volume is the constant term plus that value. Adding the two terms also shows the size of the effect in one number: the ratio of the volume of the body to the volume of the unit ball, which the statement implies because the surface is a perturbation of the sphere.

## Computation

Insert $A = \pi$ and $B = \frac{100}{99}$ into the quadratic term of Part 2:

$$
T_{2} = \frac{AB}{25} = \frac{\pi}{25}\cdot\frac{100}{99} = \frac{4\pi}{99}.
$$

Add the constant term:

$$
V = \frac{4\pi}{3} + \frac{4\pi}{99}
= \frac{4\pi}{3}\left(1 + \frac{1}{33}\right)
= \frac{4\pi}{3}\cdot\frac{34}{33}
= \frac{136\pi}{99}.
$$

The ratio to the unit ball is the bracket:

$$
\frac{V}{4\pi/3} = \frac{34}{33} = 1 + \frac{1}{33}.
$$

## Result

The volume is $V = \frac{136\pi}{99} = 4.31572324130$ cubic length units. The body exceeds the unit ball by the factor $\frac{34}{33}$, that is by $\frac{1}{33} = 0.0303030303$, which is about three percent. The excess itself is $\frac{4\pi}{99} = 0.126933036509$.

## Common mistake

A reader may add the two terms as $\frac{4\pi}{3}\cdot\frac{1}{33}$ and forget the unit ball, but the constant term is part of the volume, so the sum carries both terms. A reader may also divide by $33$ twice, but the bracket $1 + \frac{1}{33}$ is already the ratio, and the ratio equals $\frac{34}{33}$.

## Verification

The script `code/part3_verify.py` recomputes the ratio from two directions: from the closed form $\frac{34}{33}$ and from the quotient of the numerical volume and the volume of the unit ball. The row `relative increase of the volume: exact against quadrature` of `code/outputs/part3_summary.md` reports $0.030303030303$ against $0.030303030303$ with a difference of $2.776 \times 10^{-17}$. Part 4 then checks the value of $V$ itself by four independent numerical methods.
