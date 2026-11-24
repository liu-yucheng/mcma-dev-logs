# Part 3. The mass

## Step 3.1. Put the density into the integral

### Reason
The mass is the integral of the density over the solid, so the integrand is the density itself and the limits are the limits of Part 1. A reader may read the radical as covering only $x^{2}$, but the bar covers both terms, so the density is $\sqrt{x^{2} + y^{2}}$ and it vanishes only at the point $(0, 0, 1)$.

### Computation
$$m = \int_{-1}^{1} \int_{x^{2}}^{1} \int_{0}^{1 - y} \sqrt{x^{2} + y^{2}}\,dz\,dy\,dx.$$
The inner integral gives $(1 - y)\sqrt{x^{2} + y^{2}}$. The middle integral has an elementary antiderivative in $y$ at a fixed $x$, and the outer integral is one-dimensional.

### Result
The mass integral uses the order $dz\,dy\,dx$, and the inner integration is exact, so the value does not depend on a numerical grid.
`code/part3_verify.py` compares the mass of the cut at three heights with a two-dimensional quadrature over the same cut.
