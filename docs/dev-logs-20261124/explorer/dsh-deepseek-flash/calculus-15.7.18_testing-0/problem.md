# Problem statement

- Source file: `problem/source/problem.png`, a screenshot of a textbook exercise page.
- Source identity: the breadcrumb of the screenshot reads "Home > Calculus: Early
  Transcendentals > 15.7 Triple Integrals > Exercise: 18".
- Session: `20261123_070047_tutoring_problem_20`.
- Mode: tutoring.

## Statement

Evaluate the triple integral.

$$
\iiint_E z \, dV
$$

The solid $E$ is bounded by the cylinder $y^{2} + z^{2} = 9$ and the planes
$x = 0$, $y = 3x$, and $z = 0$, in the first octant.

## Given data

Each line gives one fact and the file that holds the fact.

- Integrand: the function $z$. Source: `problem/source/problem.png`, statement line 2.
- Differential: $dV$, a volume element. Source: `problem/source/problem.png`, statement line 2.
- Integration domain: the solid $E$. Source: `problem/source/problem.png`, statement line 2.
- Curved boundary surface: the cylinder $y^{2} + z^{2} = 9$.
  Source: `problem/source/problem.png`, statement line 2.
- Flat boundary surface 1: the plane $x = 0$.
  Source: `problem/source/problem.png`, statement line 2.
- Flat boundary surface 2: the plane $y = 3x$.
  Source: `problem/source/problem.png`, statement line 2.
- Flat boundary surface 3: the plane $z = 0$.
  Source: `problem/source/problem.png`, statement line 2.
- Position condition: the solid lies in the first octant.
  Source: `problem/source/problem.png`, statement line 2.

The source gives no numerical value of the integral and no numerical bound.
The two numbers of the statement are 9 and 3, in the two boundary equations.
Every other number of the tutorial must come from a computation of a verification
script.

## Reading of the position condition

The first octant is the set of the points with $x \ge 0$, $y \ge 0$, and $z \ge 0$.
The tutorial uses this reading and states it in the step that describes the region.
The source does not write the three inequalities, because the phrase "in the first
octant" carries them.

## Quantity asked

The problem asks for one number: the value of the triple integral of the function
$z$ over the solid $E$.
The answer is a single real number.
Its unit is the unit of a volume times the unit of $z$.
The problem asks for no intermediate quantity and for no graph.

## Facts that the tutorial must derive and must not assume

1. The region of the variables $y$ and $z$ that the cylinder and the plane $z = 0$
   leave in the first octant.
2. The interval of the variable $x$ for one fixed pair $(y, z)$ of that region.
3. The order of integration that turns the description into three nested bounds.
4. The value of the innermost integral, of the middle integral, and of the outer
   integral.
5. The value of the complete integral.
6. A second order of integration that gives the same value, as an independent check.

## Plan of the parts

1. **Part 1, the solid.** Draw $E$ and name each boundary surface.
   Derive the projection of $E$ on the coordinate planes from the four boundary
   conditions.
2. **Part 2, the bounds.** Choose an order of integration.
   Derive the three nested bounds from the projection of Part 1.
   State why each bound holds.
3. **Part 3, the evaluation.** Evaluate the three nested integrals in the chosen
   order.
   State the value.
4. **Part 4, the check.** Evaluate the same integral in a second order.
   Compare the two values with a numerical quadrature that uses neither order.

The plan names the parts of the tutorial.
The plan gives no value, because the intake stage solves nothing.

## Workspace

- `problem/problem.md`: this file.
- `problem/source/problem.png`: an exact copy of the source screenshot.
- `steps/`: one file for each step, written by the tutoring stage.
- `code/`: the verification scripts, the figures, and the outputs.
- `tutorial.html`: the composed tutorial, written by the tutoring stage.
