# Triple integral over a paraboloid region

## Statement

Evaluate the triple integral

$$\iiint_E x \, dV,$$

where $E$ is the solid region bounded by the paraboloid $x = 4y^{2} + 4z^{2}$ and the plane $x = 4$.

Source: the screenshot `problem/source/problem.png` shows this statement without a change.

## Given data

| Item | Value | Source of the fact |
| --- | --- | --- |
| Integrand | $f(x, y, z) = x$ | `problem/source/problem.png`, line of the integral |
| First boundary surface | Paraboloid $x = 4y^{2} + 4z^{2}$ | `problem/source/problem.png`, text after "where $E$ is bounded by" |
| Second boundary surface | Plane $x = 4$ | `problem/source/problem.png`, text after "and the plane" |
| Integration region | The solid $E$ that the two surfaces bound | `problem/source/problem.png` |
| Differential | Volume element $dV$ in space | `problem/source/problem.png`, symbol $dV$ |
| Textbook location | Calculus: Early Transcendentals, section 15.7, exercise 17 | Page header of `problem/source/problem.png` |

## Quantity that the problem asks for

One number: the value of the triple integral $\iiint_E x \, dV$.

The problem gives no numerical answer and no intermediate value. The tutorial stage must compute the value and must check it.

## Notes on the region

The paraboloid $x = 4y^{2} + 4z^{2}$ opens along the positive $x$ axis. Its vertex is the origin. The plane $x = 4$ is parallel to the $yz$ plane.

The region $E$ is the solid between the two surfaces. The paraboloid is the curved boundary. The plane is the flat boundary.

## Normalized notation

| Symbol | Meaning |
| --- | --- |
| $x, y, z$ | Cartesian coordinates of a point of space |
| $E$ | The solid region of integration |
| $dV$ | Volume element, equal to $dx \, dy \, dz$ in Cartesian order |
| $\iiint_E$ | Triple integral over the region $E$ |

## Source files

| File | Role | Check |
| --- | --- | --- |
| `problem/source/problem.png` | The only source file. It holds the statement as an image. | SHA-256 `dd444e9e598a03f084b862fc0f018bf3e06763868d6f6cce23540e7dc6714226`, 11540 bytes, identical to the dataset file `calculus-15.7.17/problem.png` |

The source directory holds a byte-identical copy of the dataset file. No edit changed the image.
