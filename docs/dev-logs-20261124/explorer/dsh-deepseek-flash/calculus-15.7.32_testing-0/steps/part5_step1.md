# Step 5.1 Six orders, one value

**Reason.** Six formulas that describe the same solid must give the same number for every
function that is continuous on the solid. One polynomial is enough to test the six limits
against each other, because a wrong limit changes the value of a polynomial and not only the
value of the constant function.

**Computation.** Take $f(x, y, z) = {{p5.polynomial}}$. The six orders give the value
{{p5.exact_common}}, that is ${{p5.exact_common_latex}}$, and the six symbolic integrations
return one common result. The six formulas are laid out in Step 5.3.

The six formulas are also six different expressions: the count of distinct expressions is
{{p5.latex_distinct}}.

**Result.** All six orders agree on the polynomial {{p5.polynomial}}, and the common value is
{{p5.exact_common}}. The six formulas are {{p5.latex_distinct}} different expressions.

**A common mistake.** A reader may test the six formulas with the constant function alone,
but the limits give one value for that function even when two orders differ, because a
constant weight cannot see a wrong interval that moves nothing.

**Check.** `code/part5_verify.py` runs the six symbolic integrations of the polynomial, prints
the count of distinct results, and prints the common value {{p5.exact_common}}.
