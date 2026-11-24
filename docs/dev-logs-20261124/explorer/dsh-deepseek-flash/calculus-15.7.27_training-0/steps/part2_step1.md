## Step 2.1 — A section at constant z is a rectangle

**Why.** A cross section shows the shape of the solid in one plane. Take the plane $z = z_0$ with $0 \le z_0 \le 1$. Put the value into the six inequalities of Step 1.3 and keep only those that still hold.

**Step.** The six inequalities become

$$0 \le x \le 1,\quad x \le 1-z_0,\quad 0 \le y \le 2-2z_0 .$$

The two bounds on $x$ combine into $0 \le x \le 1-z_0$, because $z_0 \ge 0$ makes $1-z_0$ no larger than $1$. The bound on $y$ uses no $x$. The section is therefore the product of two segments, so it is a rectangle with the width $1-z_0$ and the height $2-2z_0$. Its area is

$$A(z) = (1-z)(2-2z) = 2(1-z)^2 .$$

**Result.** The section at constant $z$ is a rectangle with the area $A(z) = 2(1-z)^2$. Four values are $A(0) = 2$, $A(1/4) = 9/8$, $A(1/2) = 1/2$, and $A(3/4) = 1/8$. The area falls as $z$ grows, and at $z=1$ the section is the single point $P_2 = (0,0,1)$.

**Check.** `code/part2_verify.py` clips the plane $z=z_0$ with the six half-spaces at four values of $z_0$. It compares the area of the clipped polygon with the closed form $2(1-z)^2$ by exact fraction arithmetic. It also compares the width and the height of the rectangle with $1-z$ and $2-2z$, and it takes the shape name from the number of corners and the number of parallel pairs.
