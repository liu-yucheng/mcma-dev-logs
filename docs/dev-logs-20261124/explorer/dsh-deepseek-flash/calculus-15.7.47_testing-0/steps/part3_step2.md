## Step 3.2. Evaluate the mass and check it two ways

### Reason
A value of a triple integral needs a second computation that does not repeat the first one. The first computation nests Gauss-Legendre rules in the order $dx\,dz\,dy$. The second one reduces the inner two integrations to an antiderivative in $y$ and integrates the result over $x$ alone, and a Monte Carlo mean gives a third value with its own error.

### Computation
The three-dimensional quadrature gives the mass. The Monte Carlo mean uses two million uniform samples of the box around the solid and the indicator of the solid.

### Result
The mass is {{p3_mass}}, the nested quadrature gives {{p3_mass_order}}, and the Monte Carlo mean is {{p3_mass_mc}} with standard error {{p3_mass_mc_se}}, a gap of {{p3_mass_mc_gap}}.
The density at the corner $(1, 1, 0)$ is {{p3_density_corner}}, that is $\sqrt{2}$.
`code/part3_verify.py` prints each value and each gap.
