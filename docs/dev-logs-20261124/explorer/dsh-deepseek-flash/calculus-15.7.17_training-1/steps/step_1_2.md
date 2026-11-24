# Step 1.2 — Find where the two surfaces meet

**Part:** 1 — Describe the solid
**Verification:** `code/part1_verify.py`

## Reason

The solid lies between the two surfaces. A point belongs to the solid only where the paraboloid is
below the plane. Solve the equality to find the curve that limits the solid. The shadow of that
curve on the $yz$-plane gives the region of the double integral.

## Computation

Set the two right sides equal:

$$4y^2 + 4z^2 = 4 .$$

Divide by 4:

$$y^2 + z^2 = 1 .$$

This equation does not contain $x$, and the common value is $x = 4$. Therefore the intersection is
the circle of radius 1 that lies in the plane $x = 4$.

The condition $4(y^2 + z^2) \le x \le 4$ gives $4(y^2+z^2) \le 4$, hence $y^2 + z^2 \le 1$. Therefore
every point of the solid lies above the unit disk

$$D = \{(y,z) : y^2 + z^2 \le 1\}$$

in the $yz$-plane, and every point above $D$ between the two surfaces belongs to the solid.

The area of $D$ is $\pi r^2 = \pi$.

## Result

The two surfaces meet on the circle $y^2 + z^2 = 1$ in the plane $x = 4$. The projection of the solid
on the $yz$-plane is the unit disk $D$, and its area is $\pi$.

## Check

`code/part1_verify.py`, fact 2 and fact 3:

- radius from $4r^2 = 4$: computed `1.0`, expected `1.0`;
- largest $\lvert 4r^2 - 4 \rvert$ on the circle $r = 1$: computed `8.88e-16`, expected `0.0`
  within `1.0e-12`;
- $\lvert 4r^2 - 4 \rvert$ at $r = 0.98$: computed `0.1584`, expected `0.1584`; at $r = 1.02$:
  computed `0.1616`, expected `0.1616`. A circle of another radius does not meet the plane;
- area of $D$ from $2{,}000{,}000$ random points: computed `3.14085`, expected `3.14159`, standard
  error `1.63e-3`;
- points where the description "$4(y^2+z^2) \le x \le 4$" and the description "above $D$ and below
  the plane" differ: computed `0`, expected `0`.
