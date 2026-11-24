# Part 1, Step 2: Write the definition of the moment of inertia about the z-axis

## Reason

The moment of inertia of a body about an axis measures how far the mass of the body lies from that
axis. Each small piece of mass $\rho\,dV$ contributes its mass multiplied by the square of its
distance $d$ to the axis. For a body of constant density $k$ the definition of Section 15.7 gives

$$I_{z} = \iiint_{E} d^{2}\,k\,dV .$$

The statement of the problem gives the density as the constant $k$ and gives no other property of
the material.

## Computation

For a point $(x,y,z)$ the nearest point of the $z$-axis is $(0,0,z)$, so the distance to the axis is

$$d = \sqrt{(x-0)^{2}+(y-0)^{2}+(z-z)^{2}} = \sqrt{x^{2}+y^{2}} .$$

Insert this distance into the definition. The density $k$ is constant, so it leaves the integral
sign.

## Result

The number that the problem asks for is

$$I_{z} = k \iiint_{E} \left(x^{2}+y^{2}\right) dV .$$

The statement prints no numerical value for $k$ and no numerical value for $h$, so the answer is an
expression in these two symbols. The solid has a positive volume only when $h > 0$, and the words
"solid cone" carry that condition.

Verification: `code/part1_verify.py` checks the geometric part of this step, the area of the slice
that the distance $d$ produces. At the heights $z = 0.25$, $z = 0.50$, and $z = 0.75$ the area from
quadrature is 0.196350, 0.785398, and 1.767146, and the area measured from the fraction of sampled
points inside the slice is 0.197213, 0.785367, and 1.767861 with standard errors 0.001205, 0.002151,
and 0.002464. Each measured area lies within four standard errors of $\pi z^{2}$, which is the area
of the disk that the distance $d$ describes at that height.

> **Part 1 answer.** $I_{z} = k \iiint_{E} \left(x^{2}+y^{2}\right) dV$, with $E$ the cone of apex
> $(0,0,0)$, base disk of radius $h$ in the plane $z = h$, and wall $z = \sqrt{x^{2}+y^{2}}$.
