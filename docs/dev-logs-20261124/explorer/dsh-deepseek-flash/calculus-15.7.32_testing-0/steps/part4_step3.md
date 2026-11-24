# Step 4.3 The order $dx\,dz\,dy$

**Reason.** The last order fixes $y$ on the outside and $z$ in the middle. A vertical line at
a fixed $y$ runs from the base $z = 0$ up to the slanted face, so the middle interval is the
height range of the projection $D_{yz}$ at that $y$, and the inner interval stays the one of
Step 4.1, because the inner variable $x$ is bounded by faces and not by the order.

**Computation.** The outer interval is the range of $y$ over $D_{yz}$, that is
$0 \le y \le 2$. The middle interval is $0 \le z \le y/2$. With the inner interval of
Step 4.1,

$$\iiint_E f \, dV = {{p4.latex_dxdzdy}}.$$

The value of this integral with $f = 1$ is {{p4.value_dxdzdy}}. The right panel of Figure 5
draws the vertical strips of this order.

**Result.** A sixth order is
$${{p4.latex_dxdzdy}}$$
and its value with $f = 1$ is {{p4.value_dxdzdy}}, equal to the volume of Step 1.3.
Figure 5 shows its strips.

**A common mistake.** A reader may take the middle interval as $0 \le z \le 1$ for every
$y$, but the limits give $0 \le z \le y/2$, and the check `middle bound z from 0 to 1
instead of 0 to y/2: its signed integral differs from the volume` prints
{{p4.wrong_middle_bound}} against {{p4.volume_reference}}.

**Check.** `code/part4_verify.py` reports the number of agreeing points of this order against
the half-spaces and prints {{p4.value_dxdzdy}} by both the symbolic integration and the
nested Gauss rule.
