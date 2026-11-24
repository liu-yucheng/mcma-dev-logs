## Step 4.1 - Draw the closed body

**Reason.** The problem asks for a drawing of the solid, so the drawing itself is the answer.
A reader must see three things at once: the closed body between the two surfaces, the circle where the surfaces meet, and one scale on each axis.
The drawing code builds every surface from the two equations of Step 1.1, so the drawn shape follows the inequalities and not an outline copied by hand.

**Computation.** The drawing samples the lower surface at the heights $z = r^{2}$ and the upper surface at the heights $z = 5 - r^{2}$, over the footprint $r^{2} \le \frac{5}{2}$.
The meeting circle is sampled separately and drawn as a heavier curve on the rim of the body.
Each axis carries tick marks with numbers, and the three axis names sit at the tips of their own arrows.

**Result.** The check evaluates both drawn surfaces at every sampled point and compares the height with the height that its equation gives [scan [[check:part4:drawing_surface_residual]]].
The largest residual of the lower surface is $8.882 \times 10^{-16}$ and the largest residual of the upper surface is $8.882 \times 10^{-16}$.
The largest squared radius of a drawn point is $2.500000000$, the smallest is $0$, and the gap of the rim against $\frac{5}{2}$ is $8.882 \times 10^{-16}$.
The rim of the drawn body sits at the squared radius $2.500000000$ and at the height $2.500000000$ from a root search, and the drawn circle has the radius $1.581138830$ [scan [[check:part4:closed_body_rim]]].
Figure 3 is the drawing of the answer.

FIGURE: part4_figure1.png | Left: the closed body between the two paraboloids, with the meeting circle drawn heavy and one scale on each axis. Right: the same body cut by the plane $y = 0$, where the lens shape and the two meeting points appear without perspective. One grid step is one unit on each axis.

**Common mistake.** A reader may take the drawn outline for the whole of both paraboloids, but the body stops at the meeting circle, so the drawing shows the lower surface only inside the footprint and the upper surface only above it.
