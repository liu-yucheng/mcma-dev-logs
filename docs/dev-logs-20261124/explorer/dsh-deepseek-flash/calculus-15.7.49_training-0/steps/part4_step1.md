# 4.1 The weight is the square of the distance to the $z$ axis

The moment of inertia about the $z$ axis weights each mass element by the square of its distance to that axis. Reason: the distance of the point $(x,y,z)$ to the $z$ axis is $\sqrt{x^2+y^2}$, and the axis does not move when $z$ changes.

$$I_z=\iiint_E \left(x^2+y^2\right)\rho\,dV$$

The product splits into eight monomials, and each one uses the rule of Step 3.1.

$$\left(x^2+y^2\right)(1+x+y+z)=x^2+y^2+x^3+xy^2+x^2y+y^3+x^2z+y^2z$$

The second moments group the eight monomial integrals by the coordinate that they weight. Reason: the two groups are the two terms of the weight.

$$\int_E x^2\rho\,dV=\frac{1}{15}+\frac{1}{24}+\frac{\pi}{96}+\frac{\pi}{192}=\frac{13}{120}+\frac{\pi}{64}\approx 0.157420$$

$$\int_E y^2\rho\,dV=\frac{2}{15}+\frac{1}{24}+\frac{\pi}{32}+\frac{\pi}{64}=\frac{7}{40}+\frac{3\pi}{64}\approx 0.322262$$

Each term in these two lines is one of the eight monomial integrals, and the four terms of each line come from the four terms of the density.

Figure 2 draws the eight monomial integrals as eight bars, and it labels each bar with the exact value of that same integral. The dashed line of Figure 2 marks the sum of the eight values.

Verification: `part4_verify.py` computes all eight monomial integrals with `sympy`, adds them, and compares the sum with the direct exact integral of $(x^2+y^2)\rho$. It also computes each second moment as a product and as the sum of its four terms.

**Result:** $\int_E x^2\rho\,dV=\frac{13}{120}+\frac{\pi}{64}$ and $\int_E y^2\rho\,dV=\frac{7}{40}+\frac{3\pi}{64}$, and Figure 2 shows the eight terms that give them.
