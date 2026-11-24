## Step 5.2: Check the answer by scaling, by a second center, and by sampling

**Reason.** Three independent properties must hold for the answer of step 4.2. First, the geometry
grows with the radius, so a change of $a$ to $ka$ multiplies the volume by $k^{3}$. Second, the
volume does not depend on the center of the polar coordinates, so the same integral about the axis
of the cylinder must give the same number. Third, a sampling estimate must agree with the value
within its own standard error.

**Computation.** Take $a = 1$, $a = 2$, and $a = 3$. The slice integral gives $1.205506214$,
$9.644049708$, and $32.548667765$. The ratios are $8.0$ and $27.00000000000001$. The polar integral
about the cylinder axis gives $1.205506213504$. The sampling estimate with four million samples is
$1.205697$ with a standard error of $0.000489307864$, which is $0.389911$ standard errors from the
closed form.

**Common mistake.** A reader may expect the volume to grow in proportion to the area of the
footprint, but the height of the solid grows with $a$ as well, so the report of
`code/part5_verify.py` is the cube: `scaling_ratio_at_two` gives $8.0$ and `scaling_ratio_at_three`
gives $27.00000000000001$.

**Result.** All three checks agree with $V = \frac{a^{3}\left(6\pi - 8\right)}{9}$, so the answer of
part (a) is
$$V = \frac{2}{3}\pi a^{3} - \frac{8}{9}a^{3}.$$

**Verification.** `code/part5_verify.py` prints `slice_volume_at_a_1`, `slice_volume_at_a_2`, and
`slice_volume_at_a_3`, `scaling_ratio_at_two` as $8.0$, `scaling_ratio_at_three` as
$27.00000000000001$, `cylinder_axis_polar_matches_closed_form` as $1.205506213504$, and
`monte_carlo_agreement` at four standard errors.
