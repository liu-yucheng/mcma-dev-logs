# Part 2, Step 1: Use cylindrical coordinates

## Reason

Every slice of the solid at a fixed height is a disk about the $z$-axis (Part 1, Step 1). A
coordinate that measures the distance from the axis and a coordinate that measures the angle around
the axis therefore follow the shape of the body. The two new coordinates are

$$x = r\cos\theta, \qquad y = r\sin\theta, \qquad z = z .$$

The symbol $r$ is the distance to the $z$-axis and the symbol $\theta$ is the angle in the $xy$
plane, so the integrand $x^{2}+y^{2}$ becomes the single square $r^{2}$.

## Computation

The square of the distance to the axis is

$$x^{2}+y^{2} = r^{2}\cos^{2}\theta + r^{2}\sin^{2}\theta = r^{2} .$$

The volume element of the map $(r,\theta,z) \mapsto (x,y,z)$ is the absolute value of the Jacobian
determinant,

$$\left|\frac{\partial(x,y,z)}{\partial(r,\theta,z)}\right| = r , \qquad dV = r\,dz\,dr\,d\theta .$$

The factor $r$ is not $1$: a step $d\theta$ at radius $r$ covers the arc length $r\,d\theta$.

## Result

In cylindrical coordinates the integrand of Part 1 is $k r^{2}$ and the volume element is
$r\,dz\,dr\,d\theta$. The moment of inertia becomes

$$I_{z} = \iiint k\,r^{3}\,dz\,dr\,d\theta .$$

Verification: `code/part2_verify.py` compares the analytic Jacobian $r$ with a finite-difference
Jacobian over 200000 random points, and the largest relative gap is 2.581e-10. The same script
compares $x^{2}+y^{2}$ with $r^{2}$ over the same points, and the largest gap is 2.220e-16. It also
compares the distance to the axis computed by a cross product with $z$ on the wall of the cone, and
the largest gap is 1.110e-16.
