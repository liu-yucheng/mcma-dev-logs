# Part 1, Step 2: the boundary is an ellipsoid with three semi-axes

**Reason.** The boundary $x^{2}+2y^{2}+3z^{2}=1$ meets each coordinate axis in one point. The distances from the
origin to those three points are the semi-axes, and the lengths of the three axes fix the shape of the body and
the volume. The figure shows the body and the section at one fixed height.

A reader may take the coefficient 2 as the semi-axis of $y$, but the limits give a semi-axis $\sqrt{1/2}$,
because the intersection with the $y$ axis solves $2y^{2}=1$.

**Computation.** Set two coordinates to zero in turn.

$$x\text{ axis: }x^{2}=1\Rightarrow a=1,\qquad y\text{ axis: }2y^{2}=1\Rightarrow b=\frac{1}{\sqrt{2}},\qquad z\text{ axis: }3z^{2}=1\Rightarrow c=\frac{1}{\sqrt{3}}.$$

The volume of an ellipsoid with semi-axes $a$, $b$, and $c$ is $\frac{4}{3}\pi a b c$. With these values the
volume is

$$V=\frac{4}{3}\pi\cdot 1\cdot\frac{1}{\sqrt{2}}\cdot\frac{1}{\sqrt{3}}=\frac{4\pi}{3\sqrt{6}} ={{part1.ellipsoid_volume}}.$$

**Result.** The body has the semi-axes {{part1.semi_axis_x}}, {{part1.semi_axis_y}}, and
{{part1.semi_axis_z}}, and its volume is {{part1.ellipsoid_volume}}. Figure 1 shows the body, the three axis
arrows, and the section at $z=0.4$.

[[figure:part1_figure1|Figure 1. The ellipsoid $P:x^{2}+2y^{2}+3z^{2}\le 1$ with the section at $z=0.4$ in orange.]]

**Verification.** `code/part1_verify.py` locates each axis point by a root search and compares it with the
formula. The check `semi_axis_x_by_root_finding` prints {{part1.semi_axis_x}} against {{part1.semi_axis_x}},
and the check `volume_closed_form_against_sections` prints {{part1.volume_from_sections}} against
{{part1.ellipsoid_volume}}. The script `code/part1_figure1.py` draws Figure 1 and checks that each axis letter
stays clear of the drawn body.
