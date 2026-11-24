## Step 4.2 - Read the drawing and check its scale

**Reason.** A drawing of a solid is a measurement only when each axis carries a scale, because a picture without numbers fixes no size.
The problem asks for a graphing device drawing, and that drawing must let a reader recover the radius $\sqrt{\frac{5}{2}}$ and the heights $0$ and $5$ from the marks on the axes.
So the marks of the picture are compared with the numbers of the derivation, and the comparison is part of the answer.

**Computation.** The horizontal axes carry the marks $1$ and $2$, and the vertical axis carries the marks $1$, $3$ and $5$.
The rim of the body reaches the squared radius $\frac{5}{2}$, so the rim sits between the horizontal marks $1$ and $2$, closer to $2$.
The top of the body sits exactly at the vertical mark $5$, and the bottom sits at the foot of the vertical axis, where the value is $0$.

**Result.** The check reads the mark lists from the drawing code and compares them with the numbers of the derivation [scan [[check:part4:scales_agree]]].
The horizontal mark list is $(1.0, 2.0)$, the vertical mark list is $(1.0, 3.0, 5.0)$, and the squared radius of the rim equals $\frac{5}{2}$ to machine precision.
The area of the widest section in the drawing equals $\pi \frac{5}{2} = 7.853981634$, so the scale of the picture and the derivation agree.

**Common mistake.** A reader may take the distance between two marks for the radius of the circle, because the rim ends near the mark $2$, but the rim ends at $\sqrt{\frac{5}{2}} = 1.5811$, and the mark $2$ lies outside the body.

**Answer of Part 4.** The drawing of the answer is Figure 3: the closed body between $z = x^{2} + y^{2}$ and $z = 5 - x^{2} - y^{2}$ with the meeting circle drawn heavy, the horizontal marks $1$ and $2$, and the vertical marks $1$, $3$ and $5$.
