## Step 1.1 — Turn the four surfaces into three pairs of limits

**Reason.** A triple integral needs one pair of limits for each variable. The statement gives four surfaces: the cylinder $y^{2} + z^{2} = 9$, the plane $x = 0$, the plane $y = 3x$, and the plane $z = 0$, and it places the solid in the first octant. The cylinder speaks about $y$ and $z$ only, so it fixes the outer variables. The plane $y = 3x$ speaks about $x$ and $y$ only, so it fixes the inner variable once $y$ is known. A reader may take the solid for the whole quarter cylinder, but the plane $y = 3x$ gives the bound $x \le y / 3$, and that bound removes the part of the quarter cylinder where $x$ is larger. The first octant gives the lower bound $0$ of each variable.

**Computation.** The cylinder meets the plane $z = 0$ at $y = 3$, so $y$ runs from $0$ to $3$. For a fixed $y$ the cylinder gives $z$ from $0$ to $\sqrt{9 - y^{2}}$. For a fixed $y$ the plane $y = 3x$ gives $x$ from $0$ to $y / 3$. The three pairs of limits are

$$ 0 \le y \le 3, \qquad 0 \le z \le \sqrt{9 - y^{2}}, \qquad 0 \le x \le \frac{y}{3}. $$

The inner integral is a length along $x$, the middle integral is a length along $z$, and the outer integral is a length along $y$. The order is $dx\,dz\,dy$.

**Verification.** `code/part1_verify.py` integrates the constant $1$ over these limits in the order $dx\,dz\,dy$ and again in the order $dz\,dy\,dx$. The two orders agree to a relative difference of ${{volume_relative_difference_latex}}$, and each order agrees with a uniform sample of the box $0 \le x \le 1$, $0 \le y \le 3$, $0 \le z \le 3$. The sample route prints ${{volume_monte_carlo|3}}$ inside the error ${{volume_monte_carlo_error|3}}$, and the closed form prints ${{volume}}$.

**Result.** The volume of the solid is ${{volume|3}}$ cubic units, and the limits above are the limits of every integral in this tutorial. Figure 1 draws the four surfaces and the body that they close, and the anchor rows of `code/part1_verify.py` print the residual of the equation of each surface at the point that its label marks.

{{figure:part1_figure1|The solid $E$ that the four surfaces close. The curved face is $y^{2} + z^{2} = 9$, the slanted face is $y = 3x$, the base is $z = 0$, and the back face is $x = 0$. Each label points at a point of its own surface.}}
