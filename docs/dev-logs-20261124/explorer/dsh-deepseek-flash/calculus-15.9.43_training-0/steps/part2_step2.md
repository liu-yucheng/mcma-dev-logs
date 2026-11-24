# Part 2, Step 2: The area of the section as a function of the height

## Reason

The area function collects the whole shape into one curve. Once the curve is known, the volume
is an integral of one variable, and the drawing of the silo follows the same curve, because the
silhouette of the body is the outline of the widest section at each height.

## Computation

Square the radius of Step 2.1 and multiply by $\pi$. On the lower branch the area does not
depend on $z$:

$$A(z)=\pi\cdot 9=9\pi,\qquad 0\le z\le 10 .$$

On the upper branch, write $u=z-10$ and square the second radius:

$$A(z)=\pi\bigl(9-(z-10)^{2}\bigr),\qquad 10\le z\le 13 .$$

At $z=10$ both branches give $9\pi$, so the curve is continuous. At $z=13$ the second branch
gives $0$, so the curve reaches the top of the cap.

## Result

$$A(z)=\begin{cases}9\pi, & 0\le z\le 10,\\ \pi\bigl(9-(z-10)^{2}\bigr), & 10\le z\le 13 .\end{cases}$$

The largest area is $9\pi=28.2743338823$ on the whole lower branch, and the area at the height
$11.5$ is $21.205750412$. The curve of Figure 2, drawn by `code/part2_figure1.py`, has these
two branches and marks the heights $3$, $10$, and $11.5$.

## Common mistake

A reader may take the area to fall from the lowest height, but the lower branch is constant; the
two marked heights $3$ and $10$ give the same area $28.274333882$, as the print of
`code/part2_figure1.py` shows.

## Verification

Verification script: `code/part2_verify.py` check C2 compares the formula with the shoelace area of a 720-vertex
polygon whose vertices are the bisected radii, at the heights $3$, $10$, and $11.5$, and prints
a largest difference of $3.589\times 10^{-4}$; the polygon is inscribed, so the small
underestimate is expected. Check C3 compares the area just below $z=10$ with the area just above
and prints $28.2743338823$ against $28.2743338823$, so the two branches meet. Figure 2 is drawn
by `code/part2_figure1.py`, which asserts that each legend and each annotation stays inside its
axes box before it writes the file.
