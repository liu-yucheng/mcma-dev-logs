# Part 4, Step 2: Check the drawing against the limits, and state the answer

## The reason

A drawing can look right and be wrong. The drawing is a set of triangles, so every claim about it
can be measured: a volume, an area, a cut, a projection. Each measurement is compared with a value
that the limits give. The answer of the exercise is the drawing that survives these comparisons.

## The computation

The drawing is a mesh of 15840 triangles, built from the five patches on a grid of 40 subdivisions
in each parameter direction. A triangle of zero area is dropped, because the collapse at $y = 2$
produces such triangles.

**The mesh is closed.** Each edge of the mesh belongs to two triangles. The count of edges that
belong to one triangle is $0$.

**The volume agrees.** The divergence theorem on the closed mesh gives the volume $6.665833$. The
integral of the cut area from Part 2, Step 2 gives $6.666667$. The iterated integral of the problem
gives $6.666667$. The relative gap of the mesh value and the cut value is $1.25\times10^{-4}$.

**The areas agree.** The drawn area of each patch and the integral of Part 3, Step 1 give the same
value within $1.56\times10^{-4}$ in relative terms.

**The cuts agree.** The drawn mesh is cut at the three heights $0.51$, $1.01$, and $1.51$. Each
height lies between two rows of the mesh, so each crossing point comes from an interpolation and
not from a point that the parameter map placed there. The measured areas are $5.571855$,
$2.949705$, and $0.842555$. The limits give $5.572451$, $2.950101$, and $0.842751$. The largest
relative gap is $2.33\times10^{-4}$.

**The projection agrees.** The projection of the solid on the plane $x = 0$ is the rectangle
$[0,4] \times [0,2]$. A sample of 200000 points of that rectangle all reach the solid, so the
fraction is $1$. The area of the rectangle outside the disk $x^{2} + z^{2} \le 4$ is $4.841080$,
so the projection is not a disk.

The volume $20/3$ appears in this part only as a check. The exercise asks for a sketch of the
solid. It asks for no number and no evaluation of the integral. The answer is the drawing.

## The result

The answer to the exercise is the sketch of the solid: the body in the box
$[0,4] \times [0,2] \times [0,2]$, closed by the five patches $y = 0$, $x = 0$, $z = 0$,
$y + z = 2$, and $x = 4-y^{2}$, with the five corners $A$, $B$, $C$, $D$, $T$, and a cut that is a
rectangle at every height below $y = 2$. Every measurement of the drawing agrees with the limits.

## The check

`code/part4_verify.py`, sections "volume", "areas", "cuts", "projection", and "labels". Each
section computes its value two ways and asserts the gap. The script prints the computed value and
the expected value of every row, and it stops with an assertion error when a gap is too large.
