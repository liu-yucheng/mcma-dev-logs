## Step 3.1: The radial integral gives $\frac{2}{3}a^{3}\left(1 - |\sin\theta|^{3}\right)$

**Reason.** Put $u = a^{2} - r^{2}$, so that $du = -2r\,dr$. The integrand becomes $\sqrt{u}$, and
the antiderivative is $-\frac{2}{3}u^{3/2}$. At the upper limit $r = a\cos\theta$ the term
$a^{2} - r^{2}$ equals $a^{2}\sin^{2}\theta$, so its three halves power is $a^{3}|\sin\theta|^{3}$.
The absolute value is necessary, because a power of an even exponent loses the sign of $\sin\theta$.

**Computation.** Take $a = 1$. At $\theta = 0$ the radial integral is $0.666666666667$. At
$\theta = -\pi/4$ it is $0.430964406271$, which is $\frac{2}{3}\left(1 - 0.353553\right)$ because
$|\sin(-\pi/4)|^{3} = 0.353553$. The substitution $u = r^{2}$ gives the same value
$0.43096440627115096$ as the direct quadrature $0.4309644062711509$.

**Common mistake.** A reader may keep the sign of $\sin\theta$ and write
$\frac{2}{3}a^{3}\left(1 - \sin^{3}\theta\right)$, but the limits give
$\frac{2}{3}a^{3}\left(1 - |\sin\theta|^{3}\right)$: `code/part3_verify.py` prints $0.902368927062$
for the signed form at $\theta = -\pi/4$ against $0.430964406271$ for the correct form.

**Result.** After the radial integration,
$$V = \frac{2}{3}a^{3}\int_{-\pi/2}^{\pi/2}\left(1 - |\sin\theta|^{3}\right)d\theta.$$

**Verification.** `code/part3_verify.py` prints `substituted_radial_integral` as $0.43096440627115096$
against $0.4309644062711509$, the slope checks `antiderivative_slope_at_r_0` at three radii with a
tolerance of $1.0\times10^{-7}$, and `upper_bound_maximum` as $1.0$ against $a$.
