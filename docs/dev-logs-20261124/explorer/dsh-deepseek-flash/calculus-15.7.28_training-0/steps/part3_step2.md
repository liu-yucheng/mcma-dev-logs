# Part 3, Step 2: Find the corners and the edges, and show that the boundary is closed

## The reason

A sketch of five separate patches can still be wrong at the joins. The patches must meet along
shared edges, and the edges must meet at shared corners. The corners and the edges are also the
points and the lines that a reader uses to check the shape of the drawing.

## The computation

A corner is a point where three of the five equations hold at the same time. Take each triple in
turn and keep the point inside the solid:

| Corner | Point | Equations that hold there |
| --- | --- | --- |
| $A$ | $(0,0,0)$ | $x = 0$, $y = 0$, $z = 0$ |
| $B$ | $(4,0,0)$ | $y = 0$, $z = 0$, $x = 4-y^{2}$ |
| $C$ | $(4,0,2)$ | $y = 0$, $y + z = 2$, $x = 4-y^{2}$ |
| $D$ | $(0,0,2)$ | $x = 0$, $y = 0$, $y + z = 2$ |
| $T$ | $(0,2,0)$ | $x = 0$, $z = 0$, $y + z = 2$, and $x = 4-y^{2}$ |

The corner $T$ satisfies four equations, and the other four corners satisfy three each. There are
five corners and no sixth one.

An edge is the set where two patches meet. There are eight edges:

| Edge | From | To | Equations | Length |
| --- | --- | --- | --- | --- |
| $e_1$ | $A$ | $B$ | $y = 0$, $z = 0$ | $4$ |
| $e_2$ | $B$ | $C$ | $y = 0$, $x = 4-y^{2}$ | $2$ |
| $e_3$ | $C$ | $D$ | $y = 0$, $y + z = 2$ | $4$ |
| $e_4$ | $D$ | $A$ | $y = 0$, $x = 0$ | $2$ |
| $e_5$ | $A$ | $T$ | $x = 0$, $z = 0$ | $2$ |
| $e_6$ | $D$ | $T$ | $x = 0$, $y + z = 2$ | $2\sqrt{2} = 2.828\ldots$ |
| $e_7$ | $B$ | $T$ | $z = 0$, $x = 4-y^{2}$ | $4.646784$ |
| $e_8$ | $C$ | $T$ | $y + z = 2$, $x = 4-y^{2}$ | $5.124014$ |

The two curved edges are $e_7$ and $e_8$. Their lengths are arc lengths of the parabola
$x = 4-y^{2}$, and each of them needs its own integral.

The boundary is closed when every edge belongs to exactly two patches. The table gives two patches
for each edge, and the corner table gives three or four patches for each corner. The five patches
therefore close the boundary of the solid.

## The result

The solid has five corners $A$, $B$, $C$, $D$, $T$ and eight edges. The corner $T$ lies on four
patches, and each other corner lies on three. Every edge lies on exactly two patches, so the five
patches close the boundary.

## The check

`code/part3_verify.py`, section "corners". The script holds a list of the five surfaces. For each
corner it counts the surfaces whose equation the point satisfies, and it reports $3$, $3$, $3$,
$3$, and $4$ in the order $A$, $B$, $C$, $D$, $T$.

`code/part3_verify.py`, section "edges". For each edge, the script takes 401 points along the edge.
The residual of each of the two named equations is $0$. The residual of each of the other three is
at least $1.414$, so the edge does not lie on a third patch. The two end points match the named
corners exactly. The arc length and the chord length of the same 401 points agree within
$10^{-4}$.
