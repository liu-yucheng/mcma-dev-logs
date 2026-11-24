# Part 1, Step 4: the volume from the sections

**Reason.** The volume is the integral of the section area over the height. The section exists only where
$1-3z^{2}$ is not negative, so the height runs from $-1/\sqrt{3}$ to $1/\sqrt{3}$. This step tests the semi-axes
of Step 2 with a second method, and it fixes the integration limits that Part 3 uses again.

A reader may take the height limit as 1, but the limits give $1/\sqrt{3}$, because the inequality
$1-3z^{2}\ge 0$ gives $|z|\le 1/\sqrt{3}$.

**Computation.** Integrate the section area over the height.

$$V=\int_{-1/\sqrt{3}}^{1/\sqrt{3}}\frac{\pi}{\sqrt{2}}(1-3z^{2})\,dz =\frac{\pi}{\sqrt{2}}\left[z-z^{3}\right]_{-1/\sqrt{3}}^{1/\sqrt{3}} =\frac{\pi}{\sqrt{2}}\cdot\frac{4}{3\sqrt{3}}=\frac{4\pi}{3\sqrt{6}}.$$

**Result.** The volume from the sections is {{part1.volume_from_sections}}, and the closed form of Step 2 gives
{{part1.ellipsoid_volume}}. The two values agree to the printed digits.

**Verification.** `code/part1_verify.py` computes the section integral by quadrature and compares it with the
closed form. The check `volume_closed_form_against_sections` prints {{part1.volume_from_sections}} against
{{part1.ellipsoid_volume}}. The check `section_0.4_half_width_x_against_formula` prints the half width
{{part1.section_rows.2.semi_x}} against the formula value {{part1.section_rows.2.semi_x}}, so the section that
this step integrates is the section that Step 3 measures.
