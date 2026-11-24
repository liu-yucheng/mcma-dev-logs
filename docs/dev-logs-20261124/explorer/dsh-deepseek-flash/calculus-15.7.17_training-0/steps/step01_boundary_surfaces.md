# Step 1 — Identify the two boundary surfaces

## Reason

The limits of the integral come from the geometry of the two surfaces. You must know which surface is the floor of the region and which surface is the roof. The direction in which the paraboloid opens decides this.

## Computation

The first surface is a paraboloid of revolution:

$$
x = 4y^{2} + 4z^{2} = 4\left(y^{2} + z^{2}\right).
$$

Set $r^{2} = y^{2} + z^{2}$. The equation becomes $x = 4r^{2}$. The vertex is the origin, because $r = 0$ gives $x = 0$. The value $x = 4r^{2}$ increases with $r$. Therefore the paraboloid opens along the positive $x$ axis.

The second surface is the plane $x = 4$. This plane is parallel to the $yz$ plane and it cuts the $x$ axis at $(4, 0, 0)$.

At the axis point $(0, 0)$ of the $yz$ plane, the paraboloid has $x = 0$. The plane has $x = 4$. Thus the paraboloid is below the plane near the axis.

## Result

The region $E$ is the set of points above the paraboloid and below the plane:

$$
E = \left\{(x, y, z) : 4\left(y^{2} + z^{2}\right) \le x \le 4\right\}.
$$

The curved surface is the lower bound on $x$. The flat surface is the upper bound on $x$.

## Verification

`code/part1_verify.py` checks the height of the paraboloid at chosen radii. It reports the height $4.000000$ at $r = 1$ and the height $4.080400$ at $r = 1.01$. Both values agree with the statement above.
