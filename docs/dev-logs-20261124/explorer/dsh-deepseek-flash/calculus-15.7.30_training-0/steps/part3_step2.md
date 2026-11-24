### Step 3.2 — Third order: inner integral over $z$, then $x$, then $y$

**Reason.** Take the rectangle as the region of the inner two integrations. Cut the rectangle into
strips of constant $x$: on the strip at $x$, the coordinate $z$ runs from the lower edge to the
upper edge.

**Computation.** On the rectangle at $y=b$, the coordinate $z$ runs from $-\sqrt{9-b^2}$ to
$\sqrt{9-b^2}$ for every $x$ in $[-2,2]$. The outer variable $y$ runs over $[-3,3]$. Therefore

$$\iiint_E f\,dV=\int_{-3}^{3}\int_{-2}^{2}\int_{-\sqrt{9-y^2}}^{\sqrt{9-y^2}}f(x,y,z)\,dz\,dx\,dy.$$

**Result.** In the order $dz\,dx\,dy$ the inner limits depend on the outer variable $y$, and the
middle limits are constants. The projection on the plane $y=0$ is the rectangle
$[-2,2]\times[-3,3]$, and it gives this order.

**Verification.** The script `code/part3_verify.py` evaluates this order for $f=1$ and reports
$113.097335529233$ against $36\pi$.
