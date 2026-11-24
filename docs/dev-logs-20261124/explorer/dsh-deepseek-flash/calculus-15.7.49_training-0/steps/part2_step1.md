# 2.1 The inner integral in $z$

The mass is the integral of the density over $E$. Reason: the density is a mass per unit volume, and the mass of a solid is the integral of its density.

$$m=\iiint_E (1+x+y+z)\,dV$$

Integrate in the order $dz\,dy\,dx$. Reason: in this order each limit holds only the variables of the outer integrations, so the three integrations follow the three inequalities of Step 1.1 from the innermost to the outermost.

$$m=\int_0^1\int_0^{Y}\int_0^{y}(1+x+y+z)\,dz\,dy\,dx$$

The inner integral uses $x$ and $y$ as constants, and it uses the upper limit $y$. Reason: the antiderivative of a polynomial in $z$ is a polynomial in $z$, and the upper limit replaces $z$.

$$\int_0^{y}(1+x+y+z)\,dz=(1+x)y+y^2+\frac{y^2}{2}=(1+x)y+\frac{3}{2}y^2$$

The two terms $y^2$ and $y^2/2$ come from the constant part $1+x+y$ times the length $y$ of the interval and from the term $z$ itself. They add to $\frac{3}{2}y^2$.

Verification: `part2_verify.py` computes this inner integral once with `sympy` and once with a numerical quadrature at three pairs of $(x,y)$, and it compares the two results at each pair.

**Result:** the inner integral in $z$ is $(1+x)y+\frac{3}{2}y^2$.
