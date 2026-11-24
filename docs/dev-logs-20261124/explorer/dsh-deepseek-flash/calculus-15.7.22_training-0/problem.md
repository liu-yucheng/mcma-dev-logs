# Volume of a Solid Bounded by a Circular Cylinder and Two Planes

## Source

- Source file: `problem/source/problem.png`.
- The image is a screenshot of an exercise page. The navigation line of the page gives the origin:
  `Home > Calculus, Early Transcendentals > 15.7 Triple Integrals > Exercise: 22`.
- The page belongs to section 15.7, "Triple Integrals", of the textbook *Calculus: Early
  Transcendentals*. The exercise number is 22.
- The image has a width of 985 px and a height of 199 px. The format is PNG. The bit depth is 8,
  and the color type is 6, which is RGBA. The file size is 10906 bytes.
- The source file is an unchanged copy of
  `mcma-dataset-20261124/training/problems/calculus-15.7.22/problem.png`. The MD5 checksum of the
  copy is `6053af2d4f660e277c21e49eb7db3b35`, and the checksum of the dataset file is the same
  value.

## Statement

The statement below is a quotation of the exercise text in the source image. The text keeps its
original words and its original punctuation.

> Use a triple integral to find the volume of the given solid.
> The solid enclosed by the cylinder x^2 + z^2 = 4 and the planes y = -1 and y + z = 4

## Given data

| Fact | Value | Source |
| --- | --- | --- |
| Method that the exercise requires | A triple integral | Statement, first sentence |
| Cylinder that bounds the solid | `x^2 + z^2 = 4` | Statement, second sentence |
| First plane that bounds the solid | `y = -1` | Statement, second sentence |
| Second plane that bounds the solid | `y + z = 4` | Statement, second sentence |
| Solid | The region that the three surfaces enclose | Statement, second sentence |

The exercise gives no length as a separate number. The three equations above fix the solid. The
constant `4` in the cylinder equation, and the constants `-1` and `4` in the plane equations, are
the only numeric data.

## Quantity that the problem asks for

- The volume `V` of the solid, in cubic units.
- The exercise fixes the method: the volume must come from one triple integral.

## Reading of the three surfaces

The four lines below record the form of each equation. They are a reading of the given data, and
they are not a solution step.

- The equation `x^2 + z^2 = 4` contains no term in `y`. Thus the surface is a circular cylinder,
  and its axis is the `y` axis. The surface limits the solid in the `x` direction and in the `z`
  direction. It gives no bound in `y` by itself.
- The equation `y = -1` contains no term in `x` and no term in `z`. Thus the surface is a plane
  with the normal vector `(0, 1, 0)`. It gives one bound in `y`.
- The equation `y + z = 4` contains no term in `x`. Thus the surface is a plane with the normal
  vector `(0, 1, 1)`. It gives the other bound in `y`.
- The two planes are not parallel, because their normal vectors differ. Thus the solid is not a
  prism between two parallel planes, and the thickness of the solid in the `y` direction changes
  with `z`.

## Work that this stage does not do

- This stage does not solve the problem. It states no bound of integration, no order of
  integration, no cross-section, and no volume.
- The tutoring stage must derive each of these quantities from the three equations above. A
  cross-section must come from the inequalities that the three surfaces define, and not from the
  shape of a figure.
- The two planes are not parallel. Thus a slice at a fixed value of one variable can have a shape
  that differs from the circle of the cylinder. The tutoring stage must derive the shape of every
  slice from the inequalities, and it must sample the area of the slice at three heights.

## Items for the tutoring stage

1. Identify the region in three-dimensional space that the three surfaces enclose.
2. Select an order of integration, and derive each bound from the three equations.
3. Derive the shape and the area of the cross-section at a fixed value of the outer variable.
   Sample the area at three heights with a script, and compare the sample with the integral of the
   area.
4. Evaluate the triple integral, and check the value with an independent computation.

## Files of this stage

| Path | Content |
| --- | --- |
| `problem/problem.md` | This file: the statement, the given data, the asked quantity, and the source of each fact |
| `problem/source/problem.png` | Unchanged copy of the source image |
