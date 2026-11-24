# Step 2.3 The order $dz\,dy\,dx$

**Reason.** The exchange of $x$ and $y$ leaves the four half-spaces of Step 1.1 unchanged,
because the conditions $x \le 2$ and $y \le 2$ exchange and the condition
$x + y - 2z \ge 2$ is symmetric in $x$ and $y$. A symmetry of the solid exchanges the orders
of integration that fix the same third variable, so the second order with $z$ innermost is
the first order with $x$ and $y$ exchanged.

**Computation.** The outer interval is the range of $x$ over $D_{xy}$, that is
$0 \le x \le 2$. The middle interval is the range of $y$ along one vertical slice of
$D_{xy}$ at a fixed $x$, that is $2 - x \le y \le 2$. The inner interval is the one of
Step 2.1. Hence

$$\iiint_E f \, dV = {{p2.latex_dzdydx}}.$$

The value of this integral with $f = 1$ is {{p2.value_dzdydx}}. The right panel of Figure 3
draws the vertical strips of this order.

**Result.** A second order is
$${{p2.latex_dzdydx}}$$
and its value with $f = 1$ is {{p2.value_dzdydx}}, equal to the value of Step 2.2 and to the
volume of Step 1.3. Figure 3 shows its strips.

**A common mistake.** A reader may take the middle bound as $0 \le y \le 2$ inside the outer
interval, but the limits give $2 - x \le y \le 2$, because a point with $y < 2 - x$ and a
fixed $x$ leaves the projection $D_{xy}$.

**Check.** `code/part2_verify.py` reports the number of agreeing points of this order against
the half-spaces, and it prints the value {{p2.value_dzdydx}} by a symbolic integration and
again by a nested Gauss rule.
