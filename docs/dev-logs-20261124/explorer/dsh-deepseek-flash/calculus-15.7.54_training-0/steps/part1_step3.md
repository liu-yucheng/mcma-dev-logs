## Part 1, Step 3: read the shape of each horizontal section

**Goal.** Decide the shape of the section at a fixed height $z$, because the volume and the integral both use that shape.

**Reason.** Fix a height $z$ between $0$ and $1$. A point of the section keeps that $z$ and must satisfy the two inequalities of Step 1 that involve $x$ and $y$. The second inequality, $z \leq 1 - x^2 - y^2$, becomes a disk condition, and the first inequality, $0 \leq z$, is already true for the fixed height.

**Computation.** For $0 \leq z \leq 1$ the section is $\{(x, y) : x^2 + y^2 \leq 1 - z\}$. This is a disk of radius $\sqrt{1 - z}$ and of area $\pi (1 - z)$. At $z = 1$ the disk shrinks to the single point $(0, 0)$. At a height above $1$ the section is empty. In the section at $y = 0$, the section at height $z$ appears as a chord from $x = -\sqrt{1 - z}$ to $x = \sqrt{1 - z}$, and Figure 2 draws three such chords.

**Result.** Each horizontal section is a disk, not an annulus, and its area is $\pi (1 - z)$. The area falls from $\pi$ at $z = 0$ to $0$ at $z = 1$, and the largest area is $\pi$.

**Verification.** The check `[[check:part1:section_shapes]]` reports the shape at five radii $r$ of the rim. The four values $r^2 = 0$, $0.25$, $0.75$, $1$ give the shape "segment" with the printed corner list $(0.0,\ 1 - r^2)$, the value $r^2 = 1.44$ gives "empty", and the value $r^2 = 1$ gives "point". The check `[[check:part2:slice_areas]]` compares the closed form $\pi (1 - z)$ with a grid count of the disk at $z = 0$, $0.5$, $0.8$.

FIGURE: part2_figure1.png | The section of $E$ at $y = 0$. The three horizontal chords are the diameters of the sections at $z = 0.25$, $z = 0.5$, and $z = 0.75$; the dashed lines mark the half width $\sqrt{1 - z}$ of the middle chord.
**Common mistake.** A reader may take each horizontal section for an annulus, because the side wall of a bowl often reads as a ring. The inequalities give $x^2 + y^2 \leq 1 - z$, which is one closed disk around the axis; an annulus would need a lower bound of the form $x^2 + y^2 \geq a(z)$ with $a(z) > 0$, and no such bound occurs.
