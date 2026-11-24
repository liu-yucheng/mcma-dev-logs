## Step 1.3 The sections at a fixed y and at a fixed x

**Reason.** Set $y = y_{0}$. The bounds are $0 \le z \le 1 - y_{0}^{2}$ and $0 \le x \le 1 - z$. The largest $x$ for a
given $z$ is $1 - z$, so the length in $x$ falls linearly from $1$ at $z = 0$ to $1 - u$ at $z = u$, where
$u = 1 - y_{0}^{2}$. A region with two parallel vertical sides and a straight top is a right trapezoid. Set
$x = x_{0}$. The bounds are $0 \le z \le 1 - x_{0}$ and $|y| \le \sqrt{1 - z}$, so the two sides of the section are
the curves $|y| = \sqrt{1 - z}$.

A reader may take the section at $x = 1$ as a single point, but the printed corners give the segment from
$(1.000, -1.000, 0.000)$ to $(1.000, 1.000, 0.000)$ of length $2$.

**Computation.** The trapezoid area is the height $u$ times the mean of the parallel sides:

$$B(y_{0}) = u \cdot \frac{1 + (1 - u)}{2} = u - \frac{u^{2}}{2}, \qquad u = 1 - y_{0}^{2}$$

The corners at $y = 0$ are {{p1_corners_at_y_zero}}, where two corners coincide and the trapezoid degenerates to a
triangle. The corners at $x = 1$ are {{p1_corners_at_x_one}}, and the corners at $z = 0$ are
{{p1_corners_at_z_zero}}.

**Result.** The section at fixed $y$ is {{p1_shape_at_y}}, and the section at fixed $x$ is {{p1_shape_at_x}}.
Figure 2 draws the three sections, and `code/part1_figure2.py` prints their areas: the section at $z = 0.5$ has the
area $0.707107$, the section at $y = 0.5$ has the area $0.468750$, and the section at $x = 0.25$ has the area
$1.166667$. Verified by `code/part1_verify.py`, which compares a quadrature of $2\sqrt{1 - z}$ with the closed form
of the area at fixed $x$.
