# Part 6, Step 1: The projection of the silo on the plane $y=0$

## Reason

A drawing device draws curves, and the silhouette of a round body is the outline of its
projection. To obtain that outline, drop one coordinate and keep the two that the drawing paper
carries. The plane of the paper is $y=0$, so the projection keeps $x$ and $z$ and drops $y$.

## Computation

A pair $(x,z)$ belongs to the projection when some height $y$ completes it to a point of the
body. The body allows every $y$ with $x^{2}+y^{2}\le 9$ at the height $z$ below the ceiling, and
such a $y$ exists exactly when $x^{2}\le 9$. The ceiling of Step 1.2 then applies with
$r^{2}=x^{2}$, because the widest section at the height $z$ has $y=0$:

$$|x|\le 3,\qquad 0\le z\le 10+\sqrt{9-x^{2}} .$$

Split that region at the height $z=10$. Below the split the ceiling exceeds $10$, so the pairs
with $|x|\le 3$ and $0\le z\le 10$ all belong: that is the rectangle $6$ wide and $10$ high.
Above the split the condition $z\le 10+\sqrt{9-x^{2}}$ is the same as
$x^{2}+(z-10)^{2}\le 9$: that is the half disk of radius $3$ about $(0,10)$.

## Result

The projection on the plane $y=0$ is the union of the rectangle $|x|\le 3$, $0\le z\le 10$ and
the half disk $x^{2}+(z-10)^{2}\le 9$, $z\ge 10$. The right panel of Figure 1 draws exactly
those two regions, and the dashed line marks their common edge at $z=10$, which is interior to
the projection and therefore not part of the outline. The outline is the base, the two vertical
sides, and the semicircular arc.

## Common mistake

A reader may call this region the projection on the plane $x=0$, but a projection that drops the
coordinate $y$ lies on the plane $y=0$; the panel label of Figure 1 and the docstring of
`code/part6_verify.py` both name the plane $y=0$.

## Verification

Verification script: `code/part6_verify.py` check C1 tests the ceiling inequality against the union of the rectangle
and the half disk on 216931 points of a grid and prints 0 mismatches. Check C2 scans the
inequality along seven heights and prints a maximum distance of $5.662\times 10^{-15}$ between
the scanned silhouette and the meridian formula $3\cos\varphi$ of the cap. Check C3 tests the
nodes of all three meshes against their own equations and prints a residual of
$7.105\times 10^{-15}$.
