# Part 3, Step 2: spherical coordinates split the ball integral

**Reason.** On the unit ball the integrand depends on the radius only, so spherical coordinates separate the
integral into one angular factor and one radial integral. The angular factor is the area of the unit sphere and
does not depend on the problem, and the radial integral carries the whole answer.

A reader may take the angular factor as $\pi$, but the limits give $4\pi$, because the angular integral covers
the whole sphere and not a hemisphere.

**Computation.** With $u=r\sin\theta\cos\phi$, $v=r\sin\theta\sin\phi$, and $w=r\cos\theta$ the volume element is
$r^{2}\sin\theta\,dr\,d\theta\,d\phi$ and the integrand is $1-r^{2}$. Therefore

$$\iiint_{B}\left(1-r^{2}\right)dV=\left(\int_{0}^{2\pi}\int_{0}^{\pi}\sin\theta\,d\theta\,d\phi\right) \left(\int_{0}^{1}(1-r^{2})r^{2}\,dr\right).$$

The angular factor is $4\pi={{part3.angular_factor}}$. The radial integral is

$$\int_{0}^{1}\left(r^{2}-r^{4}\right)dr=\frac{1}{3}-\frac{1}{5}=\frac{2}{15} ={{part3.radial_factor}}.$$

**Result.** The angular factor is {{part3.angular_factor}} and the radial integral is
{{part3.radial_factor}}. The cumulative radial integral reaches
{{part3.cumulative_values.3}} at $r=1$, and its values at $r=0.25$, $0.5$, and $0.75$ are
{{part3.cumulative_values.0}}, {{part3.cumulative_values.1}}, and {{part3.cumulative_values.2}}.
Figure 3 shows the integrand and the cumulative integral.

[[figure:part3_figure1|Figure 3. The radial integrand $(1-r^{2})r^{2}$ and its cumulative integral, with the four sample radii marked.]]

**Verification.** `code/part3_verify.py` compares both factors with independent quadratures. The check
`angular_integral_against_four_pi` prints {{part3.angular_factor}} against $4\pi$, the check
`radial_integral_antiderivative_against_quadrature` prints {{part3.radial_factor}} against the quadrature value
{{part3.radial_factor}}, and the check `cumulative_radial_at_one` prints {{part3.cumulative_values.3}} against
{{part3.radial_factor}}. The script `code/part3_figure1.py` draws Figure 3 and checks that each label stays
clear of the drawn curve.
