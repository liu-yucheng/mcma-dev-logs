# Step 1.1 — Read the two surfaces

**Part:** 1 — Describe the solid
**Verification:** `code/part1_verify.py`

## Reason

The two equations in the statement are the only information about the solid. Read each equation as a
surface before you compute anything. The shape of each surface tells you which variable can act as
the inner variable of the integral.

## Computation

The first surface is the paraboloid

$$x = 4y^2 + 4z^2 .$$

Write $r^2 = y^2 + z^2$. Then $x = 4r^2$, and the right side is a sum of two squares.

1. The right side is never negative. Therefore $x \ge 0$ on the paraboloid.
2. The right side is zero only at $y = 0$ and $z = 0$. Therefore the lowest point of the paraboloid
   is the origin $(0,0,0)$.
3. The value $x$ grows with the distance from the $x$-axis. Therefore the bowl opens toward the
   positive $x$ direction.

The second surface is the plane

$$x = 4 .$$

The equation does not contain $y$ or $z$. Therefore the plane is vertical, parallel to the
$yz$-plane, and it crosses the $x$-axis at $x = 4$.

## Result

The paraboloid is a bowl with its vertex at the origin, and it opens toward positive $x$. The plane
$x = 4$ is a vertical wall at distance 4 from the $yz$-plane.

## Check

`code/part1_verify.py`, fact 1:

- least value of $x$ on the paraboloid: computed `0.0`, expected `0.0`;
- number of sampled points with $x = 0$: computed `1.0`, expected `1.0`, and that point is the
  origin.

The script samples a $401 \times 401$ grid on $-1.2 \le y,z \le 1.2$.
