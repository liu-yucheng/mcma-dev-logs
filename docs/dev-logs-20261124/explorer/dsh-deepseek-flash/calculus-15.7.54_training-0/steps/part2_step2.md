## Part 2, Step 2: repeat the volume in cylindrical coordinates

**Goal.** Obtain the same volume from a second order of integration, so that the answer does not depend on one order.

**Reason.** The body is a surface of revolution about the $z$ axis, and the two surfaces depend on $x^2 + y^2$ alone. Cylindrical coordinates therefore turn the disk $D$ into the rectangle $0 \leq r \leq 1$, $0 \leq \theta \leq 2\pi$, and the height becomes $0 \leq z \leq 1 - r^2$.

**Computation.** With the volume element $r\, dz\, dr\, d\theta$ and the height range of Step 1.1,

$$V(E) = \int_{0}^{2\pi} \int_{0}^{1} \int_{0}^{1 - r^2} r\, dz\, dr\, d\theta = 2\pi \int_{0}^{1} r (1 - r^2)\, dr = 2\pi \left[ \frac{r^2}{2} - \frac{r^4}{4} \right]_{0}^{1} = 2\pi \cdot \frac{1}{4} = \frac{\pi}{2}$$

**Result.** Both orders give $V(E) = \dfrac{\pi}{2}$. The coefficient of $\pi$ in the radial route is $\dfrac{1}{4}$, and the factor $2\pi$ of the angle carries it to $\dfrac{\pi}{2}$.

**Verification.** The check `[[check:part2:exact_routes]]` computes the two coefficients with exact fractions. The radial route returns $\dfrac{1}{2}$, and the height route returns $\dfrac{1}{2}$. The check `[[check:part2:volume_rejection_sample]]` draws $400000$ points in the box $[-1, 1] \times [-1, 1] \times [0, 1]$ of volume $4$ and reports $1.57336$ with a standard error $0.0030895$, so the sample agrees with $\dfrac{\pi}{2}$ inside one standard error.

**Common mistake.** A reader may drop the Jacobian factor $r$, because the limits already contain $r$. The limits $0 \leq r \leq 1$ are a length, and the area element of the disk is $r\, dr\, d\theta$; without the factor $r$ the same limits give $\dfrac{2\pi}{3}$, which is too large by the factor $\dfrac{4}{3}$.
