# Part 1, Step 1: Put a frame on the silo

## Reason

A drawing needs a frame, and every later integral needs coordinates. The statement gives one
radius and one height, so the frame should hide no symmetry: put the flat face in a horizontal
plane and the axis of the cylinder on the vertical axis. Then the circular symmetry of the body
becomes a symmetry in one variable only.

## Computation

Place the origin at the center of the lower face. Let the $z$ axis run up the axis of the
cylinder, and let the $x$ axis and the $y$ axis lie in the plane of the lower face. Write
$r=\sqrt{x^{2}+y^{2}}$ for the distance from the vertical axis.

The cylinder of radius $3$ and height $10$ is the set of points with

$$x^{2}+y^{2}\le 9,\qquad 0\le z\le 10 .$$

The hemisphere sits on the top face of the cylinder, so its center is $(0,0,10)$ and its radius
is $3$. The silo is the union of that cylinder and that hemisphere:

$$x^{2}+y^{2}\le 9,\quad 0\le z\le 10 ;\qquad x^{2}+y^{2}+(z-10)^{2}\le 9,\quad z\ge 10 .$$

## Result

The body is the union of the two sets above. Its highest point is the top of the cap,
$(0,0,13)$, and the rim where the cap meets the cylinder is the circle $r=3$ in the plane
$z=10$. See Figure 1 for the frame and the two pieces.

## Common mistake

A reader may take the cap to be a full sphere, but the inequality $z\ge 10$ keeps only the
upper half; a full sphere would add the volume $18\pi$ a second time.

## Verification

Verification script: `code/part1_verify.py` check C1 compares the ceiling that the union gives with a direct
membership test on 11163 points and prints the number of disagreements as 0. Check C12
compares the highest point of the union $10+3$ with the largest sampled height of the cap and
prints 13 against 13. Check C5 compares a point of the cap at $\varphi=\pi/2$ with a point of
the cylinder at $z=10$ and prints 0 for their distance, so the two pieces meet.
