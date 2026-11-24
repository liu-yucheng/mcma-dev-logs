## Step 2.3. Stack the sections of Step 2.1

### Reason
The solid is the union of the cuts at fixed $z$, and two cuts at different heights do not overlap, so the volume is the integral of the cut area over $z$. The same argument gives the mass in Part 3, with the density in place of $1$.

### Computation
$$V = \int_{0}^{1} A(z)\,dz = \int_{0}^{1} \frac{4}{3}\left(1 - z\right)^{3/2} dz.$$
The integral of $(1 - z)^{3/2}$ over $z$ from $0$ to $1$ is $\frac{2}{5}$, so the volume is $\frac{8}{15}$.

### Result
The stack of the section areas gives {{p2_stacked_area}}, which agrees with the volume of Step 1.3.
`code/part2_verify.py` compares the stacked area with the volume of the order $dz\,dy\,dx$.
