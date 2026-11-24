# Step 4.1: Compute the moment about the plane $x = 0$

## Reason

The coordinate $\bar{x}$ measures the distance of the center of mass from the plane $x = 0$. A mass at the point $(x, y, z)$ carries the moment $x\, dm$ about that plane. The moment of the whole solid is the integral of $x \rho$ over $E$. The integral of the moment is the first step toward $\bar{x}$.

## Work

$$M_{yz} = \iiint_{E} x \rho\, dV = \int_{0}^{1}\int_{0}^{\sqrt{x}}\int_{0}^{1+x+y} 2x\, dz\, dy\, dx .$$

The inner integral over $z$ multiplies the integrand by the height $1 + x + y$:

$$M_{yz} = \int_{0}^{1}\int_{0}^{\sqrt{x}} 2x\,(1 + x + y)\, dy\, dx .$$

The inner integral over $y$ is $2x\left[(1 + x)\sqrt{x} + \frac{x}{2}\right] = 2\left(x^{3/2} + x^{5/2} + \frac{x^{2}}{2}\right)$.

Integrate over $x$:

$$\int_{0}^{1} x^{3/2} dx = \frac{2}{5}, \qquad \int_{0}^{1} x^{5/2} dx = \frac{2}{7}, \qquad \int_{0}^{1} \frac{x^{2}}{2} dx = \frac{1}{6}.$$

$$M_{yz} = 2\left(\frac{2}{5} + \frac{2}{7} + \frac{1}{6}\right) = 2\cdot\frac{84 + 60 + 35}{210} = 2\cdot\frac{179}{210} = \frac{179}{105}.$$

## Result

$M_{yz} = \frac{179}{105} \approx 1.704762$.

Verification: `part4_verify.py` prints $M_{yz}$ from exact terms, from a symbolic triple integral, from a numerical triple quadrature, and from a Monte Carlo sample.
