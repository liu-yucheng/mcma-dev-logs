## Part 1, Step 1: name the body that the two surfaces enclose

**Goal.** Write the solid $E$ as a set of inequalities before any integral appears.

**Reason.** The statement says that the paraboloid $z = 1 - x^2 - y^2$ and the plane $z = 0$ enclose $E$, and it gives no inequality. The paraboloid opens downward, so its apex $(0, 0, 1)$ is its highest point. The two surfaces meet only where $1 - x^2 - y^2 = 0$, that is on the circle $x^2 + y^2 = 1$ in the plane $z = 0$. A closed body needs a rim, so this circle is the rim of $E$.

**Computation.** Take a point with $x^2 + y^2 < 1$. There the height of the paraboloid is positive, so the paraboloid lies above the plane. The vertical line through that point meets the two surfaces at $z = 0$ and at $z = 1 - x^2 - y^2$, and it meets the body between them. Take a point with $x^2 + y^2 > 1$. There the paraboloid lies below the plane, and the two surfaces do not bound any point above the plane, so no point of $E$ lies there.

$$E = \left\{(x, y, z) : x^2 + y^2 \leq 1,\; 0 \leq z \leq 1 - x^2 - y^2\right\}$$

**Result.** The body is a cap of height $1$ over a base disk of radius $1$. Figure 1 shows the cap and its rim. The cap is closed: the paraboloid closes the top and the disk closes the bottom.

**Verification.** The printed check `[[check:part1:boundary_radius]]` locates the rim twice. A bisection on $1 - r^2$ and the closed form $\sqrt{1}$ both give the radius $1.0$. The check `[[check:part1:height_extreme]]` reports the largest height $1.0$ by a grid search and by a bounded minimisation of $-z$.

**Common mistake.** A reader may take the body for the region above the paraboloid and below the plane $z = 2$, because the word "enclosed" suggests a box. The two surfaces meet at $z = 0$ alone, so the pair fixes one height, $0 \leq z \leq 1 - x^2 - y^2$, and no second ceiling.

FIGURE: part1_figure1.png | The solid $E$ and its projection. The left panel shows the paraboloid cap over the unit disk, its rim in red, and the plane $z = 0$ as the floor. The right panel shows the projection $D$, the closed unit disk, with its area $\pi$.
