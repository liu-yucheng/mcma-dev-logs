# Part 2. The two families of cross sections

## Step 2.1. Cut the solid at a fixed height $z$

### Reason
A cut at a fixed $z$ is a plane parallel to the plane $z = 0$, so the cut keeps $x$ and $y$ and replaces the third coordinate by a constant. A reader may take the cut as a disk of radius $\sqrt{1 - z}$, but the inequalities give $x^{2} \le y \le 1 - z$, which is a parabolic segment above the parabola and below a horizontal line, and a parabola is not a circle.

### Computation
At a fixed $z$ the cut is $\{(x, y) : |x| \le \sqrt{1 - z},\ x^{2} \le y \le 1 - z\}$. Its area is
$$A(z) = \int_{-\sqrt{1 - z}}^{\sqrt{1 - z}} \left(1 - z - x^{2}\right) dx = \frac{4}{3}\left(1 - z\right)^{3/2}.$$

### Result
At the heights $z = $ {{p2_z_slices}} the areas are {{p2_area_z_list}}.
The shape of the cut at the two end values is {{p2_shape_z_list}}, read from the printed corner list of `code/part2_verify.py`.
