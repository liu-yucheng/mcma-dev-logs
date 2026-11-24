## Step 3.1 — Compute the numerators of $\bar{x}$ and $\bar{y}$

**Reason.** The coordinate $\bar{x}$ is the integral of $x\rho$ over the solid divided by the mass, and $\bar{y}$ is the integral of $y\rho$ divided by the same mass. The numerator of $\bar{x}$ has the extra factor $x$ under the inner integral, so it is a quartic in $y$, and the numerator of $\bar{y}$ has the extra factor $y$, so it carries one more power of $y$ than the mass does. A reader may divide the numerator of $x\rho$ by the volume instead of the mass, but the mass $M = {{mass}}$ is the divisor that the definition gives.

**Computation.** The inner integral of $x\rho$ is $\int_{0}^{y/3} x(x^{2} + y^{2})\,dx = \frac{y^{4}}{324} + \frac{y^{4}}{18} = \frac{19y^{4}}{324}$, and the inner integral of $y\rho$ is $y$ times the value of Step 2.1, $\frac{28y^{4}}{81}$. After the $z$ and $y$ integrals,

$$ \int_{E} x\rho \, dV = \frac{171\pi}{128} = {{numerator_x}}, \qquad \int_{E} y\rho \, dV = \frac{63\pi}{8} = {{numerator_y}} . $$

**Verification.** `code/part3_verify.py` computes each numerator from its closed form, from quadrature in the order $dx\,dz\,dy$, from quadrature in the order $dz\,dy\,dx$, and from a uniform sample. The printed rows are

{{table:numerators}}

Each row prints the closed form, the second order, the sample value, the error of the sample, and the deviation in standard errors.

**Result.** The numerators are $\int x\rho\,dV = {{numerator_x}}$ and $\int y\rho\,dV = {{numerator_y}}$, so

$$ \bar{x} = \frac{{{numerator_x}}}{{{mass}}} = {{x_bar}} \to {{x_bar_3dp}}, \qquad \bar{y} = \frac{{{numerator_y}}}{{{mass}}} = {{y_bar}} \to {{y_bar_3dp}} . $$

The check named "the shortcut that divides by the volume misses x bar" of `code/part3_verify.py` prints ${{wrong_x_with_volume}}$ for the wrong divisor $V$ and ${{x_bar}}$ for the correct divisor $M$.
