# Part 2, Step 2: compare the candidate regions

**Reason.** The exchange argument gives the answer in principle, but a reader wants evidence that no common
region does better. This step evaluates the integral over four regions of comparable size: the positive part
$P$, the unit ball, the unit cube, and the scaled copies of $P$.

A reader may take the unit ball as the best region because it is the roundest, but the limits give the ellipsoid
$P$ a larger value {{part2.maximum_value}} against {{part2.ball_inside}}, because the weight of the integrand
matches the shape of $P$ and not the shape of the ball.

**Computation.** Evaluate the same integrand over each region. Each value comes from a closed form and from an
independent quadrature.

| Region | Value | Quadrature |
| --- | --- | --- |
| $P$ | ${{part2.candidate_rows.0.value}}$ | ${{part2.candidate_rows.0.quadrature}}$ |
| unit ball | ${{part2.candidate_rows.1.value}}$ | ${{part2.candidate_rows.1.quadrature}}$ |
| unit cube | ${{part2.candidate_rows.2.value}}$ | ${{part2.candidate_rows.2.quadrature}}$ |
| scaled $0.80P$ | ${{part2.candidate_rows.3.value}}$ | ${{part2.candidate_rows.3.quadrature}}$ |
| scaled $1.25P$ | ${{part2.candidate_rows.4.value}}$ | ${{part2.candidate_rows.4.quadrature}}$ |

$P$ holds the largest value of the five rows. The unit ball holds a negative value, because the ball reaches
outside $P$ into the region of negative integrand.

**Result.** The maximum value is {{part2.maximum_value}}. Each other row is smaller, and the verification script prints the gap of each row to the maximum. The ball is
smaller because its outside part adds {{part2.ball_outside}}.

**Verification.** `code/part2_verify.py` prints each row with a closed form and a quadrature. The checks
`candidate_ellipsoid_P_closed_form_against_quadrature` and
`candidate_unit_ball_closed_form_against_quadrature` print the two values of the first two rows, and the checks
`candidate_scaled_0.80_below_maximum` and `candidate_scaled_1.25_below_maximum` assert the gap of each scaled copy
against the maximum {{part2.maximum_value}}.
