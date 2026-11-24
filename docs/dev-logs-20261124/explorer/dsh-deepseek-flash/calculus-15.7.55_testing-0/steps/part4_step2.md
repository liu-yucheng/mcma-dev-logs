# Part 4, Step 2: the symbolic check and the rounded value

**Reason.** Part (b) asks for a computer algebra calculation of the exact maximum. The exact maximum follows from
the symbolic integral of the radial factor, so this step repeats the radial integral with a symbolic engine and
then rounds the result. The symbolic result must equal $\frac{2}{15}$ exactly, and the rounded value must agree
with the quadratures of Part 3.

A reader may take the symbolic integral as the only proof of the exact value, but the limits give the antiderivative
$\frac{1}{3}-\frac{1}{5}$ directly, because the symbolic engine and the antiderivative are two routes to one
number.

**Computation.** Integrate the radial factor symbolically and simplify the difference of the two closed forms.

$$\int_{0}^{1}r^{2}\left(1-r^{2}\right)dr=\left[\frac{r^{3}}{3}-\frac{r^{5}}{5}\right]_{0}^{1} =\frac{2}{15},\qquad \frac{8\pi}{15\sqrt{6}}-\frac{4\pi\sqrt{6}}{45}=0 .$$

The value rounded to six decimals is {{part4.six_decimals}}.

**Result.** The symbolic integral agrees with the antiderivative, the difference of the two closed forms simplifies
to zero, and the maximum value rounded to six decimals is {{part4.six_decimals}}.

**Verification.** `code/part4_verify.py` uses the symbolic engine and exact fractions. The check
`symbolic_integral_against_closed_form` prints the symbolic integral against the antiderivative value
{{part4.radial_integral}}, and the check `six_decimal_rounding_against_part3_value` prints
{{part4.six_decimals}} against the Part 3 value {{part3.exact_value}} rounded to six decimals.
