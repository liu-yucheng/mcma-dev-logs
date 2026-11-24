# Step 3.2 The order $dy\,dx\,dz$

**Reason.** The outer variable is $z$, so the outer interval is the range of $z$ over the
projection on the plane $y = 0$. The middle variable is $x$, so the middle interval is the
range of $x$ along one horizontal slice of that projection at a fixed $z$. The inner
interval is the one of Step 3.1.

**Computation.** The projection $D_{xz}$ holds the pairs with $0 \le z \le {{p3.outer_z_max}}$
and $2z \le x \le 2$. With the inner interval of Step 3.1,

$$\iiint_E f \, dV = {{p3.latex_dydxdz}}.$$

The value of this integral with $f = 1$ is {{p3.value_dydxdz}}, which is the volume of
Step 1.3.

Figure 4 shows the projection with the three horizontal strips of this order.

!figure part3_figure1.png | The projection $D_{xz}$ on the plane $y = 0$ with the strips of the order $dy\,dx\,dz$ on the left, which fix $z$ and sweep $x$, and the strips of the order $dy\,dz\,dx$ on the right, which fix $x$ and sweep $z$.

**Result.** A third order is
$${{p3.latex_dydxdz}}$$
and its value with $f = 1$ is {{p3.value_dydxdz}}. Figure 4 shows its strips.

**A common mistake.** A reader may take the outer bound as $0 \le z \le 2$ because the
picture of the solid reaches the height of the vertex $B$, but the limits give
$0 \le z \le {{p3.outer_z_max}}$, and the check `outer bound z from 0 to 2 instead of 0 to 1:
its signed integral differs from the volume` prints {{p3.wrong_outer_bound}} against
{{p3.volume_reference}}.

**Check.** `code/part3_verify.py` compares the limits with the four half-spaces on
{{p3.random_count}} random points and on the boundary points, and it prints
{{p3.value_dydxdz}} by a symbolic integration and again by a nested Gauss rule with
{{p3.gauss_points}} points.
