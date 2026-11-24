## Step 4.2 — Close the body with the three walls and the top face

**Why.** The base and the heights alone give an open surface. The three walls close the sides, and the top face closes the body. Each wall is one inequality with equality, so the walls come from Step 3.2 and not from the picture.

**Step.** Draw in this order:

1. the base triangle $D$ in the plane $y=0$, with the corners $P_0$, $P_1$, and $P_2$;
2. the wall $z=0$, the rectangle $P_4 P_1 P_0 P_3$, which stands on the edge $P_0P_1$;
3. the wall $x=0$, the triangle $P_3 P_0 P_2$, which stands on the edge $P_0P_2$;
4. the wall $x+z=1$, the triangle $P_4 P_2 P_1$, which stands on the edge $P_1P_2$;
5. the top face $y+2z=2$, the triangle $P_4 P_3 P_2$, which closes the body.

**Result.** The closed body is the sketch of the solid: a triangle base, three vertical walls, and one slanted top face. The wall $z=0$ is the tallest wall, because the height $2-2z$ is largest there. The body has five corner points and five faces.

**Check.** `code/part4_verify.py` prints the face table with the inequality, the face name, the corner points, and the area of every face. It also checks that the midpoint of every pair of corner points lies inside the solid, so the body that the five faces close is convex.
