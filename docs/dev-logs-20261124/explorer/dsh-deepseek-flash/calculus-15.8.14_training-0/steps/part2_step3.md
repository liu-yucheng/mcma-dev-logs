## Step 2.3 - Find the widest section and the meeting height

**Reason.** The widest section is the place where the drawing must show the rim of the body, so the drawing needs both its height and its area.
The area of Step 2.2 is one expression with two linear pieces, and the largest value sits where the two pieces meet.
The height of the widest section is therefore the meeting height of Step 1.2, and the width at that height follows from the same expression.

**Computation.** Write the area in its two pieces.

$$ A(z) = \pi z \ \text{for}\ 0 \le z \le \frac{5}{2}, \qquad A(z) = \pi (5 - z) \ \text{for}\ \frac{5}{2} \le z \le 5 $$

The first piece grows with $z$ and the second piece falls with $z$, so the largest value is at $z = \frac{5}{2}$.

$$ A\left(\frac{5}{2}\right) = \pi \frac{5}{2} = 7.853981634 $$

The widest section is the disk of radius $\sqrt{\frac{5}{2}}$ at the meeting height, and that disk is the projection of the meeting circle of Step 1.2.

**Result.** The check searches a fine grid of heights for the largest area and compares the result with the height where the two surfaces are equal [scan [[check:part2:widest_section]]].
The grid maximum is at $2.500000000$ and the equality of the two heights is at $2.500000000$, with a difference of $0$ against a tolerance of $10^{-4}$.
The area at that height from the integral of $2 \pi r$ is $7.853981633974$ against $\pi \frac{5}{2} = 7.853981633974$, with a difference of $2.665 \times 10^{-15}$.
Figure 2 shows the area curve and the three sections that the check samples.

FIGURE: part2_figure1.png | Left: the area $A(z) = \pi \min(z, 5 - z)$ of the horizontal section against its height, with the three sampled heights marked. Right: the sections at $z = 0.5$, $z = 2.5$ and $z = 4.5$, seen from above, with the rim circle $x^{2} + y^{2} = \frac{5}{2}$ dashed.

**Common mistake.** A reader may take the widest section for a section above the meeting height, because the drawn body looks wider near its top in a flat picture, but the area $\pi \min(z, 5 - z)$ is largest at $z = \frac{5}{2}$ and is smaller at every other height.

**Answer of Part 2.** The footprint on the plane $z = 0$ is the disk $x^{2} + y^{2} \le \frac{5}{2}$.
The section at height $z$ is a disk of area $\pi \min(z, 5 - z)$, and the widest section is the disk of area $\pi \frac{5}{2} = 7.853981634$ at $z = \frac{5}{2}$.
