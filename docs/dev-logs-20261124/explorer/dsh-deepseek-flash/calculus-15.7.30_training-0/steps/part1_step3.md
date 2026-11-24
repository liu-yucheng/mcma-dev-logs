### Step 1.3 — Name the two projections

**Reason.** An integration order is a projection followed by a stack of sections. Each order needs
the projection that drops the two inner variables, so name the two projections once.

**Computation.** Drop $x$: the set $\{(y,z): y^2+z^2\leq 9\}$ is the disk of radius $3$ in the
plane $x=0$. Drop $z$: the set $\{(x,y): -2\leq x\leq 2,\ -3\leq y\leq 3\}$ is the rectangle
$[-2,2]\times[-3,3]$ in the plane $z=0$.

**Result.** The projection on the plane $x=0$ is a disk. The projection on the plane $z=0$ is a
rectangle. A projection that keeps the coordinates $x$ and $z$ drops $y$, so it lies on the plane
$y=0$, and by symmetry it is the same rectangle.

**Verification.** The script `code/part1_verify.py` measures the disk area on a grid at five values
of $x$ and reports $28.2754$ against $9\pi=28.2743$. The plane $x=2.2$ misses the solid, and the
measured area there is $0$.
