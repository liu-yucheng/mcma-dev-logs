# Step 1.3: fix one coordinate and read the shape of the section

## Reason

A section is the solid cut by one plane of constant coordinate. Fix $y$ and the remaining conditions give a region in the plane of that $y$. The shape of that region decides which integration order is easy, so read it from the inequalities and not from a picture of the cylinder.

A reader may call the section at a fixed $z$ an annulus because the cylinder is round, but the conditions give a triangle, because $x$ runs from $0$ to $y/3$ for every $y$ that the disk allows.

## Computation

Fix $y$. The condition $y^{2} + z^{2} \le 9$ gives $0 \le z \le \sqrt{9 - y^{2}}$, and the condition $y \ge 3x$ gives $0 \le x \le \dfrac{y}{3}$. The section is a rectangle with the area $\dfrac{y}{3}\sqrt{9 - y^{2}}$.

Fix $z$. The cylinder gives $0 \le y \le \sqrt{9 - z^{2}}$, and the condition $y \ge 3x$ gives $0 \le x \le \dfrac{y}{3}$. The section is the triangle with the corners $(0, 0)$, $\left(0, \sqrt{9 - z^{2}}\right)$ and $\left(\dfrac{\sqrt{9 - z^{2}}}{3}, \sqrt{9 - z^{2}}\right)$, and its area is $\dfrac{9 - z^{2}}{6}$.

## Result

At $y = {{p2_demo_height}}$ the section is a {{p1_slice_y_kind}} with the area ${{p1_slice_y_area}}$. At $z = {{p2_demo_height}}$ the section is a {{p1_slice_z_kind}} with the area ${{p1_slice_z_area}}$. At the ends of the range the section loses a dimension: at $y = 0$ it is a {{p1_end_y0_kind}}, at $y = 3$ it is a {{p1_end_y3_kind}} and at $z = 3$ it is a {{p1_end_z3_kind}}, as the corner list of `code/part1_verify.py` reports. Figure 3 shows the two sections at the height ${{p2_demo_height}}$.

## Verification

`code/part1_verify.py` builds the corner list of every section from the inequalities and classifies the list as a point, a segment, a triangle or a rectangle. It counts the area of each section on a grid and compares the count with the closed form, with a relative gap below $8.0\times 10^{-3}$.
