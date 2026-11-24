# Step 1.3 - Name the three faces and the three edges

Part 1: what the solid is.

## Reason

An integral over a solid cuts the boundary into pieces, and each piece supplies one limit or one base. Therefore we must know which piece is where, and where two pieces meet. The edges matter, because an edge is the curve along which one limit changes its formula.

## Computation

Take the three walls from Step 1.1 and keep only the part that touches the solid.

- Floor: the plane $z = 0$ over the region $y \geq x^{2}$, $y \leq 1$.
- Wall: the cylinder $y = x^{2}$, with $0 \leq z \leq 1 - x^{2}$.
- Roof: the plane $y + z = 1$, with $y \geq x^{2}$.

Now intersect the walls in pairs.

- Floor with wall: set $z = 0$ and $y = x^{2}$. This gives the parabola $\left(x,\, x^{2},\, 0\right)$ for $-1 \leq x \leq 1$.
- Wall with roof: set $y = x^{2}$ and $y + z = 1$. This gives $z = 1 - x^{2}$, the curve $\left(x,\, x^{2},\, 1 - x^{2}\right)$.
- Floor with roof: set $z = 0$ and $y + z = 1$. This gives $y = 1$, the straight edge $\left(x,\, 1,\, 0\right)$ for $-1 \leq x \leq 1$.

## Result

The solid has three faces and three edges. The highest point of the solid is $\left(0,\, 0,\, 1\right)$, where the wall meets the roof above the origin. The two ends of the sharp edge are $\left(-1,\, 1,\, 0\right)$ and $\left(1,\, 1,\, 0\right)$. At those two points the solid has no thickness, because the wall, the floor, and the roof meet there.

## Check

`code/part1_verify.py` tests nine points. The points $\left(0,0,0\right)$, $\left(1,1,0\right)$, $\left(-1,1,0\right)$, $\left(0,0,1\right)$, and $\left(0,1,0\right)$ are members. The points $\left(1.02,1,0\right)$, $\left(0,1.02,0\right)$, $\left(0,0,1.02\right)$, and $\left(0,-0.02,0\right)$ are not. The last four points sit just outside one wall each, so the three walls do bound the solid on every side.
