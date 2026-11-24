### Step 2.2 — First order: inner integral over $z$, then $y$, then $x$

**Reason.** Take the disk as the region of the inner two integrations. Cut the disk into strips of
constant $y$: on the strip at $y$, the coordinate $z$ runs from the lower half of the circle to the
upper half.

**Computation.** On the disk, $z^2\leq 9-y^2$ gives $-\sqrt{9-y^2}\leq z\leq\sqrt{9-y^2}$, and the
strip exists when $-3\leq y\leq 3$. The outer variable $x$ runs over $[-2,2]$. Therefore

$$\iiint_E f\,dV=\int_{-2}^{2}\int_{-3}^{3}\int_{-\sqrt{9-y^2}}^{\sqrt{9-y^2}}f(x,y,z)\,dz\,dy\,dx.$$

**Result.** In the order $dz\,dy\,dx$ the inner pair $(dz,dy)$ covers the disk, and the inner limits
depend on $y$ only. The limits of the integral in $x$ are constants.

**Verification.** The script `code/part2_verify.py` evaluates this order for $f=1$ and reports
$113.097335529233$ against $36\pi$.
