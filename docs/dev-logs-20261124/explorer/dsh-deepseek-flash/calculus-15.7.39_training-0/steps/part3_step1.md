# Step 3.1: Multiply the volume by the density

## Reason

The density $\rho = 2$ is constant. A constant factor moves out of an integral. So the mass is the density times the volume. This step needs no new integration.

## Work

$$m = \iiint_{E} \rho\, dV = \iiint_{E} 2\, dV = 2 \iiint_{E} 1\, dV = 2V .$$

Use the volume of Step 2.2:

$$m = 2 \cdot \frac{79}{60} = \frac{79}{30}.$$

A direct triple integral gives the same value. The bounds come from the two descriptions of Step 1.1 and the ceiling of Step 2.1:

$$\int_{0}^{1}\int_{0}^{\sqrt{x}}\int_{0}^{1+x+y} 2\, dz\, dy\, dx .$$

The inner integral is $2(1 + x + y)$. Then the middle integral is $2 s(x)$, and the outer integral is $2V$.

## Result

$m = \frac{79}{30} \approx 2.633333$.

Verification: `part3_verify.py` prints the mass from exact fractions, from a symbolic triple integral, from a numerical triple quadrature, and from a Monte Carlo sample. It also prints the quotient of mass over volume, and that quotient is $2$.
