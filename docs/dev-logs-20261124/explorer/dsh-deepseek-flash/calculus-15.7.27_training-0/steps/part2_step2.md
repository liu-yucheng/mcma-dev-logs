## Step 2.2 — A section at constant x is a trapezoid

**Why.** Take the plane $x = x_0$ with $0 \le x_0 \le 1$. Put the value into the six inequalities of Step 1.3.

**Step.** The six inequalities become

$$0 \le z \le 1-x_0,\quad 0 \le y \le 2-2z .$$

Over the segment $0 \le z \le 1-x_0$ the upper bound on $y$ is a straight line that falls from $2$ at $z=0$ to $2x_0$ at $z=1-x_0$. The region under a straight line over a segment is a trapezoid. Its two parallel sides are the vertical sides at $z=0$ and at $z=1-x_0$, with the lengths $2$ and $2x_0$, and the distance between them is $1-x_0$. Its area is

$$A(x) = \frac{1}{2}\,(1-x)(2+2x) = 1-x^2 .$$

**Result.** The section at constant $x$ is a trapezoid with the area $A(x) = 1-x^2$. Four values are $A(0) = 1$, $A(1/4) = 15/16$, $A(1/2) = 3/4$, and $A(3/4) = 7/16$. At $x=0$ one parallel side has the length $0$, so the section is the base triangle. At $x=1$ the distance between the parallel sides is $0$, so the section is the single segment from $(1,0,0)$ to $(1,2,0)$.

**Check.** `code/part2_verify.py` clips the plane $x=x_0$ with the six half-spaces at the same four values. It compares the area of the clipped polygon with $1-x^2$ by exact fraction arithmetic, compares the two parallel sides with $2$ and $2x$, and compares the distance between them with $1-x$.
