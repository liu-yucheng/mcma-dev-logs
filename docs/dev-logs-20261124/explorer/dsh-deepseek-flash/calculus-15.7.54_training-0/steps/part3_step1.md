## Part 3, Step 1: write the integrand in cylindrical coordinates

**Goal.** Prepare the triple integral of $f(x, y, z) = x^2 z + y^2 z$ over $E$.

**Reason.** The function contains $x^2 + y^2$, and the body is a solid of revolution about the $z$ axis. Cylindrical coordinates therefore simplify both the function and the region at the same time, and the height range that Step 1.1 gives stays valid.

**Computation.** Factor the function, $f = (x^2 + y^2) z$, then substitute $x^2 + y^2 = r^2$ and $dV = r\, dz\, dr\, d\theta$.

$$f(x, y, z)\, dV = r^2 z \cdot r\, dz\, dr\, d\theta = r^3 z\, dz\, dr\, d\theta$$

The region becomes $0 \leq \theta \leq 2\pi$, $0 \leq r \leq 1$, $0 \leq z \leq 1 - r^2$.

**Result.** The triple integral that remains is

$$\iiint_{E} \left(x^2 z + y^2 z\right) dV = \int_{0}^{2\pi} \int_{0}^{1} \int_{0}^{1 - r^2} r^3 z\, dz\, dr\, d\theta$$

**Verification.** The check `[[check:part3:exact_cylindrical_route]]` forms the coefficient of the $r$ integral with exact fractions and compares it with the coefficient of the horizontal route of Step 3.2; both return $\dfrac{1}{24}$ for the whole integral divided by $\pi$.

**Common mistake.** A reader may substitute $x^2 + y^2 = r^2$ and keep the plane element $dx\, dy$, which drops the factor $r$ of the Jacobian. The volume element in cylindrical coordinates is $r\, dz\, dr\, d\theta$, so the integrand is $r^3 z$ and not $r^2 z$.
