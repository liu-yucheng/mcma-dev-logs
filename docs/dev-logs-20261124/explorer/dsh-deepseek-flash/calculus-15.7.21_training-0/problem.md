# Volume of a Solid Bounded by a Parabolic Cylinder and Two Planes

## Source

- Source file: `problem/source/problem.png`.
- The image is a screenshot of an exercise page. The navigation line of the page gives the origin:
  `Home > Calculus, Early Transcendentals > 15.7 Triple Integrals > Exercise: 21`.
- The page belongs to section 15.7, "Triple Integrals", of the textbook *Calculus: Early
  Transcendentals*. The exercise number is 21.
- The image has a width of 985 px and a height of 203 px. The format is PNG with an RGBA color
  model.
- The source file is an unchanged copy of
  `mcma-dataset-20261124/training/problems/calculus-15.7.21/problem.png`. The MD5 checksum of the
  copy is `e8abbec39c8ba7a1814f4a624f176829`, and the checksum of the dataset file is the same
  value.

## Statement

The statement below is a quotation of the exercise text in the source image. The text keeps its
original words and its original punctuation.

> Use a triple integral to find the volume of the given solid.
> The solid enclosed by the cylinder y = x^2 and the planes z = 0 and y + z = 1

## Given data

| Fact | Value | Source |
| --- | --- | --- |
| Method that the exercise requires | A triple integral | Statement, first sentence |
| Cylinder that bounds the solid | `y = x^2` | Statement, second sentence |
| First plane that bounds the solid | `z = 0` | Statement, second sentence |
| Second plane that bounds the solid | `y + z = 1` | Statement, second sentence |
| Solid | The region that the three surfaces enclose | Statement, second sentence |

The exercise gives no numeric value for a length. The solid is fully specified by the three
equations above.

## Quantity that the problem asks for

- The volume `V` of the solid, in cubic units.
- The exercise fixes the method: the volume must come from one triple integral.

## Reading of the three surfaces

The three lines below record the form of each equation. They are a reading of the given data, and
they are not a solution step.

- The equation `y = x^2` contains no term in `z`. Thus the surface is a parabolic cylinder, and its
  rulings are parallel to the `z` axis. The surface is a boundary of the solid in the `x` direction
  and in the `y` direction, and it does not limit the solid in the `z` direction by itself.
- The equation `z = 0` is the `xy` plane. It is a horizontal boundary of the solid.
- The equation `y + z = 1` is a plane. It is the second horizontal boundary of the solid.

## Work that this stage does not do

- This stage does not solve the problem. It states no bound of integration, no order of
  integration, no cross-section, and no volume.
- The tutoring stage must derive each of these quantities from the three equations above. A
  cross-section must come from the inequalities that the three surfaces define, and not from the
  shape of a figure.

## Items for the tutoring stage

1. Identify the region in three-dimensional space that the three surfaces enclose.
2. Select an order of integration, and derive each bound from the three equations.
3. Derive the shape and the area of the cross-section at a fixed value of the outer variable.
4. Evaluate the triple integral, and check the value with an independent computation.

## Files of this stage

| Path | Content |
| --- | --- |
| `problem/problem.md` | This file: the statement, the given data, the asked quantity, and the source of each fact |
| `problem/source/problem.png` | Unchanged copy of the source image |
