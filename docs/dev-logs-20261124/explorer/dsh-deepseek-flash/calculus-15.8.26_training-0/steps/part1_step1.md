## Step 1.1: The equation $r = a\cos\theta$ draws a circle in the plane $z = 0$

**Reason.** The instruction asks for cylindrical coordinates, so the first task is to read the
given surface in the plane $z = 0$. Multiply the equation by $r$ and use
$x = r\cos\theta$ and $y = r\sin\theta$. Then $r^{2} = a r\cos\theta$ becomes
$x^{2} + y^{2} = a x$. Complete the square in $x$ and the equation becomes
$(x - a/2)^{2} + y^{2} = (a/2)^{2}$. The trace in the plane $z = 0$ is therefore a circle of
radius $a/2$ about the point $(a/2, 0)$, and the surface itself is the vertical cylinder over
that circle.

**Computation.** Take the reference radius $a = 1$. The trace has center $(0.5, 0)$ and diameter
$1.0$, and its area is $\pi a^{2}/4 = 0.785398163397$. The trace also passes through the origin,
where $r = 0$, and it stays in the half plane $x \ge 0$.

**Common mistake.** A reader may take $r = a\cos\theta$ for the circle of radius $a$ about the
origin, but completing the square gives the radius $a/2$ about $(a/2, 0)$.

**Result.** The cutting surface is the vertical cylinder of radius $a/2$ about the line
$x = a/2$, $y = 0$. Figure 1 draws its trace in the plane $z = 0$, the center $C$, and one
radius of length $a/2$.

**Verification.** `code/part1_verify.py` prints `base_area_grid` as $0.785408632020912$ and
`base_area_lens_formula` as $0.7853981633974483$, with a tolerance of $2.0\times10^{-3}$. It also
prints `cylinder_predicates_agree` as $0.0$ over $60000$ sample points, and
`tangency_center_distance` as $0.5$ against $0.5$.

![Figure 1: the trace of the cylinder $r = a\cos\theta$ in the plane $z = 0$, its center, and one radial segment](figures/part1_figure1.png)
