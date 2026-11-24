## Step 4.2: Expand the product and state the volume of the solid

**Reason.** Multiply $\frac{2}{3}a^{3}$ into the parenthesis of step 4.1. The two terms are
$\frac{2}{3}\pi a^{3}$ and $\frac{2}{3}a^{3} \cdot \frac{4}{3} = \frac{8}{9}a^{3}$. The difference is
the volume, and the common denominator $9$ gives the single fraction $\frac{a^{3}\left(6\pi - 8\right)}{9}$.

**Computation.** Take $a = 1$. The value is $1.205506213504$, and the two terms are
$2.094395102393$ and $0.888888888889$. At $a = 2$ the value is $9.644049708034$, and at $a = 3$ it
is $32.548667764616$. The solid holds the fraction $0.287793409211$ of the ball, and the rest of the
ball has the volume $2.983283991282$.

**Common mistake.** A reader may report the first term alone, but the second term is present:
`code/part4_verify.py` prints $2.094395102393$ for $\frac{2}{3}\pi a^{3}$ against $1.205506213504$
for the volume at $a = 1$.

**Result.** The volume of part (a) is
$$V = \frac{2}{3}\pi a^{3} - \frac{8}{9}a^{3} = \frac{a^{3}\left(6\pi - 8\right)}{9}.$$

**Verification.** `code/part4_verify.py` prints `two_forms_at_a_1`, `two_forms_at_a_2`, and
`two_forms_at_a_3` as $1.205506213504$, $9.644049708034$, and $32.548667764616$,
`closed_form_matches_triple_integral_a_1` and `closed_form_matches_triple_integral_a_2` against the
adaptive triple quadrature, `fraction_of_sphere` as $0.2877934092108062$ against
$\frac{6\pi - 8}{12\pi}$, and `solid_plus_complement_is_ball` as $4.18879020478639$ against
$\frac{4\pi}{3}$.
