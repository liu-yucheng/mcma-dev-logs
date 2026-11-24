# Part 3, Step 1: Turn each equality of the limits into one patch of the boundary

## The reason

A closed solid is bounded by surfaces. The sketch must show these surfaces, and it must name each
one by an equation. The equations are already present in the limits: every limit that is an
inequality gives one surface when it becomes an equality.

## The computation

The solid is $R = \{0 \le y \le 2,\ 0 \le z \le 2-y,\ 0 \le x \le 4-y^{2}\}$. The five inequalities
that change with the point give five surfaces:

| Patch | Equality | Surface | Inside the other limits |
| --- | --- | --- | --- |
| $S_1$ | $y = 0$ | the plane $y = 0$ | $0 \le x \le 4$, $0 \le z \le 2$ |
| $S_2$ | $x = 0$ | the plane $x = 0$ | $0 \le y \le 2$, $0 \le z \le 2-y$ |
| $S_3$ | $z = 0$ | the plane $z = 0$ | $0 \le y \le 2$, $0 \le x \le 4-y^{2}$ |
| $S_4$ | $y + z = 2$ | the plane $y + z = 2$ | $0 \le y \le 2$, $0 \le x \le 4-y^{2}$ |
| $S_5$ | $x = 4 - y^{2}$ | the parabolic cylinder $x = 4-y^{2}$ | $0 \le y \le 2$, $0 \le z \le 2-y$ |

The limit $y \le 2$ is an inequality too, but its equality $y = 2$ gives no patch. At $y = 2$ the
other two limits force $z = 0$ and $x = 0$, so the set at that value is the single point
$(0,2,0)$. A single point has no area, and it cannot be a patch of the boundary. Part 2, Step 2
already showed this collapse, and the corner list of the check confirms it.

The area of each patch is a separate computation:

- $S_1$ is the rectangle $4 \times 2$, so its area is $8$.
- $S_2$ is the triangle with legs $2$ and $2$, so its area is $2$.
- $S_3$ is the region under the parabola, so its area is $\int_{0}^{2}(4-y^{2})\,dy = 16/3 = 5.333\ldots$
- $S_4$ is the region of $S_3$ on a plane of slope $\sqrt{2}$, so its area is $(16/3)\sqrt{2} = 7.542\ldots$
- $S_5$ is the region under the parabola on a surface of slope $\sqrt{1+4y^{2}}$, so its area is
  $\int_{0}^{2}(2-y)\sqrt{1+4y^{2}}\,dy = 3.5358\ldots$

## The result

The boundary of the solid is the union of five patches. Their equations are $y = 0$, $x = 0$,
$z = 0$, $y + z = 2$, and $x = 4-y^{2}$. Their areas are $8$, $2$, $16/3$, $(16/3)\sqrt{2}$, and
$3.5358\ldots$. The limit $y = 2$ gives the single point $T = (0,2,0)$ and no patch.

## The check

`code/part3_verify.py`, section "surfaces". For each patch, the script takes 600 points that lie on
the equation of the patch, and it makes three tests. The residual of the equation is $0$ at every
point. Every point satisfies the other four inequalities. A step of $10^{-5}$ along the outward
normal leaves the solid, and a step of the same size inward stays inside the solid. The last two
tests fail for a point that lies on the wrong surface, so they can fail.
