# Step 5.2 A numerical quadrature with no symbolic bound

**Reason.** A symbolic integration and its own limits cannot disagree, because both come from
the same limits. An independent check must integrate the polynomial over the box that holds
the solid and weight each point by one or by zero, so that no limit of integration of the six
orders enters the computation.

**Computation.** The box $0 \le x \le 2$, $0 \le y \le 2$, $0 \le z \le 1$ holds the solid,
and the six conditions of Step 1.2 decide whether a point of the box lies in $E$. A random
sample of {{p5.monte_carlo_count}} points gives {{p5.monte_carlo}} with the standard error
{{p5.monte_carlo_spread}}. A midpoint rule on a grid of cells gives the values
{{p5.riemann_20}}, {{p5.riemann_40}}, {{p5.riemann_80}}, {{p5.riemann_160}}, and
{{p5.riemann_320}} for 20, 40, 80, 160, and 320 cells on one axis; the last error is
{{p5.riemann_error_320}}, and each refinement lowers the error by about four.

Figure 6 plots the error of the midpoint rule against the number of cells on one axis.

!figure part5_figure1.png | The absolute error of the midpoint rule with the indicator of $E$ against the number of cells on one axis, with a dashed reference line of slope $-2$ above the data and a band that holds the error of the box quadrature.

**Result.** Both quadratures agree with the symbolic value {{p5.exact_common}}: the box
quadrature gives {{p5.monte_carlo}} with the standard error {{p5.monte_carlo_spread}}, and the
finest grid gives the error {{p5.riemann_error_320}}. Figure 6 shows the convergence.

**A common mistake.** A reader may integrate the polynomial over the whole box without the
indicator, but the limits give a smaller solid inside the box, and the weight of the extra
points changes the value of a polynomial that depends on the coordinates.

**Check.** `code/part5_verify.py` computes the box value with {{p5.monte_carlo_count}} random
points, the grid values at the five resolutions, and the ratios of the successive errors; it
prints {{p5.check_passed}} passing checks out of {{p5.check_count}}.
