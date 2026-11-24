# 1.2 A section turns a triple integral into one integral

A section of $E$ at a fixed $x$ is the set of the pairs $(y,z)$ with $0 \le z \le y \le Y$, where $Y=\sqrt{1-x^2}$. Reason: the inequalities of Step 1.1 keep $x$ fixed and leave the two other inequalities unchanged, so the section is a triangle in the plane of that fixed $x$.

The triangle has the vertices $(0,0)$, $(Y,0)$, and $(Y,Y)$ in the $(y,z)$ plane, so its area is $Y^2/2$. Reason: the legs of the right triangle along the two axes have the lengths $Y$ and $Y$.

The volume is the integral of the section area. Reason: the section area is the area element of the order $dx$ last.

$$V=\int_0^1 \frac{Y^2}{2}\,dx=\frac{1}{2}\int_0^1 (1-x^2)\,dx=\frac{1}{2}\left(1-\frac{1}{3}\right)=\frac{1}{3}$$

A section at a fixed $z$ gives the same volume by a different route. The section is the set of the pairs $(x,y)$ with $z \le y \le 1$ and $0 \le x \le \sqrt{1-y^2}$, so its area is $\pi/4 - \left(z\sqrt{1-z^2}+\arcsin z\right)/2$. At $z=0$ this area is $\pi/4$, and the integral of the area over $0 \le z \le 1$ is again $1/3$.

The section at $x=1$ collapses to the single point $(0,0)$ in the $(y,z)$ plane, because $Y=0$ at $x=1$. The right panel of Figure 1 shows one section that does not collapse.

Verification: `part1_verify.py` computes the section area at a fixed $x$ in two ways, with the shoelace formula on the printed vertices and with a midpoint grid, and it computes the section area at four values of $z$ with a quadrature and with a grid. It then integrates both families of section areas and compares each volume with $1/3$.

**Result:** $V=\int_0^1 Y^2/2\,dx=1/3$, and the two families of sections agree.
