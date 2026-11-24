# Step 5.3 The six answers

**Reason.** The exercise asks for six iterated integrals and for no number, so the answer is
the six formulas together with the reason that each limit follows from a face of the solid.
The six formulas come in three pairs, and each pair fixes the same innermost variable.

**Computation.** With $z$ innermost:

$$\iiint_E f \, dV = {{p2.latex_dzdxdy}} = {{p2.latex_dzdydx}}.$$

With $y$ innermost:

$$\iiint_E f \, dV = {{p3.latex_dydxdz}} = {{p3.latex_dydzdx}}.$$

With $x$ innermost:

$$\iiint_E f \, dV = {{p4.latex_dxdydz}} = {{p4.latex_dxdzdy}}.$$

Every formula gives the volume ${{p1.volume_latex}}$ when $f = 1$, and every formula gives
{{p5.exact_common}} when $f = {{p5.polynomial}}$.

**Result.** The six iterated integrals of the exercise are the six formulas of this step:
${{p2.latex_dzdxdy}}$, ${{p2.latex_dzdydx}}$, ${{p3.latex_dydxdz}}$, ${{p3.latex_dydzdx}}$,
${{p4.latex_dxdydz}}$, and ${{p4.latex_dxdzdy}}$, and each of them equals the triple integral
of $f$ over $E$.

**A common mistake.** A reader may keep the formula of a pair and exchange only the two outer
differentials, but the limits give a different order of nesting, because the outer interval
belongs to the outer differential and the middle interval belongs to the middle one.

**Check.** `code/part5_verify.py` prints the six formulas and their common value, and
`code/part2_verify.py`, `code/part3_verify.py`, and `code/part4_verify.py` check the two
formulas of each pair against the half-spaces and against the volume
${{p1.volume_latex}}$; {{checks.passed}} of the {{checks.total}} checks of the tutorial pass.
