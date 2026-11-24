# Step 1.1: turn the four boundary words into four inequalities

## Reason

The word "bounded" names one surface for each condition, and each point of the solid must stay on one chosen side of that surface. The first octant is the part of space where none of the three coordinates is negative. Write each condition as an inequality before you draw anything, because a picture of a curved surface hides the side that the solid keeps.

A reader may take the cylinder to be $x^{2} + y^{2} = 9$ with its axis on $z$, but the equation names $y$ and $z$, so the axis of this cylinder is the $x$ axis.

## Computation

The cylinder gives $y^{2} + z^{2} \le 9$. The plane $x = 0$ gives $x \ge 0$. The plane $y = 3x$ gives $y \ge 3x$. The plane $z = 0$ gives $z \ge 0$. The first octant repeats $x \ge 0$ and $z \ge 0$ and adds $y \ge 0$.

The condition $y^{2} + z^{2} \le 9$ forces $z \le 3$. The conditions $0 \le 3x \le y$ with $y^{2} + z^{2} \le 9$ force $y \le 3$. The solid is therefore

$$E = \{(x, y, z) : 0 \le x,\ 3x \le y,\ y^{2} + z^{2} \le 9,\ 0 \le z\}.$$

## Result

The solid is closed in the three directions, and the point $(0, 0, 0)$ belongs to it. Its volume is ${{p1_volume_latex}}$.

## Verification

`code/part1_verify.py` tests the membership of sample points against the four inequalities and counts the volume of the solid. The count gives ${{p1_volume_count}}$ against the exact ${{p1_volume_decimal}}$, and the Monte Carlo estimate gives ${{p1_volume_monte_carlo}}$ with a standard error of ${{p1_volume_standard_error}}$, which is ${{p1_volume_standard_error_ratio}}$ standard errors from the exact value.
