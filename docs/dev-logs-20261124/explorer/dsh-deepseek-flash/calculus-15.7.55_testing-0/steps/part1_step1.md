# Part 1, Step 1: the sign of the integrand selects the region

**Reason.** The region $E$ is free and the integrand depends on the point only. A point where the integrand is
positive adds a positive amount when the point joins $E$. A point where the integrand is negative subtracts.
A region that holds a negative point loses value when that point leaves, and a region that omits a positive
point gains value when that point joins. Therefore the best region holds every positive point and no negative
point, and its boundary is the set where the integrand is zero.

A reader may take the boundary of the best region as free to move into the negative side, but the limits give a
boundary that is the zero set of the integrand, because every negative point lowers the value.

**Computation.** Write the quadratic form and the integrand.

$$Q(x,y,z)=x^{2}+2y^{2}+3z^{2},\qquad f(x,y,z)=1-Q(x,y,z).$$

The integrand is positive exactly when $Q<1$, zero exactly when $Q=1$, and negative exactly when $Q>1$.
The set $Q=1$ is a closed bounded surface, because $Q$ is a positive definite quadratic form. The positive part
is the interior of that surface, so the candidate region is

$$E^{*}=\{(x,y,z):x^{2}+2y^{2}+3z^{2}\le 1\}.$$

**Result.** The region that maximizes the integral is the solid ellipsoid $E^{*}$ bounded by
$x^{2}+2y^{2}+3z^{2}=1$. Its three semi-axes are
$a={{part1.semi_axis_x}}$, $b={{part1.semi_axis_y}}$, and $c={{part1.semi_axis_z}}$.

**Verification.** `code/part1_verify.py` checks the boundary residual on each axis and the sign split.
The check `semi_axis_y_by_root_finding` prints the root {{part1.semi_axis_y}} against the formula value
{{part1.semi_axis_y}}. The check `volume_closed_form_against_sections` prints the volume from the sections
{{part1.volume_from_sections}} against the closed form {{part1.ellipsoid_volume}}. The check
`volume_against_sample` prints the sampled volume {{part1.volume_sample}} with the error
{{part1.volume_sample_error}} against the same closed form.
