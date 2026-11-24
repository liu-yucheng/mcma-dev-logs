# Problem 9: Six Iterated Integrals over One Solid

## Source record

| Item | Value |
| --- | --- |
| Source file | `problem/source/problem.png` |
| Original path | `.../mcma-dataset-20261124/training/problems/calculus-15.7.29/problem.png` |
| Original root | `D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261124` |
| SHA-256 | `5c5821cf701e9006f635eb042cb534d457c36938a730a687a76a0795d5aa68d6` |
| Image size | 978 by 223 pixels, RGBA |
| Book location | Calculus, Early Transcendentals, Section 15.7 Triple Integrals, Exercise 29 |

The copy in `problem/source/problem.png` is byte-identical to the original path. The
SHA-256 value above is the hash of both files.

## Problem statement

The source image holds this text. The quotation keeps the original wording.

> Express the integral
> $\iiint_E f(x, y, z)\, dV$
> as an iterated integral in six different ways, where $E$ is the solid bounded by the given
> surfaces.

The source image gives these two surfaces under the sentence.

> $y = 4 - x^{2} - 4z^{2}, \quad y = 0$

## Given data

| Symbol | Meaning | Source of the fact |
| --- | --- | --- |
| $f$ | An arbitrary integrand of three variables | Statement sentence, `problem/source/problem.png` |
| $E$ | The solid that the two surfaces bound | Statement sentence, `problem/source/problem.png` |
| $y = 4 - x^{2} - 4z^{2}$ | The upper surface, an elliptic paraboloid | Surface line of `problem/source/problem.png` |
| $y = 0$ | The lower surface. It is the plane $x z$ | Surface line, the same pixel box |

The surface line comes from the pixel box (260, 150) to (660, 205) of
`problem/source/problem.png`, enlarged three times. The crop makes the coefficients 1
and 4 legible.

The two surfaces close a bounded solid. No other boundary appears in the source image. The
statement gives no numeric value for $f$, so every answer keeps $f$ symbolic.

## Quantity that the problem asks for

Six iterated integrals. Each one equals $\iiint_E f(x, y, z)\, dV$. Each one uses one of the
six orders of the three differentials $dx$, $dy$, and $dz$.

## Facts that the intake stage checks

1. The statement asks for six forms, not for one form. Source: the words "six different ways".
2. The order count is six because three variables give $3! = 6$ orders. This count is a
   property of the request, not a result of the solid.
3. The paraboloid has the coefficient 4 on $z^{2}$ and the coefficient 1 on $x^{2}$. Source:
   the enlarged crop of the surface line. A reader must not read the coefficient of
   $z^{2}$ as 1.
4. The region is described by inequalities on $y$ directly, because both surfaces have the form
   $y = g(x, z)$. This form comes from the surface equations, not from a figure.
5. The source image holds no figure of the solid. Every figure in the tutorial is a product of
   this workspace, and the tutorial must say so.

## Planned work split

The intake stage does not solve the problem. The plan below names the parts and the steps. A
later stage fills each step and writes one verification script for each part.

- **Part 1. Read the solid from the two equations.** Step 1.1: the inequality chain on $y$.
  Step 1.2: the trace of $E$ on the plane $y = 0$. Step 1.3: the largest value of $y$ on $E$.
- **Part 2. The projection of $E$ on the plane $y = 0$.** Step 2.1: the outline of the
  projection in the plane $y = 0$. Step 2.2: the section of $E$ at a fixed value of $y$.
  Step 2.3: the boundary values of $y$.
- **Part 3. The two orders that start with $dy$.** Step 3.1: $dy\, dx\, dz$. Step 3.2:
  $dy\, dz\, dx$.
- **Part 4. The orders that start with $dz$.** Step 4.1: the split of the $x$ range at a fixed
  value of $z$. Step 4.2: $dz\, dy\, dx$. Step 4.3: $dz\, dx\, dy$.
- **Part 5. The orders that start with $dx$.** Step 5.1: the split of the $z$ range at a fixed
  value of $x$. Step 5.2: $dx\, dy\, dz$. Step 5.3: $dx\, dz\, dy$.
- **Part 6. The six forms in one table.** Step 6.1: the projection table. Step 6.2: the check
  that each form gives the same value for one test function.

## Conventions for the later stages

- The $x z$ plane means the plane $y = 0$. A projection that drops the coordinate $y$ lies on
  the plane $y = 0$. A sentence names a plane by the two axes that its points keep.
- The tutorial states a reason before a computation.
- Every numerical claim cites the script that computes it. Each script compares a value from
  one method with a value from a different method.
- The source image gives exactly two surfaces. Part 1 must show from the equations whether the
  solid has another wall, and must not borrow that shape from a figure.

## Open items

- A later stage must decide the exact drawing set. The plan above needs one figure of the
  solid, one figure of the projection, and one figure of each split of an outer range.
- A later stage must choose one test function for the equality check of Part 6. The test
  function must have an exact integral over $E$.
