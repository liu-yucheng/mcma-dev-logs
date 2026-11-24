# Step 1.2: drop one coordinate to get the three projections

## Reason

A projection keeps two coordinates and forgets the third one. Each pair that belongs to the projection is the pair that some point of the solid has. Take the inequalities of Step 1.1 and remove the forgotten coordinate from them.

A reader may name a projection by the coordinate that it drops, but a projection that drops $y$ lies on the plane $y = 0$ and keeps $x$ and $z$.

## Computation

On the plane $x = 0$ the solid keeps $y$ and $z$, and the two conditions $y \ge 0$ and $y^{2} + z^{2} \le 9$ describe a quarter disk of radius $3$. Its area is $\dfrac{9\pi}{4} = {{p1_yz_area_decimal}}$.

On the plane $y = 0$ the solid keeps $x$ and $z$. The conditions $0 \le z$ and $y^{2} + z^{2} \le 9$ give $0 \le z \le 3$, and the plane $y = 3x$ with the cylinder gives $0 \le x \le \dfrac{\sqrt{9 - z^{2}}}{3}$. The area is $\dfrac{3\pi}{4} = {{p1_xz_area_decimal}}$.

On the plane $z = 0$ the solid keeps $x$ and $y$, and the three conditions $0 \le x$, $3x \le y$ and $y \le 3$ describe the triangle with the corners $(0, 0)$, $(0, 3)$ and $(1, 3)$. Its area is $\dfrac{3}{2} = {{p1_xy_area_decimal}}$.

## Result

The three projections have the areas $\dfrac{9\pi}{4}$, $\dfrac{3\pi}{4}$ and $\dfrac{3}{2}$. Figure 1 shows the solid and Figure 2 shows the three projections with the same areas.

## Verification

`code/part1_verify.py` counts the cells of a fine grid that fall inside each projection and compares each count with its closed form. The relative gap of each count stays below the counted tolerance of $8.0\times 10^{-3}$.
