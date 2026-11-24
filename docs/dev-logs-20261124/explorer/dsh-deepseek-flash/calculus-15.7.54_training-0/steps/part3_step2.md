## Part 3, Step 2: integrate the height first

**Goal.** Reduce the triple integral to one integral in $r$.

**Reason.** The height range depends on $r$ alone, $0 \leq z \leq 1 - r^2$, and the integrand is linear in $z$. The inner integral in $z$ is therefore elementary, and it removes $z$ from the problem without touching the limits in $r$ and $\theta$.

**Computation.** Integrate in $z$ first, then in $\theta$, then in $r$.

$$\int_{0}^{1 - r^2} r^3 z\, dz = r^3 \cdot \frac{(1 - r^2)^2}{2}$$

The angle contributes the factor $2\pi$, because no term contains $\theta$. The radial integral is the area under the curve of Figure 3, $g(r) = \dfrac{r^3 (1 - r^2)^2}{2}$, and it equals $\dfrac{1}{48}$:

$$\int_{0}^{1} \frac{r^3 (1 - r^2)^2}{2}\, dr = \frac{1}{2} \int_{0}^{1} \left(r^3 - 2 r^5 + r^7\right) dr = \frac{1}{2}\left(\frac{1}{4} - \frac{2}{6} + \frac{1}{8}\right) = \frac{1}{48}$$

Therefore the triple integral is $2\pi \cdot \dfrac{1}{48} = \dfrac{\pi}{24}$.

**Result.** $\displaystyle\iiint_{E} \left(x^2 z + y^2 z\right) dV = \frac{\pi}{24} = 0.1308996939$. Figure 3 shows the radial integrand, its shaded area $\dfrac{1}{48}$, and its largest value $0.0458066708$ at $r^2 = \dfrac{3}{7}$.

FIGURE: part3_figure1.png | The radial integrand $g(r) = \dfrac{r^3 (1 - r^2)^2}{2}$ of the triple integral. The shaded area is $\dfrac{1}{48}$, the largest value is $0.0458066708$ at $r^2 = \dfrac{3}{7}$, and the ticks at $0.25$ steps from $r = 0$ to $r = 1$ fix the width of the interval.

**Verification.** The check `[[check:part3:exact_horizontal_route]]` integrates the same function slice by slice, with the moment of each disk, and returns the coefficient $\dfrac{1}{24}$. The check `[[check:part3:integral_cartesian_quadrature]]` integrates over $E$ in Cartesian order and returns $0.1308996939$. The check `[[check:part3:integral_rejection_sample]]` reports $0.13077082$ with a standard error $0.00036251$. The check `[[check:part3:wrong_integrands]]` shows that the wrong integrands of the two common mistakes give $\dfrac{8\pi}{105}$ and $\dfrac{\pi}{6}$, which differ from $\dfrac{\pi}{24}$ by the factors $\dfrac{64}{35}$ and $4$.

**Common mistake.** A reader may take the inner integral in $z$ for the length $1 - r^2$ and drop the factor $z$ of the integrand. The integrand is $r^3 z$, so the inner integral gives $r^3 \dfrac{(1 - r^2)^2}{2}$; the length alone would give the wrong mass $\dfrac{11}{24} + \dfrac{3\pi}{64}$ in place of the correct value.
