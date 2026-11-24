# Step 5.1: Compute the moment about the plane $y = 0$

## Reason

The coordinate $\bar{y}$ needs the moment of the solid about the plane $y = 0$. A mass at the point $(x, y, z)$ carries the moment $y\, dm$ about that plane. So integrate $y \rho$ over $E$.

## Work

$$M_{xz} = \iiint_{E} y \rho\, dV = \int_{0}^{1}\int_{0}^{\sqrt{x}}\int_{0}^{1+x+y} 2y\, dz\, dy\, dx .$$

Integrate over $z$ first. The height is $1 + x + y$:

$$M_{xz} = \int_{0}^{1}\int_{0}^{\sqrt{x}} 2y\,(1 + x + y)\, dy\, dx .$$

The inner integral over $y$ splits into two terms:

$$\int_{0}^{\sqrt{x}} 2(1 + x)y\, dy = (1 + x)x, \qquad \int_{0}^{\sqrt{x}} 2y^{2}\, dy = \frac{2}{3}x^{3/2}.$$

So the inner integral is $x + x^{2} + \frac{2}{3}x^{3/2}$. Integrate over $x$:

$$\int_{0}^{1} x\, dx = \frac{1}{2}, \qquad \int_{0}^{1} x^{2} dx = \frac{1}{3}, \qquad \int_{0}^{1} \frac{2}{3}x^{3/2} dx = \frac{2}{3}\cdot\frac{2}{5} = \frac{4}{15}.$$

$$M_{xz} = \frac{1}{2} + \frac{1}{3} + \frac{4}{15} = \frac{15}{30} + \frac{10}{30} + \frac{8}{30} = \frac{33}{30} = \frac{11}{10}.$$

## Result

$M_{xz} = \frac{11}{10} = 1.1$.

Verification: `part5_verify.py` prints $M_{xz}$ from exact terms, from a symbolic triple integral, from a numerical triple quadrature, and from a Monte Carlo sample.
