# 3.1 The three first moments

A first moment integrates the density times one coordinate. Reason: the coordinate of the center of mass is the quotient of that moment by the mass, and the moment of a mass element is its mass times its distance from the coordinate plane.

$$M_{yz}=\iiint_E x\rho\,dV, \qquad M_{xz}=\iiint_E y\rho\,dV, \qquad M_{xy}=\iiint_E z\rho\,dV$$

Each product of two factors splits into monomials, and every monomial uses one rule for the two inner integrations. Reason: the inner integral in $z$ of $z^c$ is $y^{c+1}/(c+1)$, so the length $y$ of the inner interval raises the power of $y$ by one more.

$$\iiint_E x^a y^b z^c\,dV=\frac{1}{(c+1)(b+c+2)}\int_0^1 x^a\left(1-x^2\right)^{(b+c+2)/2}dx$$

The moment $M_{yz}$ becomes four monomial integrals, and each one follows from one polynomial integral of the same two families as Step 2.2.

$$M_{yz}=\int_E x\,dV+\int_E x^2\,dV+\int_E xy\,dV+\int_E xz\,dV=\frac{1}{8}+\frac{1}{15}+\frac{1}{15}+\frac{1}{30}=\frac{7}{24}$$

The moment $M_{xz}$ uses the same rule with the factor $y$.

$$M_{xz}=\int_E y\,dV+\int_E xy\,dV+\int_E y^2\,dV+\int_E yz\,dV=\frac{\pi}{16}+\frac{1}{15}+\frac{2}{15}+\frac{1}{15}=\frac{\pi}{16}+\frac{4}{15}$$

The moment $M_{xy}$ uses the factor $z$.

$$M_{xy}=\int_E z\,dV+\int_E xz\,dV+\int_E yz\,dV+\int_E z^2\,dV=\frac{\pi}{32}+\frac{1}{30}+\frac{1}{15}+\frac{2}{45}=\frac{\pi}{32}+\frac{13}{90}$$

Verification: `part3_verify.py` computes each moment twice, once as one product and once as the sum of its four monomial integrals, and it compares both values with a nested quadrature in two orders. The three sums agree with the three products to $10^{-15}$.

**Result:** $M_{yz}=\frac{7}{24}$, $M_{xz}=\frac{\pi}{16}+\frac{4}{15}$, and $M_{xy}=\frac{\pi}{32}+\frac{13}{90}$.
