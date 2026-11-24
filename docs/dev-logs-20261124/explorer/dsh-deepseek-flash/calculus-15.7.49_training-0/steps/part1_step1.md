# 1.1 Four surfaces become four inequalities

$E$ is the part of the first octant that four surfaces bound. The first octant supplies the three sign conditions. Reason: a point of the first octant has three non-negative coordinates.

$$x \ge 0, \qquad y \ge 0, \qquad z \ge 0$$

The cylinder $x^2+y^2=1$ bounds $E$ from the outside. Reason: the statement names the cylinder as a bounding surface, and $E$ is bounded, so $E$ lies inside the cylinder.

$$x^2+y^2 \le 1 \iff 0 \le y \le \sqrt{1-x^2}$$

So $x$ runs from $0$ to $1$, and at a fixed $x$ the coordinate $y$ runs from $0$ to $Y=\sqrt{1-x^2}$. The plane $x=0$ closes the solid at the small values of $x$, and the cylinder closes it at $x=1$.

The plane $y=z$ bounds $z$ from above, and the plane $z=0$ bounds $z$ from below. Reason: $E$ lies between the two planes, so at a point of $E$ the value of $z$ is at least $0$ and at most the value of $y$ at that same point.

$$0 \le z \le y$$

The description of $E$ is therefore one pair of inequalities for each coordinate, and the outer pair holds no other variable.

$$E=\{(x,y,z) : 0 \le x \le 1,\ 0 \le y \le \sqrt{1-x^2},\ 0 \le z \le y\}$$

Four points are the vertices of $E$: $(0,0,0)$, $(0,1,0)$, $(0,1,1)$, and $(1,0,0)$. Reason: a vertex lies on three of the four surfaces, and these four points are the only such points in the first octant.

Figure 1 draws the four surfaces. The left panel labels each surface at a point that satisfies its own equation. The right panel draws the section at $x=0.6$.

Verification: `part1_verify.py` solves every triple of the four surfaces, keeps the solutions that satisfy the fourth surface, and prints the four vertices. It also computes the volume of $E$ in three integration orders, and the three quadratures agree with each other to $1.110\times 10^{-16}$. The Monte Carlo estimate of the volume is $0.333488$ with a standard error of $0.000236$, which is inside four standard errors of $1/3$.

**Result:** $E=\{(x,y,z) : 0 \le x \le 1,\ 0 \le y \le \sqrt{1-x^2},\ 0 \le z \le y\}$ and $V=1/3$.
