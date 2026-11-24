## Step 1.1 - Read each surface from its own equation

**Reason.** Each equation gives the height $z$ of one surface above a point of the plane $z = 0$.
The lower equation holds the sum $x^{2} + y^{2}$, and that sum is the squared distance from the vertical axis.
So the lower surface is a surface of revolution about the vertical axis, it opens upward, and its lowest point is the origin.
The upper equation holds $5$ minus the same sum, so the upper surface is the same shape turned over, and its highest point is $(0, 0, 5)$.

**Computation.** Write $r^{2} = x^{2} + y^{2}$ for the squared distance from the vertical axis.
The two surfaces then read as follows.

$$ z_{\text{lower}} = r^{2}, \qquad z_{\text{upper}} = 5 - r^{2} $$

The lower height is never negative, so the lower surface stays at or above the plane $z = 0$.
The upper height never passes $5$, so the upper surface stays at or below the plane $z = 5$.

**Result.** The check samples two hundred thousand points of the square $|x| \le 2$, $|y| \le 2$, so it covers all four quadrants, and it prints the largest gap at every sampled point [scan [[check:part1:cylindrical_identity]]].
The gap between $x^{2} + y^{2}$ and $r^{2}$ is $8.882 \times 10^{-16}$ for the lower surface and $1.776 \times 10^{-15}$ for the upper surface, against the tolerance $1.0 \times 10^{-12}$.
The check also compares a finite difference of each height along the radius with the slope $2 r$ and $-2 r$, and the largest gaps are $9.548 \times 10^{-14}$ and $1.199 \times 10^{-13}$, so the rewritten forms are exact rather than approximate.

**Common mistake.** A reader may take the upper equation for a bowl that opens upward, but the minus sign in front of $x^{2} + y^{2}$ makes it open downward from the height $5$.
