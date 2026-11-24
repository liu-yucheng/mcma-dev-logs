# Step 1.2: Write the solid as three inequalities

## Reason

The word "enclosed" means the bounded region between the surfaces. A point belongs to the region when it
is on the correct side of each surface. One test point fixes each side.

## Computation

The point $(0,1,0)$ satisfies the three equations with room to spare: $0<4$, $1>-1$, and $1+0<4$. Thus
the point $(0,1,0)$ is inside the solid, and every inequality points toward that point:

$$x^2+z^2\le 4,\qquad y\ge -1,\qquad y+z\le 4.$$

## Check

The cylinder gives $-2\le x\le 2$ and $-2\le z\le 2$. The first plane gives $y\ge -1$. The second plane
gives $y\le 4-z\le 6$. The region is bounded in all three directions, and the inequality
$y\le 4-z$ is the only bound that depends on a horizontal coordinate.

## Result

$$S=\{(x,y,z):x^2+z^2\le 4,\ -1\le y\le 4-z\}.$$

## Verification

`code/part1_verify.py` tests the three inequalities in two directions. The script builds $500$ points
inside the disk, each with a random height between $-1$ and $4-z$; all $500$ pass the membership test.
The script builds $500$ further points inside the same disk, each with a height at least $0.05$ below
$-1$ or above $4-z$; none of them passes. The printed counts are $500$ of $500$ and $0$ of $500$.
