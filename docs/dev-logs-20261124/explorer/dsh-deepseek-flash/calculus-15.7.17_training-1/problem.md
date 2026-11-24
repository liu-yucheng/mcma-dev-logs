# Problem: Triple integral over a paraboloid-bounded solid

## Origin

- Book page: Calculus, Early Transcendentals. Section 15.7, Triple Integrals. Exercise 17.
- Screenshot: `problem/source/problem.png`. Size 981 by 213 pixels. The page header reads "Home > Calculus, Early Transcendentals > 15.7 Triple Integrals > Exercise: 17".
- Dataset copy of the screenshot: `D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261124/mcma-dataset-20261124/training/problems/calculus-15.7.17/problem.png`.
- Integrity check: MD5 `e412ebf68afb3fe20261c73890244896` for both copies. The two copies are identical byte for byte.

## Statement

The statement in the screenshot has two sentences. The first sentence gives the task. The second sentence gives the region.

1. "Evaluate the triple integral."
2. "$\iiint_E x \, dV$, where $E$ is bounded by the paraboloid $x = 4y^2 + 4z^2$ and the plane $x = 4$."

The same statement in one sentence:

> Evaluate $\iiint_E x \, dV$, where the solid $E$ is bounded by the paraboloid $x = 4y^2 + 4z^2$ and the plane $x = 4$.

## Given data

| Item | Value | Source |
| --- | --- | --- |
| Integrand | $f(x,y,z) = x$ | Screenshot, second sentence, after the integral sign |
| Volume element | $dV$ | Screenshot, second sentence, after the integrand |
| Number of integration variables | Three. The symbol is a triple integral. | Screenshot, second sentence, the sign $\iiint$ |
| Lower bounding surface | Paraboloid $x = 4y^2 + 4z^2$ | Screenshot, second sentence, first surface |
| Upper bounding surface | Plane $x = 4$ | Screenshot, second sentence, second surface |
| Name of the solid | $E$ | Screenshot, second sentence, phrase "where $E$ is bounded by" |
| Coordinate system | Rectangular coordinates $(x, y, z)$ | Screenshot, second sentence, uses $x$, $y$, and $z$ |

The statement gives no numeric value of the integral. The statement gives no further constraint on $E$.

## Quantity that the problem asks for

The problem asks for the number $I$ that the triple integral gives:

$$I = \iiint_E x \, dV.$$

The answer is one real number.

## Region description

The next three facts follow from the two bounding surfaces. They describe the region. They do not evaluate the integral.

- The paraboloid $x = 4y^2 + 4z^2$ opens in the positive $x$ direction. Its vertex is the origin $(0,0,0)$.
- The plane $x = 4$ is a vertical plane. It closes the solid on the side of large $x$.
- The two surfaces meet where $4y^2 + 4z^2 = 4$. This condition is equivalent to $y^2 + z^2 = 1$. The intersection is therefore the circle of radius 1 in the plane $x = 4$, and the solid stands on the unit disk in the $yz$-plane.
- The solid $E$ is closed and bounded. The solid is symmetric about the plane $y = 0$ and about the plane $z = 0$.

The tutoring stage must verify each of the three derived facts with a script.

## Reading notes

- The screenshot uses italic math type. The symbol $E$ is the name of the solid, not the number $e$.
- The exponent is two on both $y$ and $z$. No square root and no fraction appears in the statement.
- The plane is $x = 4$, not $z = 4$. The right side of the paraboloid equation is $4y^2 + 4z^2$.

## Source files

| File | Role |
| --- | --- |
| `problem/source/problem.png` | Unchanged copy of the screenshot that holds the statement |
| `problem/problem.md` | This normalized record |

No other source file supports this problem.
