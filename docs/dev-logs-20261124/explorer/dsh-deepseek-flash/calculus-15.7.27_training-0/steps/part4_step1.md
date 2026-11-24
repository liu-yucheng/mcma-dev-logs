## Step 4.1 — Draw the base, then raise each point by the height

**Why.** The drawing follows the reading of the limits in the same order. The outer two limits give the base in the plane $y=0$. The innermost limit gives the height above each base point. Draw the base first, and draw the height second.

**Step.** Draw the axes with $y$ pointing up. Mark the base triangle $D$ in the plane $y=0$ with the corners $(0,0)$, $(1,0)$, and $(0,1)$ in the $xz$-plane. Then, above a base point $(x,z)$, draw a vertical segment from $y=0$ up to $y=2-2z$. The upper ends of these segments sweep the top face.

**Result.** The base is a right triangle with two sides of length $1$ along the axes, and the height falls from $2$ on the edge $z=0$ to $0$ at the point $P_2=(0,0,1)$. Above the point $(1/4, 2/5)$ the height is $2-2\cdot 2/5 = 6/5$. Figure 2 shows the base and one level line, and Figure 3 carries the height bar at that point.

**Check.** `code/part3_verify.py` tests $200$ points of the height segment at $(1/4, 2/5)$ against the six inequalities, and every point passes. It compares the length of the segment with $2-2z = 6/5$, and it compares the drawn base triangle with the section $y=0$ of the solid.
