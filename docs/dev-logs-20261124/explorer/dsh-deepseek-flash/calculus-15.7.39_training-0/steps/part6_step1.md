# Step 6.1: Compute the moment about the plane $z = 0$

## Reason

The coordinate $\bar{z}$ needs the moment of the solid about the plane $z = 0$. A mass at the point $(x, y, z)$ carries the moment $z\, dm$ about that plane. So integrate $z \rho$ over $E$.

## Work

$$M_{xy} = \iiint_{E} z \rho\, dV = \int_{0}^{1}\int_{0}^{\sqrt{x}}\int_{0}^{1+x+y} 2z\, dz\, dy\, dx .$$

The inner integral over $z$ gives $\left[z^{2}\right]_{0}^{1+x+y} = (1 + x + y)^{2}$:

$$M_{xy} = \int_{0}^{1}\int_{0}^{\sqrt{x}} (1 + x + y)^{2}\, dy\, dx .$$

Integrate over $y$. Write $a = 1 + x$ and $b = \sqrt{x}$. Then

$$\int_{0}^{b} (a + y)^{2} dy = \frac{(a + b)^{3} - a^{3}}{3} = a^{2}b + ab^{2} + \frac{b^{3}}{3}.$$

In terms of $x$ this is $(1 + x)^{2}\sqrt{x} + (1 + x)x + \frac{1}{3}x^{3/2}$. Integrate the three terms over $[0, 1]$:

$$\int_{0}^{1}(1 + x)^{2}\sqrt{x}\, dx = \frac{2}{3} + \frac{4}{5} + \frac{2}{7} = \frac{184}{105}, \qquad \int_{0}^{1}(x + x^{2})\, dx = \frac{1}{2} + \frac{1}{3} = \frac{5}{6},$$

$$\int_{0}^{1}\frac{1}{3}x^{3/2} dx = \frac{1}{3}\cdot\frac{2}{5} = \frac{2}{15}.$$

Add the three exact terms with the common denominator $210$:

$$M_{xy} = \frac{368}{210} + \frac{175}{210} + \frac{28}{210} = \frac{571}{210}.$$

## Result

$M_{xy} = \frac{571}{210} \approx 2.719048$.

Verification: `part6_verify.py` prints $M_{xy}$ from exact terms, from a symbolic triple integral, and from a numerical triple quadrature.
