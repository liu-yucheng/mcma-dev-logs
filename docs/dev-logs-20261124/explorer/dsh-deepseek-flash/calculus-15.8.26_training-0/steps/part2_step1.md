## Step 2.1: Write the solid as three pairs of limits

**Reason.** Step 1.2 gives the angle range, step 1.1 gives the radial bound, and step 1.3 gives the
height bound. Each bound comes from one surface, so the solid is the set of points that satisfy all
three pairs of limits at once:
$$E = \left\{(r,\theta,z) : -\frac{\pi}{2} \le \theta \le \frac{\pi}{2},\ 0 \le r \le a\cos\theta,\
-\sqrt{a^{2} - r^{2}} \le z \le \sqrt{a^{2} - r^{2}}\right\}.$$
The outer variable is $\theta$, the middle variable is $r$, and the inner variable is $z$. This
order is legal for one reason only: the limits of $r$ depend on $\theta$ alone, and the limits of
$z$ depend on $r$ alone. No inner limit depends on a variable that is still outside it.

**Computation.** Take $a = 1$. Bisection on the equation of the trace gives the largest radius at
the angle $\theta$: the value is $1.0$ at $\theta = 0$, $0.707106781186549$ at $\theta = \pi/4$, and
$0.5000000000000022$ at $\theta = \pi/3$. A ray of a fixed angle meets the solid in one segment, so
the count of segments along each ray is $1$.

**Common mistake.** A reader may put the outer integral over $r$ from $0$ to $a$, but the inner
limit of $r$ is $a\cos\theta$, which depends on $\theta$ and reaches $0$ at both ends of the range.

**Result.** The solid is described by the three pairs of limits above, in the order $\theta$, then
$r$, then $z$. The left panel of Figure 2 draws the footprint and one polar cell of it.

**Verification.** `code/part2_verify.py` prints `base_radius_at_theta_0` as $1.0$,
`base_radius_at_theta_1` as $0.707106781186549$, and `single_vertical_segment` as $1.0$ for both
the smallest and the largest count. It prints `region_predicates_agree` as $0.0$ disagreements over
$80000$ samples, while the control with a shortened angle range prints $6905$ disagreements.

![Figure 2: the footprint of the cylinder in the plane $z = 0$ with one polar cell, and the vertical segment over one ray](figures/part2_figure1.png)
