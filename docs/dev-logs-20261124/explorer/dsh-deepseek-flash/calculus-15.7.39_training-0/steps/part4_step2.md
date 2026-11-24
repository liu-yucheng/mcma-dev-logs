# Step 4.2: Divide the moment by the mass to get $\bar{x}$

## Reason

The center of mass is the point where the whole mass acts. Its coordinate $\bar{x}$ is the moment $M_{yz}$ divided by the mass $m$. The division is exact while both numbers are fractions.

## Work

$$\bar{x} = \frac{M_{yz}}{m} = \frac{179/105}{79/30} = \frac{179}{105}\cdot\frac{30}{79} = \frac{179 \cdot 30}{105 \cdot 79}.$$

Cancel the common factor $15$ in $30$ and $105$: $\frac{30}{105} = \frac{2}{7}$. So

$$\bar{x} = \frac{179 \cdot 2}{7 \cdot 79} = \frac{358}{553}.$$

The value $553 = 7 \cdot 79$ has no common factor with $358 = 2 \cdot 179$. So the fraction is in lowest terms.

A numerical check: $358 \div 553 = 0.647378$.

The value lies inside the $x$-extent $[0, 1]$ of $D$, as a coordinate of a point of $E$ must.

## Result

$\bar{x} = \frac{358}{553} \approx 0.647378$.

Verification: `part4_verify.py` prints $\bar{x}$ from the fraction division, from a symbolic moment over a symbolic mass, and from the quadrature moment over the exact mass.
