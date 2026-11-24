# Part 4, Step 1: the two closed forms carry one rational coefficient

**Reason.** The answer appears in two forms, $\frac{8\pi}{15\sqrt{6}}$ and $\frac{4\pi\sqrt{6}}{45}$. Both forms
must carry the same rational coefficient in front of $\pi^{2}$ after squaring, and that coefficient is a rational
number. A rational identity is exact and needs no tolerance, so it is the strongest check of this part.

A reader may take the two forms as different values because their irrational factors differ, but the limits give
one value, because the product $\sqrt{6}\cdot\sqrt{6}$ is the integer 6.

**Computation.** Square each form.

$$\left(\frac{8\pi}{15\sqrt{6}}\right)^{2}=\frac{64\pi^{2}}{225\cdot 6}=\frac{32\pi^{2}}{675}, \qquad\left(\frac{4\pi\sqrt{6}}{45}\right)^{2}=\frac{16\cdot 6\pi^{2}}{2025}=\frac{32\pi^{2}}{675}.$$

The rational coefficient is $\frac{32}{675}$ in both forms, and the script prints the numerator
{{part4.squared_coefficient.0}} and the denominator {{part4.squared_coefficient.1}} of that fraction.

**Result.** The two closed forms of Part 3 are one value, and the coefficient of $\pi^{2}$ is the rational number
$\frac{32}{675}$ in both forms. The maximum value is {{part4.exact_value}}.

**Verification.** `code/part4_verify.py` forms each square with exact fractions and compares them. The check
`squared_forms_carry_one_rational_coefficient` prints the coefficient of each form and asserts that the two
fractions are equal. The check `rationalized_form_against_closed_form` prints
{{part4.exact_value_rationalized}} against {{part4.exact_value}} with a tolerance of $10^{-15}$.
