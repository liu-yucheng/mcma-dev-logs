## Step 1.2. Find the projection on the plane $z = 0$

### Reason
The projection on the plane $z = 0$ keeps the coordinates $x$ and $y$ and drops $z$. A pair $(x, y)$ belongs to the projection exactly when some $z$ completes the point, so the projection is the set of pairs that the solid attains.

### Computation
The inequality $0 \le z \le 1 - y$ has a solution in $z$ exactly when $0 \le y \le 1$. Together with $x^{2} \le y$, the projection is the parabolic segment $\{(x, y) : -1 \le x \le 1,\ x^{2} \le y \le 1\}$. Its area is the integral $\int_{-1}^{1} (1 - x^{2})\,dx$.

### Result
The area of the projection on the plane $z = 0$ is {{p1_projection_area}}, and the exact value is $\frac{4}{3}$.
`code/part1_verify.py` compares this integral with the polygon area of the same boundary and with the exact fraction.
