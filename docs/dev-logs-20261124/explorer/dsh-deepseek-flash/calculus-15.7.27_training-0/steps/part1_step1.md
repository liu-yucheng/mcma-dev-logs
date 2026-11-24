## Step 1.1 — The innermost limit fixes the variable y

**Why.** The integral is written with the differentials $dy\,dz\,dx$. The innermost integral therefore runs in $y$. Its lower limit is $0$ and its upper limit is $2-2z$. The upper limit uses the variable $z$ alone, and it uses no $x$. So the height in the direction $y$ depends on $z$ alone.

**Step.** Hold the pair $(x,z)$ fixed. The innermost integral covers the segment

$$\int_0^{2-2z} dy = 2-2z .$$

This number is the length of the segment in $y$ above the point $(x,z)$. It is the height of the solid at that point.

**Result.** Above a base point $(x,z)$ the solid spans $0 \le y \le 2-2z$. The height is $2-2z$, and it is the same for every $x$. Three values follow at once: the height is $2$ at $z=0$, it is $1$ at $z=1/2$, and it is $0$ at $z=1$.

**Check.** `code/part1_verify.py` evaluates the upper limit at two points with the same $z$ but different $x$, and it obtains the same height for both points. It also evaluates the height at $z=0$, $z=1/2$, and $z=1$, and it compares each value with the value that the limit function returns.
