# Solid Enclosed by Two Paraboloids

## Problem statement

The problem is exercise 14 of section 15.8 of *Calculus, Early Transcendentals*.
The breadcrumb of the page reads "Calculus, Early Transcendentals > 15.8 Triple Integrals in
Cylindrical Coordinates > Exercise: 14".
The page gives one instruction and no other text.
The instruction reads:

> Use a graphing device to draw the solid enclosed by the paraboloids $z = x^{2} + y^{2}$ and
> $z = 5 - x^{2} - y^{2}$.

## Given data

Each row of the table quotes the statement line of `problem/source/problem.png`.
The table gives no other source, because the page holds no other mathematical line.

| Item | Value | Source |
| --- | --- | --- |
| Lower boundary surface | the paraboloid $z = x^{2} + y^{2}$ | statement line |
| Upper boundary surface | the paraboloid $z = 5 - x^{2} - y^{2}$ | statement line |
| Constant of the upper surface | $5$ | statement line |
| Number of boundary surfaces | two, because the page writes "paraboloids" in the plural | statement line |
| Relation between the surfaces | the two surfaces together enclose the solid | statement line |
| Asked instrument | a graphing device | statement line |
| Textbook location | section 15.8, exercise 14 | breadcrumb line |

The page gives no numeric data other than the constant $5$.
The page gives no interval for $x$, no interval for $y$, and no interval for $z$.
The page names no volume, no area, and no integral.

## Quantity that the problem asks for

The problem asks for one drawing: a picture of the solid that the two paraboloids enclose.
The problem asks for no number.
A complete answer holds three items:

1. the inequality description of the solid, which the page does not give and the tutorial derives;
2. the drawn solid, which shows both boundary surfaces, the closed body, and the curve where the two
   surfaces meet;
3. a scale on each axis, because a reader must read the extent of the solid from the drawing.

The word "enclosed" fixes the solid as the bounded body between the two surfaces.
A drawing of one paraboloid alone does not answer the problem.
A drawing of the two surfaces without the body between them does not answer the problem.

## Facts that the page fixes and facts that the tutorial must derive

The page fixes the two boundary surfaces and the instruction to draw.
The page does not fix the following items, and the tutorial derives each one:

- the shape of each paraboloid and the direction in which each one opens;
- the curve where the two surfaces meet;
- the projection of the solid on the plane $z = 0$;
- the inequality description of the solid;
- the vertical extent of the solid;
- the scale of the drawing;
- the check that a drawn point lies on the surface that its label names.

## Conventions of this tutorial

- The solid is a closed body, so each boundary surface belongs to the solid.
  The boundary does not change a volume or an integral, but the tutorial states the limits as closed
  inequalities and the reader may check the boundary separately.
- The symbol $E$ names the solid.
- A figure illustrates the solid, but a figure does not define the solid.
  Every geometric claim starts from the two surface equations, and the drawing follows the claim.
- The graphing device of this tutorial is a Python script under `code/`.
  The tutorial records the version of each tool and the random seed that a reported result uses.
- Every numerical claim has a check in one Python file under `code/`.
  The tutorial cites the file and the line range of the check beside the claim.
- A check compares a value that one method computes with a value that a different method computes.
  A comparison of a value with itself does not check a claim.

## Planned parts

The tutorial divides the work into five parts.
Each part contains short steps that a reader can check by hand.

| Part | Subject | Reason for the position of the part |
| --- | --- | --- |
| Part 1 | the two paraboloids and their meeting curve | the meeting curve fixes the outline of the solid |
| Part 2 | the projection of the solid on the plane $z = 0$ | the projection fixes the horizontal extent |
| Part 3 | the inequality description and the vertical extent | the description fixes the solid of the drawing |
| Part 4 | the drawing of the solid, with a scale on each axis | the drawing is the answer that the page asks for |
| Part 5 | the checks of the drawing and a summary | one place compares the picture with the description |

Part 1 must come first, because the meeting curve fixes the widest horizontal section of the solid.
Part 2 follows Part 1, because the projection is the region inside that curve.
Part 3 follows Part 2, because the vertical extent holds above each point of the projection.
Part 4 follows Part 3, because a drawing that comes before the description can show a wrong body, and
a reader cannot detect the error from the picture alone.
Part 5 repeats every geometric claim against one independent computation.

## Source files

| File | Role | State |
| --- | --- | --- |
| `problem/source/problem.png` | the only source of the statement | an unchanged copy, 984 by 178 pixels |

The dataset path of the file is
`mcma-dataset-20261124/training/problems/calculus-15.8.14/problem.png`.
The copy in `problem/source/` holds the same bytes as the dataset file, and the SHA-256 digest of
both files is
`6cfb31fc0b8a39a4c83c9b9ebbce14558976693f8b80fef6b5322ecb9a3610b8`.
The page holds a breadcrumb line, a bookmark button, and one statement line.
The statement line is the only line with mathematical content.
