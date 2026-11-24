# Problem Statement

## Normalized statement

Express the integral

    ∭_E f(x, y, z) dV

as an iterated integral in six different ways, where E is the solid that the given surfaces bound.

The given surfaces are

    y^2 + z^2 = 9,    x = -2,    x = 2.

## Given data

| Item | Value | Source of the fact |
| --- | --- | --- |
| Integrand | f(x, y, z) | `problem/source/problem.png`, line 1 of the statement |
| Integration domain | the solid E | `problem/source/problem.png`, line 1 of the statement |
| Surface 1 | y^2 + z^2 = 9 | `problem/source/problem.png`, surface list |
| Surface 2 | x = -2 | `problem/source/problem.png`, surface list |
| Surface 3 | x = 2 | `problem/source/problem.png`, surface list |
| Requested count of orders | six | `problem/source/problem.png`, line 1 of the statement |
| Textbook reference | Calculus, Early Transcendentals, section 15.7, exercise 30 | `problem/source/problem.png`, navigation trail |

The image gives no numerical value for f. The letter f is a general continuous function.

## Quantity that the problem asks for

Six iterated integrals. Each iterated integral must equal the triple integral of f over E. Each
iterated integral must give one order of integration and the six limits that the order needs.

## Shape facts that the statement gives

1. The surface y^2 + z^2 = 9 is a circular cylinder. Its axis is the x-axis. Its radius is 3.
   Source: the equation y^2 + z^2 = 9 in `problem/source/problem.png`.
2. The surfaces x = -2 and x = 2 are two parallel planes. They cut the cylinder.
   Source: the equations x = -2 and x = 2 in `problem/source/problem.png`.
3. The solid E is the part of the cylinder that the two planes bound.
   Source: the phrase "the solid bounded by the given surfaces" in `problem/source/problem.png`.

## Stage note

This file records the statement only. The stage does not solve the problem. The six orders, the
limits, and the verification scripts come in the later stages.
