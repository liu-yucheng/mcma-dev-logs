## Step 2.2. Cut the solid at a fixed value of $y$

### Reason
A cut at a fixed $y$ is a plane parallel to the plane $y = 0$, so the cut keeps $x$ and $z$. The wall gives the limit of $x$, and the roof gives the limit of $z$.

### Computation
At a fixed $y$ the cut is the rectangle $|x| \le \sqrt{y}$, $0 \le z \le 1 - y$, and its area is
$$B(y) = 2\sqrt{y}\left(1 - y\right).$$
The corner list at $y = 1$ is {{p2_corner_y_one}}. The corners differ in $x$ and agree in $z$, so the cut is a segment of length $2$ and not a point.

### Result
At the values $y = $ {{p2_y_slices}} the areas are {{p2_area_y_list}}.
The shape of the cut at the two end values is {{p2_shape_y_list}}.
Figure 2 draws the three cuts of each family. `code/part2_verify.py` compares each area with a two-dimensional quadrature over the same cut.

[[figure:part2_figure1|Figure 2. The cuts at fixed $z$ in the $xy$-plane, the cuts at fixed $y$ in the $xz$-plane, and the projection on the plane $x = 0$.]]
