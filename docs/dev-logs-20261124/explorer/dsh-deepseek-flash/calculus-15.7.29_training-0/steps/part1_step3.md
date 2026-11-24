# Part 1, Step 1.3: The top of the solid, and the closure of the boundary

Part goal: Turn the two surface equations into one inequality chain, then read the base and the top of the solid from that chain. No figure takes part in this reading.

## Reason

The statement names two surfaces. A reader must check from the equations that no third wall exists, and must find the largest height.

## Computation

The upper bound $4 - x^{2} - 4z^{2}$ is largest where $x = 0$ and $z = 0$. There it equals $4$. So the largest height is $y = 4$, at the single point $(0, 4, 0)$.

The boundary closes because the upper bound falls to $0$ on the ellipse $x^{2} + 4z^{2} = 4$, where the paraboloid meets the base. Above that ellipse the upper bound is negative, so no point of the solid lies there.

## Result

The solid has exactly two pieces of boundary: the paraboloid, and the filled ellipse on the plane $y = 0$. Its largest height is $4$, reached at one point.

## Verification

`code/part1_verify.py` casts 400 rays from interior points and records where each ray leaves the solid. Every exit lies on the plane $y = 0$ or on the paraboloid, with a residual below $1.4 \times 10^{-15}$. No ray leaves through a third surface. The same script compares the largest height of a grid with the value $4$ of the apex.
