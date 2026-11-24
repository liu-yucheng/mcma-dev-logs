# Step 2.2 The order $dz\,dx\,dy$

**Reason.** The outer variable is $y$, so the outer interval is the range of $y$ over the
projection $D_{xy}$. The middle variable is $x$, so the middle interval is the range of $x$
along one horizontal slice of $D_{xy}$ at a fixed $y$. The inner interval is the one of
Step 2.1.

**Computation.** The projection $D_{xy}$ holds the pairs with $0 \le y \le 2$ and
$2 - y \le x \le 2$, so the outer interval is $0 \le y \le 2$ and the middle interval is
$2 - y \le x \le 2$. The inner interval is $0 \le z \le (x + y - 2)/2$. Hence

$$\iiint_E f \, dV = {{p2.latex_dzdxdy}}.$$

The value of this integral with $f = 1$ is {{p2.value_dzdxdy}}, which is the volume of
Step 1.3.

Figure 3 shows the projection with the three horizontal strips of this order.

!figure part2_figure1.png | The projection $D_{xy}$ with the strips of the order $dz\,dx\,dy$ on the left, which fix $y$ and sweep $x$, and the strips of the order $dz\,dy\,dx$ on the right, which fix $x$ and sweep $y$.

**Result.** One of the six orders is
$${{p2.latex_dzdxdy}}$$
and its value with $f = 1$ is {{p2.value_dzdxdy}}. Figure 3 shows its strips.

**A common mistake.** A reader may take the order as a split of the solid into two pieces,
but the limits give one piece, because a single interval of $y$, a single interval of $x$,
and a single interval of $z$ describe the whole solid.

**Check.** `code/part2_verify.py` compares the limits of this order with the four half-spaces
of Step 1.2 on {{p2.random_count}} random points and on the boundary points; it prints the
number of agreeing points. It also computes the value by a symbolic integration and by a
nested Gauss rule with {{p2.gauss_points}} points, and prints
{{p2.value_dzdxdy}} twice.
