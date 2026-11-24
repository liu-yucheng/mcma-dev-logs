## Step 3.2 — Compute $\bar{z}$ with exact fractions and read the center of mass

**Reason.** The coordinate $\bar{z}$ is the integral of $z\rho$ over the solid divided by the mass. The density does not contain $z$, so the inner $z$ integral is $\int_{0}^{\sqrt{9-y^{2}}} z\,dz = \frac{9 - y^{2}}{2}$, and every power of $y$ that remains is even. A reader may take the mean height of the quarter disc for $\bar{z}$, but the limits $0 \le x \le y/3$ give a solid that is thinner near $y = 3$, and the value ${{z_bar}}$ follows from them.

**Computation.** The numerator is

$$ \int_{E} z\rho \, dV = \int_{0}^{3}\frac{28y^{3}}{81}\cdot\frac{9 - y^{2}}{2}\,dy . $$

Write $y = 3t$ again. The integral becomes $\frac{28}{81}\cdot\frac{81}{2}\cdot 243\int_{0}^{1} t^{3}(1 - t^{2})\,dt$, and $\int_{0}^{1} t^{3}(1 - t^{2})\,dt = \frac{1}{4} - \frac{1}{6} = \frac{1}{12}$. Hence the numerator is $\frac{21}{2}$ and

$$ \bar{z} = \frac{21/2}{56/5} = \frac{15}{16} = {{z_bar}} . $$

The division uses exact fractions, because the digits of the floating route near the third decimal cannot be trusted to round. `code/part3_verify.py` prints the exact fraction as ${{z_bar_exact}}$, and the third decimal of that value is ${{z_bar_3dp}}$.

**Verification.** `code/part3_verify.py` computes the numerator of $z\rho$ from the closed form, from the order $dx\,dz\,dy$, from the order $dz\,dy\,dx$, and from exact fractions; the four routes print ${{numerator_z}}$ and their largest spread is ${{numerator_z_max_difference_latex}}$. The check named "the centroid of the projection misses z bar" prints ${{wrong_z_disc_centroid}}$ for the mean height of the quarter disc and ${{z_bar}}$ for the correct value. The coordinate checks compare each closed route with a uniform sample of the solid, and the largest deviation is ${{coordinate_sigma_max}}$ standard errors, below the factor four that the script allows.

**Result.** The center of mass is

$$ \left(\bar{x}, \bar{y}, \bar{z}\right) = \left({{x_bar_3dp}},\ {{y_bar_3dp}},\ {{z_bar_3dp}}\right) . $$

Figure 3 draws a sample of the solid coloured by the density, with this point marked inside the sample.

{{figure:part3_figure1|A sample of ${{sample_points_kept}}$ points of the solid, coloured by the density $\rho = x^{2} + y^{2}$. The star is the center of mass $({{x_bar_3dp}}, {{y_bar_3dp}}, {{z_bar_3dp}})$ from `code/part3_verify.py`.}}
