### Step 2.1 — The section at a fixed $x$ is a disk

**Reason.** The outer integral of the first two orders runs over $x$, so the inner part must be the
section at a fixed value of $x$.

**Computation.** Fix $x=t$ with $-2\leq t\leq 2$. The condition on the point is $-2\leq t\leq 2$
and $y^2+z^2\leq 9$. The first condition holds for the whole slice, so the section is
$\{(t,y,z): y^2+z^2\leq 9\}$: a disk of radius $3$ in the plane $x=t$.

**Result.** Every section at a fixed $x$ is a disk of radius $3$ with area $9\pi$. The shape and
the area do not change with $x$.

**Verification.** The script `code/part2_verify.py` measures the area of the section on a grid at
five values of $x$ and prints each measured area against $9\pi=28.274333882308$.
