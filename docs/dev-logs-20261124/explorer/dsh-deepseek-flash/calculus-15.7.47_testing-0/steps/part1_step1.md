# Part 1. The solid and the limits of integration

## Step 1.1. Write the three bounding surfaces as inequalities

### Reason
A point belongs to the solid only when it lies on the correct side of each of the three surfaces, so each surface gives one inequality. The cylinder is a wall in the direction of $y$, because the solid lies above the parabola $y = x^{2}$ near the point $(0, 1, 0)$. A reader may take the cylinder as the roof, but the inequality $x^{2} \le y \le 1$ gives a wall, because $y$ is the coordinate that the cylinder restricts.

### Computation
The three surfaces are the cylinder $y = x^{2}$, the plane $z = 0$, and the plane $y + z = 1$. The wall and the roof meet where $x^{2} = 1$, because the roof reaches $z = 0$ at $y = 1$. Thus $x$ runs from $-1$ to $1$, and at each $x$ the coordinate $y$ runs from $x^{2}$ to $1$.

### Result
The solid is $D = \{(x, y, z) : -1 \le x \le 1,\ x^{2} \le y \le 1,\ 0 \le z \le 1 - y\}$.
Figure 1 marks each surface at a point that satisfies its own equation. `code/part1_verify.py` prints the largest residual as {{p1_residual}} and finds that the two descriptions of the solid agree on all 300000 sampled points.

[[figure:part1_figure1|Figure 1. The solid between the cylinder $y = x^{2}$ and the two planes. Each label sits at a point that its own equation satisfies.]]
