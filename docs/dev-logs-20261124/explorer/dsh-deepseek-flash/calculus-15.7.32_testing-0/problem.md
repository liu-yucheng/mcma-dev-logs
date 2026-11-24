# Problem statement

## Source

- Book: *Calculus, Early Transcendentals*.
- Section: 15.7, "Triple Integrals".
- Exercise: 32.
- Capture: `problem/source/problem.png`, 981 x 225 pixels, 13691 bytes, SHA-256
  `07189be0086eb3671b8356de7ed60fe2ec09b51ee605ca98324496807bcb9bd1`. The file is a
  byte-identical copy of the input `calculus-15.7.32/problem.png`.
- The capture has three parts: the breadcrumb `Home > Calculus, Early Transcendentals > 15.7 Triple Integrals >
  Exercise: 32`, the statement paragraph, and one centered row of four surface equations.

## Statement

A transcription of the statement paragraph of the capture follows.

> Express the integral $\iiint_E f(x, y, z)\,dV$ as an iterated integral in six different ways, where $E$ is the
> solid bounded by the given surfaces.

The four surfaces of the capture follow.

$$
x = 2, \qquad y = 2, \qquad z = 0, \qquad x + y - 2z = 2
$$

## Given data

Each row is a literal reading of the capture. No row is a deduction.

| Item | Value | Source |
| --- | --- | --- |
| Integrand | an arbitrary function $f(x, y, z)$ | statement paragraph, `problem/source/problem.png` |
| Differential | $dV$, the volume element | statement paragraph, `problem/source/problem.png` |
| Integration domain | the solid $E$ | statement paragraph, `problem/source/problem.png` |
| Required form | an iterated integral, six different ways | statement paragraph, `problem/source/problem.png` |
| Flat boundary surface 1 | the plane $x = 2$ | surface row, `problem/source/problem.png` |
| Flat boundary surface 2 | the plane $y = 2$ | surface row, `problem/source/problem.png` |
| Flat boundary surface 3 | the plane $z = 0$ | surface row, `problem/source/problem.png` |
| Flat boundary surface 4 | the plane $x + y - 2z = 2$ | surface row, `problem/source/problem.png` |
| Book section | 15.7, Triple Integrals | breadcrumb, `problem/source/problem.png` |

The capture gives no numerical value of the integral, no formula for $f$, no density, and no unit of length.
The capture holds three constants in the first three surface equations, $2$, $2$, and $0$, and the three
coefficients $1$, $1$, and $-2$ of the fourth surface equation.
Every other number of the tutorial must come from a computation of a verification script.

## Quantity asked

The problem asks for six formulas and for no number.

Each formula is one iterated integral over the same solid $E$ with the same integrand $f$.
The six formulas differ in the order of the three integrations.
The three variables $x$, $y$, and $z$ have six orders, so the problem asks for one formula for each order.

This tutorial writes an order from the inner integral to the outer integral.
For example, the order $dz\,dx\,dy$ means that $z$ is the variable of the inner integral, $x$ is the variable of the
middle integral, and $y$ is the variable of the outer integral.

## Reading points that the statement leaves open

1. The statement names four surfaces and no further surface. It does not write the planes $x = 0$ and $y = 0$.
   The tutorial must decide whether those two planes bound $E$ or whether the four named surfaces already close $E$,
   and it must show the decision from the four equations.
2. The fourth surface is a plane with the normal vector $(1, 1, -2)$. The tutorial must state which side of that
   plane holds $E$.
3. The statement gives no order of the factors $f$ and $dV$ beyond the usual reading $f\,dV$.

## Conventions of this tutorial

- A point of space is an ordered triple $(x, y, z)$ of real numbers in the usual Cartesian frame.
- The symbol $E$ names the closed solid, and the symbol $\partial E$ names its boundary.
- The symbol $dV$ names the volume element $dz\,dy\,dx$ in the order of the differentials that the formula writes.
- The function $f$ is continuous on $E$, so every order of integration gives the same value.
- The tutorial writes an order from the inner integral to the outer integral, as stated above.

## Facts that the tutorial must derive and must not assume

1. The shape of $E$ as the intersection of the four half-spaces that the four surfaces bound.
2. The projection of $E$ on each of the three coordinate planes.
3. The interval of the innermost variable for one fixed pair of the other two variables, for each of the six orders.
4. The reason for each lower bound of each integral, taken from the inequalities of the solid.
5. The value of the volume of $E$, as one independent check of the six formulas with $f = 1$.
6. One numerical quadrature of one order, as a second independent check.

## Plan of the parts

1. **Part 1, the solid.** Draw $E$. Name each boundary surface and each vertex. Derive the three coordinate
   inequalities of $E$ from the four surface equations. Derive the projection of $E$ on each coordinate plane.
2. **Part 2, the orders with $z$ innermost.** Derive the bounds of the orders $dz\,dx\,dy$ and $dz\,dy\,dx$ from the
   projection on the plane $z = 0$. State why each bound holds.
3. **Part 3, the orders with $y$ innermost.** Derive the bounds of the orders $dy\,dx\,dz$ and $dy\,dz\,dx$ from the
   projection on the plane $y = 0$.
4. **Part 4, the orders with $x$ innermost.** Derive the bounds of the orders $dx\,dy\,dz$ and $dx\,dz\,dy$ from the
   projection on the plane $x = 0$.
5. **Part 5, the checks.** Compare the six formulas with $f = 1$ against the volume of $E$. Compare one formula
   against a numerical quadrature that uses no symbolic bound.

The plan names the parts of the tutorial.
The plan gives no bound and no value, because the intake stage solves nothing.

## Workspace

- `problem/problem.md`: this file.
- `problem/source/problem.png`: an exact copy of the source capture.
- `steps/`: one file for each step, written by the tutoring stage.
- `code/`: the verification scripts, the figures, and the outputs.
- `tutorial.html`: the composed tutorial, written by the tutoring stage.

## Contents of this stage

This stage states the problem and prepares the workspace.
It derives no bound, evaluates no integral, and grades nothing.
