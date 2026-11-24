# Part 5. The moment of inertia about the $z$ axis

## Step 5.1. Write the integrand of the moment of inertia

### Reason
The distance from a point to the $z$ axis is $\sqrt{x^{2} + y^{2}}$, so the moment of inertia about that axis is the integral of the squared distance times the density. A reader may take the distance to the plane $z = 0$ as the distance to the axis, but the axis is the line $x = y = 0$, so the squared distance is $x^{2} + y^{2}$ and the coordinate $z$ does not enter the integrand.

### Computation
$$I_{z} = \int_{D} \left(x^{2} + y^{2}\right)\sqrt{x^{2} + y^{2}}\,dV = \int_{D} \left(x^{2} + y^{2}\right)^{3/2} dV.$$
The limits are the limits of Part 1.

### Result
The moment of inertia is an integral of the three coordinates with the integrand $\left(x^{2} + y^{2}\right)^{3/2}$.
`code/part5_verify.py` computes the same integral in two orders and by a stack of cuts.
