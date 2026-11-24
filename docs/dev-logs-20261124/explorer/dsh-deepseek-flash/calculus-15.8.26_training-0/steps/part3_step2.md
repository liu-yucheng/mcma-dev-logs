## Step 3.2: The radial integral vanishes at both ends of the angle range

**Reason.** At $\theta = \pm\pi/2$ the upper limit $a\cos\theta$ equals $0$, so the interval of $r$ is
the single point $r = 0$ and every integral over it is $0$. At $\theta = 0$ the upper limit is $a$,
which gives the largest value of the radial integral. On the whole interval $a^{2} - r^{2} \ge 0$,
because the upper limit never passes the sphere radius, so the height stays a real number.

**Computation.** Take $a = 1$. The radial integral is $0.666666666667$ at $\theta = 0$ and $0$ at
$\theta = \pm\pi/2$. The largest upper limit is $1.0$, the smallest upper limit is
$6.123\times10^{-17}$, and the smallest value of $a^{2} - r^{2}$ on the interval is $0.0$.

**Common mistake.** A reader may expect a large value at $\theta = \pm\pi/2$ because the vertical
segment there is long, but the radial interval has zero width, so the limits give the value $0$.

**Result.** The radial integral is $0$ at both ends of the angle range and
$\frac{2}{3}a^{3}$ at $\theta = 0$, and it stays real on the whole range.

**Verification.** `code/part3_verify.py` prints the eleven angles of `radial_integral_theta_` with a
worst error of $2.22\times10^{-16}$, `upper_bound_maximum` as $1.0$ against $a$,
`upper_bound_minimum` as $6.123\times10^{-17}$, and `upper_bound_keeps_height_real` as $0.0$.
