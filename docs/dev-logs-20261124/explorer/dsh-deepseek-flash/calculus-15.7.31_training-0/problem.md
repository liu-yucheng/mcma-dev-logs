# Problem Statement

- Source text: `problem/source/problem.png`
- Source collection: `D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261124/mcma-dataset-20261124/training/problems/calculus-15.7.31/problem.png`
- Source book: Stewart, Calculus, Early Transcendentals, Chapter 15.7 Triple Integrals, Exercise 31.
  The breadcrumb of the image gives this location.

## Statement

> Express the integral
>
> $$\iiint_E f(x, y, z)\,dV$$
>
> as an iterated integral in six different ways, where $E$ is the solid bounded by the given surfaces.

$$
y = x^2, \qquad z = 0, \qquad y + 2z = 4
$$

## Given Data

| Item | Value | Fact |
| --- | --- | --- |
| Surface 1 | $y = x^2$ | A parabolic cylinder. The image gives this equation. |
| Surface 2 | $z = 0$ | A horizontal plane. The image gives this equation. |
| Surface 3 | $y + 2z = 4$ | A plane. The image gives this equation. An equivalent form is $z = (4 - y)/2$. |
| Solid $E$ | The solid bounded by the three surfaces above | The image gives this description. |
| Integrand | $f(x, y, z)$ | The image gives this symbol. The problem gives no formula for $f$. |
| Volume element | $dV$ | The image gives this symbol. |

## Quantity Requested

Six iterated integrals. Each integral has the value $\iiint_E f(x, y, z)\,dV$.

The six integrals are the six orders of integration:

1. $dz\,dy\,dx$
2. $dz\,dx\,dy$
3. $dy\,dz\,dx$
4. $dy\,dx\,dz$
5. $dx\,dz\,dy$
6. $dx\,dy\,dz$

## Observations That the Next Stage Must Use

- The problem gives three surfaces and no fourth surface.
  The three surfaces close one bounded region, and $E$ is that region.
- The problem gives no number and no formula for $f$.
  The answer is a set of six groups of integration limits, and each group contains $f(x, y, z)$.
- The image gives one equation for each surface and gives no figure.
  The next stage must derive each limit from the three defining inequalities.
  The next stage must not take a shape from a drawing.
- The label of Exercise 31 sits in the breadcrumb, not in the statement.
  The statement itself has one sentence and one line of equations.

## Files

| Path | Content |
| --- | --- |
| `problem/problem.md` | This normalized statement. |
| `problem/source/problem.png` | The source image. The copy is byte-identical to the dataset file. SHA-256: `067d4108fac1937267dad5bf128a53abcd8d1b3037310fb9cd903932e179a1e0`. |
