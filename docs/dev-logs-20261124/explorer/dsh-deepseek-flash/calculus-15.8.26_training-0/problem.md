# Problem 17: Volume Cut Out of a Sphere by a Cylinder

- Source image: `problem/source/problem.png`
- Source SHA-256: `6c5126c452dc1c16285c21ee1ace18fc3be5d47689742d7a190e724714e2166d`
- Image size: 979 by 214 pixels
- Provenance line in the image: `Home > Calculus, Early Transcendentals > 15.8 Triple Integrals in Cylindrical Coordinates > Exercise: 26`

## Statement

The problem gives one instruction and two parts. The text below is the normalized
form of the image text. The mathematical content is unchanged.

> Use cylindrical coordinates.
>
> (a) Find the volume of the solid that the cylinder $r = a \cos \theta$ cuts out of the
> sphere of radius $a$ centered at the origin.
>
> (b) Illustrate the solid of part (a) by graphing the sphere and the cylinder on the
> same screen.

## Given data

| Item | Given value | Meaning | Source of the fact |
| --- | --- | --- | --- |
| Coordinate system | Cylindrical coordinates $(r, \theta, z)$ | The instruction names the coordinate system to use. | `problem/source/problem.png`, line 1 of the statement |
| Cutting surface | Cylinder $r = a \cos \theta$ | The cylinder removes one region from the sphere. | `problem/source/problem.png`, part (a) |
| Body that is cut | Sphere of radius $a$ centered at the origin | The sphere is the body that loses the region. | `problem/source/problem.png`, part (a) |
| Radius symbol | $a$ | The symbol $a$ is the radius of the sphere. The image gives no numeric value. | `problem/source/problem.png`, part (a) |
| Angle range | $-\pi/2 \le \theta \le \pi/2$ | The right side $a \cos \theta$ is not negative in this range. | Derived from the given surface, not stated in the image. See the note below. |
| Second task | Graph the sphere and the cylinder on one screen | Part (b) asks for one figure that shows both surfaces. | `problem/source/problem.png`, part (b) |

## Requested quantity

1. Part (a): the volume $V$ of the solid that is inside the sphere $x^{2} + y^{2} + z^{2} \le a^{2}$
   and inside the cylinder $r \le a \cos \theta$. The answer is an expression in $a$, because
   the image gives no numeric value for $a$.
2. Part (b): one figure that shows the sphere and the cylinder together.

## Symbol table

| Symbol | Meaning |
| --- | --- |
| $a$ | Radius of the sphere. The image gives $a > 0$ only through the word "radius". |
| $r$ | Distance from the $z$-axis, $r = \sqrt{x^{2} + y^{2}}$. |
| $\theta$ | Angle in the $xy$-plane, measured from the positive $x$-axis. |
| $z$ | Height above the $xy$-plane. |
| $V$ | Volume of the solid of part (a). |

## Notes on the normalized statement

- The image writes the cylinder as `r = a cos θ`. The normalized form keeps this equation.
- The image gives no numeric value for $a$. Every result of this tutorial stays symbolic in $a$.
- The angle range is not printed in the image. It follows from the equation of the cylinder,
  because $r$ is a distance and $a \cos \theta$ must not be negative. The tutorial derives this
  range in its first part and does not take it as a given fact.

## Workspace state of this stage

- The intake stage normalizes the statement and copies the source file. It does not solve the
  problem and it does not grade a solution.
- The copy in `problem/source/problem.png` matches the dataset file byte for byte. The SHA-256
  value above is the value of both files.
