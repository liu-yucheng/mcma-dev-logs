## Step 4.1 — Compute the moment of inertia about the $z$ axis

**Reason.** The moment of inertia about the $z$ axis is the integral of $(x^{2} + y^{2})\rho$ over the solid, because the distance of a point from that axis is $\sqrt{x^{2} + y^{2}}$ and the density multiplies the squared distance. The integrand is therefore $(x^{2} + y^{2})^{2}$, which is a quartic in $x$ and $y$. A reader may replace the solid by the cylinder of radius $3$, but the limits $0 \le x \le y/3$ give the smaller value ${{iz}}$, while the cylinder of radius $3$ gives ${{iz_at_cylinder_radius}}$.

**Computation.** The inner integral is

$$ \int_{0}^{y/3}\left(x^{2} + y^{2}\right)^{2} dx = \frac{1}{5}\left(\frac{y}{3}\right)^{5} + \frac{2}{3}\left(\frac{y}{3}\right)^{3}y^{2} + \frac{y^{4}}{3}\cdot y = \frac{436\,y^{5}}{1215} . $$

The $z$ integral multiplies this value by $\sqrt{9 - y^{2}}$, and the substitution $y = 3t$ gives

$$ I_{z} = \frac{436}{1215}\cdot 3^{{{substitution_exponent}}}\int_{0}^{1} t^{5}\sqrt{1 - t^{2}}\,dt = \frac{436}{1215}\cdot {{substitution_ratio}} \cdot \frac{1}{2}B\!\left(3, \frac{3}{2}\right) = {{iz}} . $$

**Verification.** `code/part4_verify.py` compares the inner polynomial with a direct antiderivative and a Gauss rule at three values of $y$. The printed rows are

{{table:inner_iz}}

The script then computes $I_{z}$ by the Beta function, by quadrature in the order $dx\,dz\,dy$, by quadrature in the order $dz\,dy\,dx$, and by a uniform sample. The four routes print ${{iz_closed}}$ from the Beta function, ${{iz}}$ from the order $dx\,dz\,dy$ that uses the inner values of the table above, ${{iz_alternate}}$ from the order $dz\,dy\,dx$, and ${{iz_monte_carlo}}$ from the sample with the error ${{iz_monte_carlo_error}}$, which is ${{iz_sigma}}$ standard errors from the quadrature. The same script integrates the density alone as a second route to the mass and prints ${{repeated_mass}}$.

**Result.** The moment of inertia is $I_{z} = {{iz}} \to {{iz_3dp}}$, and the mean squared radius is $I_{z} / M = {{mean_square_radius}}$. The check named "the radius of the cylinder overstates the inertia" prints ${{iz_at_cylinder_radius}}$ for the cylinder and ${{iz}}$ for the solid.
