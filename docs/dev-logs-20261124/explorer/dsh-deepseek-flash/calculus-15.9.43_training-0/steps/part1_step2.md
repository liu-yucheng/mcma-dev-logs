# Part 1, Step 2: The ceiling and the three faces of the body

## Reason

Every point of the body lies below one surface, and that surface decides the upper limit of
every integral that follows. The drawing also needs the exact list of faces, because a surface
that a reader sees in a picture is not always a face of the solid: the plane $z=10$ looks like a
face in a sketch, but the body continues through it.

## Computation

Take a point above the lower face, at distance $r$ from the vertical axis, with $r\le 3$. The
cylinder allows every height up to $10$. The cap allows every height above $10$ that satisfies
$(z-10)^{2}\le 9-r^{2}$, that is $z\le 10+\sqrt{9-r^{2}}$. The two bounds fit together at
$z=10$, so the ceiling of the body at that radius is

$$Z(r)=10+\sqrt{9-r^{2}},\qquad 0\le r\le 3 .$$

Now take a point of the disk $r<3$ in the plane $z=10$. Its distance from the cap center is
$r<3$, so a small ball about that point lies inside the cap, and the same ball lies inside the
cylinder. That point is an interior point, not a point of the boundary.

## Result

The body is the set

$$0\le r\le 3,\qquad 0\le z\le 10+\sqrt{9-r^{2}} .$$

The boundary has exactly three faces: the lower disk $z=0$ with $r\le 3$; the lateral faces
$r=3$ with $0\le z\le 10$; and the cap, the part of the sphere of radius $3$ about $(0,0,10)$
with $z\ge 10$. The disk at $z=10$ is interior. The rim circle $r=3$, $z=10$ is the common edge
of the lateral face and the cap. Figure 1 marks the three faces, and each mark sits on the
surface that it names.

## Common mistake

A reader may take the plane $z=10$ as a fourth face, but the membership test puts every point of
that disk with $r<3$ inside the solid; the boundary keeps three faces.

## Verification

Verification script: `code/part1_verify.py` check C9 samples 400 points at distance 0.4 about the point
$(1.6\cos 145^{\circ},1.6\sin 145^{\circ},10)$ and prints 0 points outside the body. Check C11
steps 72 times outward from each face and 72 times inward and prints 0 failures. Checks C2 and
C3 put a parametric point of the lateral face and of the cap against its own equation and print
residuals $3.553\times 10^{-15}$ and $8.882\times 10^{-15}$. Check C10 measures the lower disk
with the shoelace rule of 720 rim points and prints 28.2739750147 against
$\pi R^{2}=28.2743338823$; the polygon is inscribed, so a difference of
$3.589\times 10^{-4}$ is expected and the check allows it.
