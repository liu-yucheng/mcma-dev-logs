# Step 1.2: Compute the area of $D$

## Reason

The area of $D$ is the first integral of the problem. The volume and the moments all use this region. A wrong area gives a wrong mass.

## Work

The area is the integral of the height of the region over the interval of $x$:

$$A(D) = \int_{0}^{1} \sqrt{x}\, dx .$$

The power rule gives $\int x^{1/2} dx = \frac{2}{3} x^{3/2}$. Evaluate the antiderivative at the two limits:

$$A(D) = \frac{2}{3}\cdot 1^{3/2} - \frac{2}{3}\cdot 0^{3/2} = \frac{2}{3}.$$

A second method uses horizontal slices. At height $y$, the slice runs from $x = y^{2}$ to $x = 1$. Its length is $1 - y^{2}$. So

$$\int_{0}^{1}\left(1 - y^{2}\right) dy = 1 - \frac{1}{3} = \frac{2}{3}.$$

Both methods give $\frac{2}{3}$. Figure 1 shows the region and the curve that bounds it.

## Result

$A(D) = \frac{2}{3} \approx 0.666667$.

Verification: `part1_verify.py` prints the area from the power rule, from quadrature, from horizontal slices, and from a Monte Carlo sample of four million points. All four values agree within their stated tolerance.
