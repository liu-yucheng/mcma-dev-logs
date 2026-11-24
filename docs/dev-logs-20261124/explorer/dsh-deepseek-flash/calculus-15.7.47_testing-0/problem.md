# Exercise 47, Section 15.7, Triple Integrals

## Source

- Problem image: `problem/source/problem.png`, 983 by 221 pixels.
- Digest of the image: `f39ce5a7acb3e1597c0a4cf02da8fed5499b3f370a4f4d6717cca84ec7f6f26a`.
- The page path is `Home > Calculus, Early Transcendentals > 15.7 Triple Integrals > Exercise: 47`.
- The copy in `problem/source/problem.png` holds the same bytes as the problem image above.
- The digest of the copy and the digest of the problem image are equal.

## Statement

Set up, but do not evaluate, integral expressions for three quantities of one solid.

- (a) The mass.
- (b) The center of mass.
- (c) The moment of inertia about the $z$-axis.

The solid is enclosed by the cylinder $y = x^{2}$ and the planes $z = 0$ and $y + z = 1$.
The density of the solid is $\rho(x, y, z) = \sqrt{x^{2} + y^{2}}$.

## Given data

- **G1. First bounding surface.** Parabolic cylinder $y = x^{2}$, for every $z$.
- **G2. Second bounding surface.** Plane $z = 0$.
- **G3. Third bounding surface.** Plane $y + z = 1$, equivalently $z = 1 - y$.
- **G4. Density function.** $\rho(x, y, z) = \sqrt{x^{2} + y^{2}}$, with no dependence on $z$.
- **G5. Solid.** The bounded component of the region that the surfaces of G1, G2, and G3 delimit.
- **G6. Requested output form.** One integral expression for each of the three quantities.

The source of G1, G2, G3, and G5 is statement line 2 of `problem/source/problem.png`.
The source of G4 is statement line 3 of `problem/source/problem.png`.
The source of G6 is statement line 1 of `problem/source/problem.png`.

The word "enclosed" of G5 names one bounded solid, not an unbounded region. The solid has a
finite volume, and therefore it has a finite mass for the density of G4.

## Quantity asked

The problem asks for three integral expressions. Each expression is a definition of its
quantity. The limits of integration are not part of the given data. The tutorial derives the
limits from G1, G2, G3, and G5.

- (a) The mass $M$ of the solid $D$ with the density $\rho$: $M = \iiint_{D} \rho \, dV$.
- (b) The center of mass $(\bar{x}, \bar{y}, \bar{z})$.
- (b1) The first coordinate: $\bar{x} = \frac{1}{M}\iiint_{D} x\rho \, dV$.
- (b2) The coordinates $\bar{y}$ and $\bar{z}$ take the same form, with $y$ and $z$ in place of $x$.
- (c) The moment of inertia about the $z$-axis: $I_{z} = \iiint_{D} (x^{2} + y^{2}) \rho \, dV$.

The symbol $D$ above is a placeholder for the solid of G5. $D$ is not a given value.

## Properties that the tutorial must treat with care

- The statement prints no limit of integration. Each limit must follow from G1, G2, G3, and G5.
- The cylinder $y = x^{2}$ does not contain $z$. A cross section at a fixed $z$ keeps one shape.
- A cross section at a fixed $y$ is a segment in $x$ that the two planes close in $z$.
- The density of G4 is a distance from the $z$-axis. The moment of inertia of (c) uses its square.
- The order of integration is free. Each order gives the same value of each integral.
- The tutorial must state the limits of the order that it uses, with one reason for each limit.

## Source rendering artifacts

- The image shows the LaTeX control word `\quad` after the semicolon of statement line 2.
- The control word is a rendering artifact of the web page, and it is not part of the statement.
- The radical bar of the density covers both terms. The density is $\sqrt{x^{2} + y^{2}}$, not $\sqrt{x^{2}} + y^{2}$.

## Workspace layout for the tutorial

- `problem/problem.md` holds this normalized statement.
- `problem/source/problem.png` holds the unchanged source image.
- `steps/` will hold one markdown file for each step.
- `code/` will hold one Python verification script for each part and the figure scripts.
- `code/figures/` holds the rendered figures.
- `code/outputs/` holds the printed check tables of the verification scripts.
- `tutorial.html` will hold the composed tutorial.

## Plan of the tutorial parts

The plan gives the title of each part. The intake stage gives no limit, no shape, and no value.

- **Part 1. The solid.** Read the three surfaces and derive the limits of the solid from them.
- **Part 2. Cross sections.** Name the shape of a section at a fixed $z$ and at a fixed $y$.
- **Part 3. The mass of (a).** Set up the integral of the density over the solid.
- **Part 4. The center of mass of (b).** Set up the three first-moment integrals and the division by the mass.
- **Part 5. The moment of inertia of (c).** Set up the integral of the squared distance from the $z$-axis.
- **Part 6. The check layer.** Compare the orders of integration and state the answer.
