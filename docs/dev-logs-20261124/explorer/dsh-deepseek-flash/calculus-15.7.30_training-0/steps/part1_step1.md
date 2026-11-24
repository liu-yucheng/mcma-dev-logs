### Step 1.1 — Read the three surfaces and write the condition on a point

**Reason.** Every later step uses one description of the region, so write that description first
and read it from the three surfaces of the statement.

**Computation.** The surface $y^2+z^2=9$ is a circular cylinder of radius $3$ whose axis is the
$x$-axis. The surface $x=-2$ is a plane, and the surface $x=2$ is a parallel plane. The solid is
bounded by these three surfaces and by no other surface, so a point lies in $E$ exactly when

$$E=\{(x,y,z): -2\leq x\leq 2,\ y^2+z^2\leq 9\}.$$

**Result.** $E$ is the part of the cylinder of radius $3$ about the $x$-axis that lies between the
planes $x=-2$ and $x=2$. It is a closed body, and it is symmetric about each of the three
coordinate planes.

**Verification.** The script `code/part1_verify.py` measures the volume of $E$ by three routes, and
every route agrees with the closed form $36\pi$.
