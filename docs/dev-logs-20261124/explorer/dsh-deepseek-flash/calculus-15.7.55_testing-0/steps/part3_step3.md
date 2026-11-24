# Part 3, Step 3: multiply the factors and read the answer

**Reason.** The volume integral over $P$ is the product of the determinant factor of Step 1, the angular factor
of Step 2, and the radial integral of Step 2. A product of three factors is easy to check by a second route, and
the second route also gives the mean value of the integrand.

A reader may take the answer as the radial integral $2/15$ alone, but the limits give the product with
$4\pi/\sqrt{6}$, because the determinant and the angular factor both multiply the radial integral.

**Computation.** Multiply the three factors.

$$\iiint_{P}\left(1-Q\right)dV=\frac{1}{\sqrt{6}}\cdot 4\pi\cdot\frac{2}{15} =\frac{8\pi}{15\sqrt{6}}=\frac{8\pi\sqrt{6}}{90}=\frac{4\pi\sqrt{6}}{45} ={{part3.exact_value}}.$$

A second route uses the mean value of the integrand over $P$. The mean value of $Q$ over the ellipsoid is
$1/5$ of the trace divided by the dimension, that is $3/5$, so the mean of $1-Q$ is
$2/5={{part3.mean_value}}$ and the integral is $\frac{2}{5}V(P)={{part3.exact_value_rationalized}}$.

**Result.** The maximum value is {{part3.exact_value}}, the rationalized form gives
{{part3.exact_value_rationalized}}, the Cartesian quadrature gives {{part3.value_cartesian}}, and the Gauss rule
gives {{part3.value_gauss}}. All four values agree.

**Verification.** `code/part3_verify.py` evaluates the same integral by three independent methods. The checks
`substitution_route_against_rationalized_route`, `cartesian_quadrature_against_exact_value`, and
`gauss_rule_against_exact_value` print {{part3.exact_value_rationalized}}, {{part3.value_cartesian}}, and
{{part3.value_gauss}} against {{part3.exact_value}}. The check `mean_value_against_two_fifths` prints the closed
mean {{part3.mean_value}} against $2/5$, and the check `mean_sample_against_closed_mean` prints the sampled mean
{{part3.mean_sample}} with the error {{part3.mean_sample_error}} against the closed mean.
