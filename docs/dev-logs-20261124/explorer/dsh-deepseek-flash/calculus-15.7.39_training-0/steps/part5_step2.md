# Step 5.2: Divide the moment by the mass to get $\bar{y}$

## Reason

The second coordinate of the center of mass is the moment about the plane $y = 0$ divided by the mass. This is the same rule as Step 4.2, applied to the other axis.

## Work

$$\bar{y} = \frac{M_{xz}}{m} = \frac{11/10}{79/30} = \frac{11}{10}\cdot\frac{30}{79} = \frac{330}{790} = \frac{33}{79}.$$

The value $79$ is prime, and $33 = 3 \cdot 11$ is not a multiple of $79$. So the fraction is in lowest terms.

A numerical check: $33 \div 79 = 0.417722$.

The pair $(\bar{x}, \bar{y}) = (0.647378, 0.417722)$ must lie in $D$. Check the upper bound: $\bar{y}^{2} = 0.174491$ and $\bar{x} = 0.647378$. So $\bar{y}^{2} \leq \bar{x}$, and the pair lies under the curve $y = \sqrt{x}$.

## Result

$\bar{y} = \frac{33}{79} \approx 0.417722$.

Verification: `part5_verify.py` prints $\bar{y}$ from the fraction division and from a symbolic moment over a symbolic mass. It also compares $\bar{y}^{2}$ with $\bar{x}$.
