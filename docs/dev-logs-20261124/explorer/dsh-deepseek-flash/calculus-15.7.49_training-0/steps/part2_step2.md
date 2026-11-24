# 2.2 The integrals in $y$ and in $x$

Integrate the inner integral over $0 \le y \le Y$. Reason: the limits of $y$ come from the cylinder, and the variable $x$ stays constant.

$$\int_0^{Y}\left((1+x)y+\frac{3}{2}y^2\right)dy=(1+x)\frac{Y^2}{2}+\frac{Y^3}{2}$$

The mass is the integral of this expression over $0 \le x \le 1$. Reason: the last inequality of Step 1.1 puts $x$ between $0$ and $1$.

$$m=\frac{1}{2}\int_0^1 (1+x)(1-x^2)\,dx+\frac{1}{2}\int_0^1 (1-x^2)^{3/2}\,dx$$

Three standard integrals finish the work. Reason: the first two are integrals of polynomials, and the third becomes an integral of a power of a cosine after the substitution $x=\sin\theta$.

$$\int_0^1 (1-x^2)\,dx=\frac{2}{3}, \qquad \int_0^1 x(1-x^2)\,dx=\frac{1}{4}, \qquad \int_0^1 (1-x^2)^{3/2}\,dx=\frac{3\pi}{16}$$

The last value follows from $x=\sin\theta$ and $\int_0^{\pi/2}\cos^4\theta\,d\theta=\frac{3\pi}{16}$.

So the mass is one rational number plus one multiple of $\pi$.

$$m=\frac{1}{2}\left(\frac{2}{3}+\frac{1}{4}\right)+\frac{1}{2}\cdot\frac{3\pi}{16}=\frac{11}{24}+\frac{3\pi}{32}=\frac{44+9\pi}{96}\approx 0.752858$$

Verification: `part2_verify.py` computes the mass by four independent methods: the exact integral above, the sum of the four integrals of $1$, $x$, $y$, and $z$, a nested quadrature in three integration orders, and a Monte Carlo sample of four million points. The Monte Carlo estimate is $0.753228$ with a standard error of $0.000544$.

**Result:** $m=\frac{11}{24}+\frac{3\pi}{32}=\frac{44+9\pi}{96}\approx 0.752858$.
