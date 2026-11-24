## Step 3.2 — The five faces and their areas

**Why.** Each inequality that cuts the solid owns one face. The face of an inequality is the set of points of the solid that satisfy that inequality with equality. The corner points of a face are the corner points of the solid that lie on the plane of the face.

**Step.** Take the five cutting planes in turn and collect the corner points on each plane.

| Plane of the face | Corner points of the face | Shape | Area |
| --- | --- | --- | --- |
| $y=0$ | $P_0,\ P_1,\ P_2$ | triangle | $1/2$ |
| $y+2z=2$ | $P_4,\ P_3,\ P_2$ | triangle | $\sqrt{5}/2 \approx 1.118034$ |
| $x=0$ | $P_3,\ P_0,\ P_2$ | triangle | $1$ |
| $z=0$ | $P_4,\ P_1,\ P_0,\ P_3$ | rectangle | $2$ |
| $x+z=1$ | $P_4,\ P_2,\ P_1$ | triangle | $\sqrt{2} \approx 1.414214$ |

**Result.** The solid has five faces: a bottom face, a top face, and three walls. The bottom face is the triangle $D$ in the plane $y=0$. The top face is the triangle $P_4P_3P_2$ in the plane $y+2z=2$, and its area is larger than the area of the bottom face because the plane is not horizontal. The wall $z=0$ is a rectangle, because the height $2-2z$ is $2$ along that whole wall.

**Check.** `code/part3_verify.py` computes each face area twice: once from the corner points, and once as an integral over the same face in its own plane. The two values agree for every face. The script prints each area and the sum of the five areas.
