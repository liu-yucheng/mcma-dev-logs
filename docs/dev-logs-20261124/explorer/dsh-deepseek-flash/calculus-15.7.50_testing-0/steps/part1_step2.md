## Step 1.2 — Read the section at a fixed $y$ and the projection on the plane $x = 0$

**Reason.** The middle and inner limits must describe a plane figure at a fixed $y$, because the outer integral adds these figures. A reader may take the section for a circular annulus, but the limits $0 \le x \le y / 3$ and $0 \le z \le \sqrt{9 - y^{2}}$ give a rectangle, because $x$ and $z$ vary independently for a fixed $y$. The corners of that rectangle are the four points where the two bounds meet.

**Computation.** For a fixed $y$ the corner list is $(0, y, 0)$, $(y/3, y, 0)$, $(y/3, y, \sqrt{9 - y^{2}})$, and $(0, y, \sqrt{9 - y^{2}})$. The width is $y / 3$ and the height is $\sqrt{9 - y^{2}}$, so the area is

$$ A(y) = \frac{y}{3}\sqrt{9 - y^{2}}. $$

The projection of the solid on the plane $x = 0$ drops $x$ and keeps the disc $y^{2} + z^{2} \le 9$ in the first quadrant, whose area is $9\pi/4$.

**Verification.** `code/part1_verify.py` builds the corner list for each value of $y$ and counts the distinct corners, and it compares that count with the shape that the edge lengths give. The printed rows are

{{table:shapes}}

The script also computes $A({{section_y|3}})$ as the product of width and height, which prints ${{section_area|6}}$, and as the difference of two cumulative volumes, which prints ${{section_area_difference|6}}$. The projection area prints ${{projection_area|6}}$ from a quadrature over the disc and from a Simpson rule in the angle, and ${{projection_area_closed_form|6}}$ from the closed form $9\pi/4$.

**Result.** At $y = {{section_y|3}}$ the section is a rectangle of width ${{section_width|3}}$ and height ${{section_height|3}}$, and its area is ${{section_area|3}}$. At $y = 0$ and at $y = 3$ the rectangle collapses to a segment, which the printed row list shows as two distinct corners. Figure 2 draws the projection on the plane $x = 0$ and the section at $y = {{section_y|3}}$.

{{figure:part1_figure2|Left: the projection of the solid on the plane $x = 0$, which is the quarter disc, with the strip at $y = {{section_y|3}}$. Right: the section at $y = {{section_y|3}}$, which is the rectangle of width ${{section_width|3}}$ and height ${{section_height|3}}$.}}
