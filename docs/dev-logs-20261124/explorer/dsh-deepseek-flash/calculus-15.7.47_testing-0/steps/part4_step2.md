## Step 4.2. Compute the other two moments

### Reason
The second and the third moment use the same limits as the mass, with the factor $y$ or $z$ in the integrand. The center of mass is the quotient of a moment by the mass, so each coordinate needs its own moment and its own quotient.

### Computation
$$M_{xz} = \int_{D} y\sqrt{x^{2} + y^{2}}\,dV, \qquad M_{xy} = \int_{D} z\sqrt{x^{2} + y^{2}}\,dV.$$
The moment of $z$ uses the inner integral $\int_{0}^{1 - y} z\,dz = \frac{1}{2}\left(1 - y\right)^{2}$.

### Result
The moments are {{p4_moment_y}} and {{p4_moment_z}}, so $\bar{y} = $ {{p4_ybar}} and $\bar{z} = $ {{p4_zbar}}.
The same two quotients from a stack of cuts give {{p4_ybar_alt}} and {{p4_zbar_alt}}, and `code/part4_verify.py` compares each pair.
