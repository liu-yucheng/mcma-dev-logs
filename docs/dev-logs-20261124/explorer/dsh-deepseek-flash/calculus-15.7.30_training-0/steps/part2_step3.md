### Step 2.3 — Second order: inner integral over $y$, then $z$, then $x$

**Reason.** Keep the disk and change the direction of the strips. Cut the disk into strips of
constant $z$: on the strip at $z$, the coordinate $y$ runs from one half of the circle to the other.

**Computation.** On the disk, $y^2\leq 9-z^2$ gives $-\sqrt{9-z^2}\leq y\leq\sqrt{9-z^2}$, and the
strip exists when $-3\leq z\leq 3$. The outer variable $x$ runs over $[-2,2]$. Therefore

$$\iiint_E f\,dV=\int_{-2}^{2}\int_{-3}^{3}\int_{-\sqrt{9-z^2}}^{\sqrt{9-z^2}}f(x,y,z)\,dy\,dz\,dx.$$

**Result.** The order $dy\,dz\,dx$ has the same outer limits as Step 2.2 and a different inner
pair. The two orders differ only in the direction of the strips on the same disk, so the two
integrals are equal.

**Verification.** The script `code/part2_verify.py` evaluates this order for $f=1$ and reports
$113.097335529233$. The script also shows that the inner double integral depends on $x$: its value
is $91.891585117501$ at $x=0$ and $120.165918999810$ at $x=1$, and the difference is $9\pi$.
