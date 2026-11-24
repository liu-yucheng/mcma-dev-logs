### Step 3.1 — The section at a fixed $y$ is a rectangle

**Reason.** The outer integral of the third and fourth orders runs over $y$, so the inner part must
be the section at a fixed value of $y$. Derive the shape from the inequalities, and read the printed
corner list before naming the shape.

**Computation.** Fix $y=b$. The condition on the point is $-2\leq x\leq 2$ and $z^2\leq 9-b^2$.
The two conditions involve different variables, so the section is the product of two intervals:

$$\{(x,b,z): -2\leq x\leq 2,\ -\sqrt{9-b^2}\leq z\leq\sqrt{9-b^2}\}.$$

**Result.** The section at $y=b$ is the rectangle $[-2,2]\times[-\sqrt{9-b^2},\sqrt{9-b^2}]$ in the
plane $y=b$, and its area is $8\sqrt{9-b^2}$. At $b=0$ the area is $24$. At $|b|=3$ the rectangle
collapses to the segment $-2\leq x\leq 2$ on the line $z=0$, and the area is $0$.

**Verification.** The script `code/part3_verify.py` prints the corner list of the section at
$b=-3,-2,0,2,3$. At $|b|=3$ the printed corners are $(-2,0)$ and $(2,0)$, which is one segment, and
the printed area is $0$.
