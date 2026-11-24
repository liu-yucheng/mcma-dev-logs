### Step 4.2 — Fifth order: inner integral over $y$, then $x$, then $z$

**Reason.** Take the rectangle at a fixed $z$ as the region of the inner two integrations. Cut it
into strips of constant $x$: on the strip at $x$, the coordinate $y$ runs from the lower edge to
the upper edge.

**Computation.** On the rectangle at $z=c$, the coordinate $y$ runs from $-\sqrt{9-c^2}$ to
$\sqrt{9-c^2}$ for every $x$ in $[-2,2]$. The outer variable $z$ runs over $[-3,3]$. Therefore

$$\iiint_E f\,dV=\int_{-3}^{3}\int_{-2}^{2}\int_{-\sqrt{9-z^2}}^{\sqrt{9-z^2}}f(x,y,z)\,dy\,dx\,dz.$$

**Result.** In the order $dy\,dx\,dz$ the inner limits depend on the outer variable $z$, and the
middle limits are constants.

**Verification.** The script `code/part4_verify.py` evaluates this order for $f=1$ and for
$f=1+x+z^2$, and reports $113.097335529233$ and $367.566340470006$ against $36\pi$ and $117\pi$.
