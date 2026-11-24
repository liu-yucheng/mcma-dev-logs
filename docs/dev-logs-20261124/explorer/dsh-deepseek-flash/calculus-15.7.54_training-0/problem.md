# Average Value of a Function over a Paraboloid Solid

## Problem statement

The problem is exercise 54 of section 15.7 of *Calculus, Early Transcendentals*.
The page gives one definition and then one task.
The definition reads:

> The average value of a function $f(x, y, z)$ over a solid region $E$ is defined to be
>
> $$f_{\mathrm{ave}} = \frac{1}{V(E)} \iiint_E f(x, y, z) \, dV,$$
>
> where $V(E)$ is the volume of $E$.
> For instance, if $\rho$ is a density function, then $\rho_{\mathrm{ave}}$ is the average density of $E$.

The task reads:

> Find the average value of the function $f(x, y, z) = x^2 z + y^2 z$ over the region enclosed by the
> paraboloid $z = 1 - x^2 - y^2$ and the plane $z = 0$.

## Given data

| Item | Value | Source |
| --- | --- | --- |
| Function to average | $f(x, y, z) = x^2 z + y^2 z$ | `problem/source/problem.png`, last line of the page |
| Upper boundary surface | the paraboloid $z = 1 - x^2 - y^2$ | `problem/source/problem.png`, last line of the page |
| Lower boundary surface | the plane $z = 0$ | `problem/source/problem.png`, last line of the page |
| Definition of the average value | $f_{\mathrm{ave}} = \frac{1}{V(E)} \iiint_E f(x, y, z) \, dV$ | `problem/source/problem.png`, definition line of the page |
| Meaning of $V(E)$ | the volume of the solid region $E$ | `problem/source/problem.png`, line after the definition |
| Textbook location | section 15.7, exercise 54 | `problem/source/problem.png`, breadcrumb of the page |

The word "enclosed" fixes the region as the bounded body between the two surfaces.
No other constraint on $x$, $y$, or $z$ appears on the page.

## Quantity that the problem asks for

The problem asks for one number: the average value $f_{\mathrm{ave}}$ of $f$ over the solid region $E$.
The problem does not ask for the volume alone and it does not ask for the integral alone.
The definition gives the answer as one ratio, so the answer has two ingredients:

1. the volume $V(E)$ of the region $E$;
2. the triple integral $\iiint_E (x^2 z + y^2 z) \, dV$.

The solid region $E$ itself is a third ingredient.
The page does not give $E$ in inequality form, so the tutorial must derive $E$ from the two surfaces.
The derivation is part of the work.

## Facts that the page fixes and facts that the tutorial must derive

The page fixes the two boundary surfaces and the integrand.
The page fixes the formula for the average value.
The page does not fix the following items, and the tutorial derives each one:

- the projection of $E$ on the plane $z = 0$;
- the inequality description of $E$;
- the order of integration;
- the value of $V(E)$;
- the value of the triple integral;
- the value of $f_{\mathrm{ave}}$.

## Conventions of this tutorial

- The region $E$ is a closed body, so each boundary surface belongs to $E$.
  The boundary does not change a volume or an integral, but the tutorial states the limits as closed
  inequalities and the reader may check the boundary separately.
- A symbol with a subscript names a fixed quantity.
  The symbol $f_{\mathrm{ave}}$ names the answer.
- Every numerical claim starts from the inequality description of $E$.
  A figure illustrates the region, but a figure does not define the region.
- Every numerical claim has a check in one Python file under `code/`.
  The tutorial cites the file and the line range of the check beside the claim.

## Planned parts

The tutorial divides the work into five parts.
Each part contains short steps that a reader can check by hand.

| Part | Subject | Reason for the position of the part |
| --- | --- | --- |
| Part 1 | the region $E$ and its projection on the plane $z = 0$ | the limits of every later integral come from this part |
| Part 2 | the volume $V(E)$ | the definition needs $V(E)$ as the denominator |
| Part 3 | the triple integral of $f$ over $E$ | the definition needs this integral as the numerator |
| Part 4 | the ratio and the final value | the definition combines the two earlier results |
| Part 5 | a check of the whole chain and a summary | the reader needs one place that compares all results |

Part 1 must come first, because a reader who takes the projection from a picture can take a wrong
projection.
Part 2 and Part 3 share the same limits, so a reader can compare them step by step.
Part 4 holds one arithmetic step, so a reader can repeat it without a tool.
Part 5 repeats every result against one independent computation.

## Source files

| File | Role | State |
| --- | --- | --- |
| `problem/source/problem.png` | the only source of the statement and the given data | an unchanged copy of the dataset file, 983 by 289 pixels, SHA-256 `42d2f78eb108ffbc930b2aad9d1948631d75c512a73ea9b335150943b58f599c` |

The dataset path of the file is
`mcma-dataset-20261124/training/problems/calculus-15.7.54/problem.png`.
The copy in `problem/source/` holds the same bytes as the dataset file.
