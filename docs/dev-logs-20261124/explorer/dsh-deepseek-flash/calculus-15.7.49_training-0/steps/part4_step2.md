# 4.2 Add the two second moments

The moment of inertia is the sum of the two second moments, because the weight is the sum of the two squares.

$$I_z=\frac{13}{120}+\frac{7}{40}+\frac{\pi}{64}+\frac{3\pi}{64}=\frac{34}{120}+\frac{\pi}{16}=\frac{17}{60}+\frac{\pi}{16}\approx 0.479683$$

A second coordinate system confirms the value. In polar coordinates $x=r\cos\theta$ and $y=r\sin\theta$, the disk becomes $0 \le r \le 1$ with $0 \le \theta \le \pi/2$, the plane $z=y$ becomes $z=r\sin\theta$, and the volume element becomes $r\,dz\,dr\,d\theta$.

$$I_z=\int_0^{\pi/2}\int_0^1\int_0^{r\sin\theta} r^3\left(1+r\cos\theta+r\sin\theta+z\right)dz\,dr\,d\theta=\frac{1}{5}+\frac{1}{12}+\frac{\pi}{16}$$

Two bounds test the size of the answer. The density lies between $1$ and $1+\sqrt{5}$ on $E$, and the plain integral of $x^2+y^2$ is $1/5$, so the moment of inertia lies between $0.200000$ and $0.647214$. It is also smaller than the mass, because $x^2+y^2 \le 1$ on $E$.

Verification: `part4_verify.py` computes $I_z$ in seven independent ways: four exact forms, which are the direct integral, the sum of the two second moments, the sum of the eight monomial integrals, and the polar integral, and three numerical routes, which are two Cartesian orders, one polar quadrature, and one Monte Carlo sample. The Monte Carlo estimate is $0.479796$ with a standard error of $0.000404$. The script also checks the two bounds and the largest density that a sample of $E$ reaches.

**Result:** $I_z=\frac{17}{60}+\frac{\pi}{16}\approx 0.479683$.
