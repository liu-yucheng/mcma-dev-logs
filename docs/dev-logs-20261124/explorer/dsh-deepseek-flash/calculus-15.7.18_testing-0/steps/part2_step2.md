# Step 2.2: check which variable each limit may use

## Reason

The limit of an inner variable may use only the variables that the outer integrals still hold. If a limit uses a variable that the inner integrals already removed, the integral cannot be evaluated. The test moves one coordinate by a small step at a point inside the solid and records which coordinates change the answer of the membership test.

A reader may let the inner limit depend on $x$, but the integral over $z$ runs before the integral over $x$, so the limit of $z$ may use $y$ alone.

## Computation

The point $(0.30, 1.20, 1.00)$ belongs to the solid. Move each coordinate by $0.05$ in turn and test the three limits of the order $dz\,dx\,dy$. The outer limit uses no coordinate. The middle limit $0 \le x \le \dfrac{y}{3}$ uses $y$. The inner limit $0 \le z \le \sqrt{9 - y^{2}}$ uses $y$.

## Result

The probe records the dependence ${{p2_chosen_inner_dependence}}$ for the middle limit and the dependence ${{p2_chosen_inner_dependence}}$ for the inner limit. No limit of this order uses $x$, so the order is admissible.

## Verification

`code/part2_verify.py` compares the dependence set that the probe records with the set of variables that each limit declares, and it reports the same set for both limits.
