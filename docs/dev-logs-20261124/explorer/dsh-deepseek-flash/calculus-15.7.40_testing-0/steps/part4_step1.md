## Step 4.1 The height over the shadow and the shadow itself

**Reason.** Project the solid on the plane $z = 0$. A point $(x, y)$ belongs to the shadow when some point above it
belongs to the solid. The two upper bounds of $z$ are $1 - y^{2}$ and $1 - x$, so the largest $z$ above $(x, y)$ is
their minimum. The point is in the shadow exactly when that minimum is not negative, which gives $x \le 1$ and
$|y| \le 1$.

$$h(x, y) = {{p4_height_latex}}$$

**Computation.** A bisection of $80$ steps finds the largest $z$ above {{p4_height_points}} shadow points; the
print of `code/part4_verify.py` gives the largest difference from the minimum as $1.11 \times 10^{-16}$. The shadow
is the rectangle $[0, 1] \times [-1, 1]$
of area {{p4_shadow_area}}. The projection on the plane $y = 0$ keeps $x$ and $z$; its corners are $(0, 0)$, $(1, 0)$
and $(0, 1)$, so its area is {{p4_projection_area}}.

**Result.** The height is {{p4_height_latex}}. The shadow on the plane $z = 0$ has area {{p4_shadow_area}} and the
projection on the plane $y = 0$ has area {{p4_projection_area}}, and Figure 3 draws both regions. Verified by
`code/part4_verify.py`.
