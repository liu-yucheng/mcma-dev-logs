# 3.2 Divide each moment by the mass

Each coordinate of the center of mass is one quotient. Reason: the quotient of a first moment by the mass gives the mean value of one coordinate over the solid, weighted by the density.

$$\bar{x}=\frac{M_{yz}}{m}, \qquad \bar{y}=\frac{M_{xz}}{m}, \qquad \bar{z}=\frac{M_{xy}}{m}$$

Each quotient has the mass $(44+9\pi)/96$ in its denominator, and the factor $96$ cancels part of the numerator.

$$\bar{x}=\frac{7/24}{(44+9\pi)/96}=\frac{28}{44+9\pi}\approx 0.387413$$

$$\bar{y}=\frac{\pi/16+4/15}{(44+9\pi)/96}=\frac{30\pi+128}{5(44+9\pi)}\approx 0.615012$$

$$\bar{z}=\frac{\pi/32+13/90}{(44+9\pi)/96}=\frac{45\pi+208}{15(44+9\pi)}\approx 0.322264$$

Two checks confirm the three values. The first check uses the difference of two coordinates, which must equal the quotient of the integral of $(y-z)\rho$ by the mass.

$$\bar{y}-\bar{z}=\frac{\frac{\pi}{16}+\frac{4}{15}-\frac{\pi}{32}-\frac{13}{90}}{m}\approx 0.292747$$

The second check tests the definition of $E$: the computed point lies inside the solid, so it satisfies all five inequalities of Step 1.1.

Verification: `part3_verify.py` compares each exact quotient with a quadrature ratio and with a Monte Carlo ratio, and it tests the point against the five inequalities. The Monte Carlo coordinates are $0.387350$, $0.615014$, and $0.322679$ with standard errors near $2\times 10^{-4}$.

**Result:** $(\bar{x},\bar{y},\bar{z})=\left(\frac{28}{44+9\pi},\ \frac{30\pi+128}{5(44+9\pi)},\ \frac{45\pi+208}{15(44+9\pi)}\right)\approx(0.387413,\ 0.615012,\ 0.322264)$.
