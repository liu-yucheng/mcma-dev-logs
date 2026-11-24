## Step 1.2: The angle range is $-\pi/2 \le \theta \le \pi/2$

**Reason.** The symbol $r$ is a distance from the $z$-axis, so $r \ge 0$. The right side
$a\cos\theta$ must therefore be not negative, and $a > 0$ gives $\cos\theta \ge 0$. The equation
then describes points only for $-\pi/2 \le \theta \le \pi/2$, taken modulo $2\pi$. The statement
of the problem does not print this range, so the range is a result and not a given fact.

**Computation.** At both ends of the range, $a\cos(\pm\pi/2) = 6.123\times10^{-17}$, which is
zero up to round-off, so the trace closes at the origin. At $\theta = 3\pi/4$ the right side is
$-0.7071067811865475$, so no point of the cylinder exists there. Inside the range the distance $r$
reaches its largest value $a = 1.0$ at $\theta = 0$.

**Common mistake.** A reader may take the full circle $0 \le \theta \le 2\pi$, but the limit
$r \ge 0$ gives $-\pi/2 \le \theta \le \pi/2$, and every angle outside that range returns a
negative distance.

**Result.** The angle range is $-\pi/2 \le \theta \le \pi/2$. At both ends the base radius is
$0$, and the largest base radius is $a$ at $\theta = 0$.

**Verification.** `code/part1_verify.py` prints `angle_range_right_end_radius` as
$6.123\times10^{-17}$ and `angle_range_left_end_radius` as $6.123\times10^{-17}$, both against
$0.0$. It prints `angle_outside_range_is_negative` as $-0.7071067811865475$ at
$\theta = 3\pi/4$.
