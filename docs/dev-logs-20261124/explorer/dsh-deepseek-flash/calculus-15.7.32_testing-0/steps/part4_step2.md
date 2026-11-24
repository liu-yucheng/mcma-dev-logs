# Step 4.2 The order $dx\,dy\,dz$

**Reason.** The outer variable is $z$, so the outer interval is the range of $z$ over the
projection on the plane $x = 0$. The middle variable is $y$, so the middle interval is the
range of $y$ along one horizontal slice of that projection at a fixed $z$. The inner
interval is the one of Step 4.1.

**Computation.** The projection $D_{yz}$ holds the pairs with $0 \le z \le 1$ and
$2z \le y \le 2$. With the inner interval of Step 4.1,

$$\iiint_E f \, dV = {{p4.latex_dxdydz}}.$$

The value of this integral with $f = 1$ is {{p4.value_dxdydz}}, which is the volume of
Step 1.3.

Figure 5 shows the projection with the three horizontal strips of this order.

!figure part4_figure1.png | The projection $D_{yz}$ on the plane $x = 0$ with the strips of the order $dx\,dy\,dz$ on the left, which fix $z$ and sweep $y$, and the strips of the order $dx\,dz\,dy$ on the right, which fix $y$ and sweep $z$.

**Result.** A fifth order is
$${{p4.latex_dxdydz}}$$
and its value with $f = 1$ is {{p4.value_dxdydz}}. Figure 5 shows its strips.

**A common mistake.** A reader may take the middle bound as $0 \le y \le 2$ inside the outer
interval, but the limits give $2z \le y \le 2$, because a point with $y < 2z$ and a fixed $z$
lies outside the projection $D_{yz}$.

**Check.** `code/part4_verify.py` compares the limits with the four half-spaces on
{{p4.random_count}} random points and on the boundary points, and it prints
{{p4.value_dxdydz}} by a symbolic integration and again by a nested Gauss rule with
{{p4.gauss_points}} points.
