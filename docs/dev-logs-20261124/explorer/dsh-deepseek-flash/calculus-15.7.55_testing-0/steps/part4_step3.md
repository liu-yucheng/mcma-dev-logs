# Part 4, Step 3: the sign test and the final answer

**Reason.** The exchange argument of Part 2 rests on the sign of the integrand. A sign error in the quadratic
form would move the boundary and change the answer, so this step tests the sign on a large random sample and
compares it with the membership test $Q<1$. A large sample with no disagreement supports the boundary and the
value together.

A reader may take the sampled estimate as the answer, but the limits give the exact value {{part4.exact_value}}
as the answer, because the sample only confirms the sign split and the exact value comes from the closed form.

**Computation.** Sample {{part4.sign_sample_count}} points in a box that holds the body and compare the sign of
the integrand with the sign of $1-Q$.

$$f>0\iff Q<1,\qquad f<0\iff Q>1,\qquad f=0\iff Q=1 .$$

The sample gives {{part4.sign_disagreements}} disagreements. The sampling estimate of the integral is
{{part3.value_sample}} with the error {{part3.value_sample_error}}, and the exact value lies inside the interval
from {{part4.sample_lower}} to {{part4.sample_upper}}.

**Result.** The region is $E^{*}=\{(x,y,z):x^{2}+2y^{2}+3z^{2}\le 1\}$ and the exact maximum is
$\frac{8\pi}{15\sqrt{6}}=\frac{4\pi\sqrt{6}}{45}={{part4.exact_value}}$, that is {{part4.six_decimals}} to six
decimals. The mean value of the integrand over the region is {{part4.mean_value}}.

**Verification.** `code/part4_verify.py` runs the sign test and the interval test. The check
`sign_disagreements_against_zero` prints {{part4.sign_disagreements}} against 0 over
{{part4.sign_sample_count}} points, the checks `sample_interval_upper_above_exact` and
`sample_interval_lower_below_exact` print {{part4.sample_upper}} and {{part4.sample_lower}} around the exact
value, and the check `mean_value_route_against_closed_form` prints {{part4.mean_route}} against
{{part4.exact_value}}.
