## Step 3.1 — The five corner points of the solid

**Why.** A drawing of a solid needs its corner points. A corner point is the common point of three boundary planes that also satisfies all six inequalities. So the corner points follow from the inequalities of Step 1.3, and not from a picture.

**Step.** The six boundary planes are $x=0$, $x=1$, $z=0$, $x+z=1$, $y=0$, and $y+2z=2$. Try every triple of planes, solve the three equations, and keep the point when it satisfies all six inequalities. Five points remain:

$$P_0=(0,0,0),\quad P_1=(1,0,0),\quad P_2=(0,0,1),\quad P_3=(0,2,0),\quad P_4=(1,2,0).$$

**Result.** The solid has five corner points. The plane $x=1$ meets the solid only along the edge from $P_1$ to $P_4$, so it cuts no face. Five planes cut a face, and the sixth plane touches the solid along one edge.

**Check.** `code/part3_verify.py` tries all $20$ triples of the six planes, keeps the points that satisfy the six inequalities, and compares the result with the five points above. It also counts the corner points on the plane $x=1$ and prints the count $2$.
