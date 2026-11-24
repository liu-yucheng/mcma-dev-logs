## Step 1.1 Read the region from the four surfaces

**Reason.** The solid has four boundary surfaces. The parabolic cylinder $z = 1 - y^{2}$ bounds $z$ from above and
the plane $z = 0$ bounds $z$ from below, so $z$ is the first coordinate with two explicit bounds. The plane
$x + z = 1$ bounds $x$ from above and the plane $x = 0$ bounds $x$ from below, so $x$ is the second coordinate. The
coordinate $y$ is the only free one, and its range comes from the condition that the two bounds of $z$ leave a
nonempty interval: $0 \le 1 - y^{2}$.

A reader may take the plane $x + z = 1$ as a bound on $z$, but the limits give $z$ its bound from the cylinder and
give $x$ the upper bound $1 - z$.

**Computation.** Solve $1 - y^{2} = 0$. The roots are {{p1_sympy_roots}}, so the free range is {{p1_y_interval}}.

$$E = \left\{(x, y, z) : -1 \le y \le 1,\ 0 \le z \le 1 - y^{2},\ 0 \le x \le 1 - z\right\}$$

**Result.** The region is the set $E$ above, and the interval of $y$ is {{p1_y_interval}}. The two membership tests
of `code/part1_verify.py`, one by height and one by width, agree on all {{p1_samples}} sampled points, with
{{p1_disagreements}} disagreements. The section areas at fixed height are {{p1_area_at_z_table}}, and Figure 1 draws
the solid with its four surfaces. Verified by `code/part1_verify.py`.
