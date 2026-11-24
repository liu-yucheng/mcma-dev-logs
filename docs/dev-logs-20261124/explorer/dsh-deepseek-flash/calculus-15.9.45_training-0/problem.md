# Problem statement

## Source

- Book: *Calculus, Early Transcendentals*.
- Section: 15.9, "Triple Integrals in Spherical Coordinates".
- Exercise: 45.
- Capture: `problem/source/problem.png`, 976 x 398 pixels. The file is a byte-identical copy of the training input
  `calculus-15.9.45/problem.png`.
- The capture has three parts: the breadcrumb `Home > Calculus, Early Transcendentals > 15.9 Triple Integrals in
  Spherical Coordinates > Exercise: 45`, the statement paragraph, and one rendered plot of the surface.

## Statement

A transcription of the statement paragraph of the capture follows.

> The surfaces $\rho = 1 + \frac{1}{5}\sin m\theta \sin n\phi$ have been used as models for tumors. The "bumpy
> sphere" with $m = 6$ and $n = 5$ is shown. Use a computer algebra system to find the volume it encloses.

The statement uses the letter $\phi$ for the polar angle. This tutorial writes $\varphi$ for the same angle, because
the renderer of this workspace shows $\phi$ and $\varphi$ alike and one glyph for one angle prevents a misreading.

## Given data

Each item below is a literal reading of the capture. No item is a deduction.

| Item | Value | Source |
| --- | --- | --- |
| Family of surfaces | $\rho = 1 + \frac{1}{5}\sin m\theta \sin n\varphi$ | statement paragraph, `problem/source/problem.png` |
| First integer parameter | $m = 6$ | statement paragraph, `problem/source/problem.png` |
| Second integer parameter | $n = 5$ | statement paragraph, `problem/source/problem.png` |
| Coefficient of the bump term | $\frac{1}{5}$ | statement paragraph, `problem/source/problem.png` |
| Body under study | the "bumpy sphere" with $m = 6$, $n = 5$ | statement paragraph and plot, `problem/source/problem.png` |
| Allowed aid | a computer algebra system | statement paragraph, `problem/source/problem.png` |
| Book section | 15.9, Triple Integrals in Spherical Coordinates | breadcrumb, `problem/source/problem.png` |

The capture gives no further numeric data. It gives no interval for $\theta$, no interval for $\varphi$, no density,
and no unit of length.

## Quantity to find

The volume of the solid region that the surface

$$
\rho(\theta, \varphi) = 1 + \frac{1}{5}\sin(6\theta)\sin(5\varphi)
$$

encloses.

## Conventions of this tutorial

- Spherical coordinates follow the convention of Section 15.9: $x = \rho\sin\varphi\cos\theta$,
  $y = \rho\sin\varphi\sin\theta$, $z = \rho\cos\varphi$, with $\rho \ge 0$, $0 \le \theta \le 2\pi$, and
  $0 \le \varphi \le \pi$.
- The angles $\theta$ and $\varphi$ use radian measure.
- A length unit is arbitrary, because the statement gives none. Every volume below is a number of cubic length units.
- The symbol $\rho$ names the radial distance. The symbol $r$ names the distance $\sqrt{x^{2} + y^{2}}$ from the
  $z$-axis when the tutorial needs that distance.

## Method constraint from the statement

The statement asks for a computer algebra system. The tutorial obeys that constraint in two independent ways: one
exact computation with symbolic algebra, and one numeric quadrature that shares no code with the exact computation.
A result counts as confirmed only when the two ways agree. A later stage holds both computations and their
assertions.

## Contents of this stage

This stage states the problem and prepares the workspace. It derives no volume and grades nothing.
