## Step 5.2. Evaluate the moment of inertia

### Reason
The integrand depends on $x$ and $y$ only, so the inner integral over $z$ is the length $1 - y$ of the line at a fixed pair $(x, y)$. That length turns the triple integral into one integral over $x$ of a two-dimensional inner quadrature.

### Computation
$$I_{z} = \int_{-1}^{1} \int_{x^{2}}^{1} \left(1 - y\right)\left(x^{2} + y^{2}\right)^{3/2} dy\,dx.$$

### Result
The moment of inertia is {{p5_inertia}}. The stack of cuts gives {{p5_inertia_alt}}, the one integral in $x$ gives {{p5_inertia_polar}}, and the Monte Carlo mean is {{p5_inertia_mc}} with standard error {{p5_inertia_mc_se}}, a gap of {{p5_inertia_gap}}.
`code/part5_verify.py` prints each value.
