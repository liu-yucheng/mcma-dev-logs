# Part 1, Step 3: the horizontal section at a fixed height

**Reason.** A section at a fixed number $z$ turns the three-dimensional region into a plane region, and the
plane area is easy to compute. The section comes from the defining inequality with $z$ held constant. It is an
ellipse, not a circle, because the coefficients of $x^{2}$ and $y^{2}$ differ.

A reader may take the section as a disk of radius $\sqrt{1-3z^{2}}$, but the limits give an ellipse with the
semi-axes $\sqrt{1-3z^{2}}$ and $\sqrt{(1-3z^{2})/2}$, because the coefficient 2 divides the second squared
coordinate.

**Computation.** Hold $z$ and read the inequality.

$$x^{2}+2y^{2}\le 1-3z^{2}\iff \frac{x^{2}}{1-3z^{2}}+\frac{y^{2}}{(1-3z^{2})/2}\le 1.$$

The area of an ellipse with semi-axes $a$ and $b$ is $\pi a b$, so the section area is

$$A(z)=\pi\sqrt{1-3z^{2}}\sqrt{\frac{1-3z^{2}}{2}}=\frac{\pi}{\sqrt{2}}\,(1-3z^{2}).$$

**Result.** At $z=0.4$ the semi-axes are {{part1.section_rows.2.semi_x}} and
{{part1.section_rows.2.semi_y}}, and the area is {{part1.section_rows.2.area_formula}}. Figure 2 shows this
section with its two semi-axes and with the equation that defines it.

[[figure:part1_figure2|Figure 2. The section of $P$ at $z=0.4$ with the semi-axes $a$ and $b$ and the equation $x^{2}+2y^{2}=1-3z^{2}$.]]

**Verification.** `code/part1_verify.py` compares the formula with a numerical quadrature and with a random
sample. The check `section_area_0.4_formula_against_quadrature` prints {{part1.section_rows.2.area_quadrature}}
against {{part1.section_rows.2.area_formula}}, and the check `section_area_0.4_formula_against_sample` prints
{{part1.section_rows.2.area_sample}} against the same formula. The script `code/part1_figure2.py` draws Figure 2
and checks that each label stays clear of the drawn curve.
