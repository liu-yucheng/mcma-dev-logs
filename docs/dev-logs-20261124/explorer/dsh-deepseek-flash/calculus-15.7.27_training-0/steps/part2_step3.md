## Step 2.3 — A section at constant y is a trapezoid, and the three families agree

**Why.** Take the plane $y = y_0$ with $0 \le y_0 < 2$. Put the value into the six inequalities of Step 1.3. This family completes the picture, because it shows how the base triangle shrinks as $y$ grows.

**Step.** The six inequalities become

$$0 \le x,\quad x+z \le 1,\quad 0 \le z \le 1-\frac{y_0}{2} .$$

For a fixed $z$ the variable $x$ runs from $0$ to $1-z$. The section is therefore the base triangle with the top corner cut off at the level $z = 1-y_0/2$. It is a trapezoid. Its lower parallel side lies at $z=0$ and runs from $x=0$ to $x=1$, so its length is $1$. Its upper parallel side lies at $z=1-y_0/2$ and runs from $x=0$ to $x=y_0/2$, so its length is $y_0/2$. The distance between the two sides is $1-y_0/2$. Its area is

$$A(y) = \frac{1}{2}\left(1-\frac{y}{2}\right)\left(1+\frac{y}{2}\right) = \frac{1}{2}-\frac{y^2}{8} .$$

**Result.** The section at constant $y$ is a trapezoid with the area $A(y) = 1/2-y^2/8$. Four values are $A(0) = 1/2$, $A(1/2) = 15/32$, $A(1) = 3/8$, and $A(3/2) = 7/32$. At $y=0$ the section is the base triangle $D$. At $y=2$ the section is the single point $P_2 = (0,0,1)$.

**Check.** `code/part2_verify.py` clips the plane $y=y_0$ at four values, compares each area with $1/2-y^2/8$, and then integrates each of the three families over its own variable. All three give the same total, and the exact fraction arithmetic gives the value $2/3$. The script also sums $240$ midpoint slices for the families in $z$ and in $x$ and compares each sum with the exact total. Figure 1 draws one section from each family.
