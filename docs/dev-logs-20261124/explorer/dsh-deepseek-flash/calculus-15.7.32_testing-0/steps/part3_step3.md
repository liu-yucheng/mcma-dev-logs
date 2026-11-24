# Step 3.3 The order $dy\,dz\,dx$

**Reason.** The exchange of the roles of the middle and the outer variable must follow the
shape of the projection and not the shape of the solid, because the inner interval of $y$
depends on $x$ and on $z$ and not on the order. On the projection $D_{xz}$ a vertical line
at a fixed $x$ runs from $z = 0$ to $z = x/2$, so the middle interval is that height range.

**Computation.** The outer interval is the range of $x$ over $D_{xz}$, that is
$0 \le x \le 2$. The middle interval is $0 \le z \le x/2$. With the inner interval of
Step 3.1,

$$\iiint_E f \, dV = {{p3.latex_dydzdx}}.$$

The value of this integral with $f = 1$ is {{p3.value_dydzdx}}. The right panel of Figure 4
draws the vertical strips of this order.

**Result.** A fourth order is
$${{p3.latex_dydzdx}}$$
and its value with $f = 1$ is {{p3.value_dydzdx}}, equal to the volume of Step 1.3.
Figure 4 shows its strips.

**A common mistake.** A reader may take the upper end of the height interval as the constant
$1$ inside the outer interval, but the limits give $z \le x/2$, because the height of the
solid above a fixed $x$ grows with $x$ and reaches $1$ only at $x = 2$.

**Check.** `code/part3_verify.py` reports the number of agreeing points of this order against
the half-spaces and prints {{p3.value_dydzdx}} by both the symbolic integration and the
nested Gauss rule.
