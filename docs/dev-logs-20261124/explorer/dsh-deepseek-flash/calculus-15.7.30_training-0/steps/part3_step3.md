### Step 3.3 — Fourth order: inner integral over $x$, then $z$, then $y$

**Reason.** Keep the rectangle and exchange the two inner integrations. Cut the rectangle into
strips of constant $z$: on the strip at $z$, the coordinate $x$ runs from $-2$ to $2$.

**Computation.** On the rectangle at $y=b$, the middle limits are $-\sqrt{9-b^2}\leq z\leq
\sqrt{9-b^2}$, and the inner limits are $-2\leq x\leq 2$. The outer variable $y$ runs over
$[-3,3]$. Therefore

$$\iiint_E f\,dV=\int_{-3}^{3}\int_{-\sqrt{9-y^2}}^{\sqrt{9-y^2}}\int_{-2}^{2}f(x,y,z)\,dx\,dz\,dy.$$

**Result.** In the order $dx\,dz\,dy$ the inner limits are constants, and the middle limits depend
on the outer variable $y$. The two orders with $y$ outermost differ only in the order of the two
inner integrations on the same rectangle, so their values agree.

**Verification.** The script `code/part3_verify.py` evaluates this order for $f=1$ and for
$f=1+x+y^2$, and reports $113.097335529233$ and $367.566340470006$ against $36\pi$ and $117\pi$.
