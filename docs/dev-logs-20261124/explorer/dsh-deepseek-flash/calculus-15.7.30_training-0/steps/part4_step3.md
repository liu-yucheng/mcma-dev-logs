### Step 4.3 — Sixth order: inner integral over $x$, then $y$, then $z$

**Reason.** Keep the rectangle at a fixed $z$ and exchange the two inner integrations. Cut the
rectangle into strips of constant $y$: on the strip at $y$, the coordinate $x$ runs from $-2$ to
$2$.

**Computation.** On the rectangle at $z=c$, the middle limits are $-\sqrt{9-c^2}\leq y\leq
\sqrt{9-c^2}$, and the inner limits are $-2\leq x\leq 2$. The outer variable $z$ runs over
$[-3,3]$. Therefore

$$\iiint_E f\,dV=\int_{-3}^{3}\int_{-\sqrt{9-z^2}}^{\sqrt{9-z^2}}\int_{-2}^{2}f(x,y,z)\,dx\,dy\,dz.$$

**Result.** In the order $dx\,dy\,dz$ the inner limits are constants, and the middle limits depend
on the outer variable $z$. The six orders are now complete: two with $x$ outermost, two with $y$
outermost, and two with $z$ outermost.

**Verification.** The script `code/part4_verify.py` evaluates this order for $f=1$ and reports
$113.097335529233$. The two orders with $z$ outermost agree to the printed digits.
