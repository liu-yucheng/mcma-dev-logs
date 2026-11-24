# Part 3, Step 2: Integrate in r and read the answer

## Reason

The remaining integral is a polynomial in $r$. The power rule gives the antiderivative of each term,
and the limits $0$ and $h$ turn the antiderivative into a single power of $h$.

## Computation

Split the integral into two terms and apply the power rule:

$$\int_{0}^{h} h\,r^{3}\,dr = h \cdot \frac{h^{4}}{4} = \frac{h^{5}}{4}, \qquad
\int_{0}^{h} r^{4}\,dr = \frac{h^{5}}{5} .$$

Subtract the second value from the first value:

$$\int_{0}^{h} \left(h\,r^{3} - r^{4}\right) dr = \frac{h^{5}}{4} - \frac{h^{5}}{5}
= h^{5}\left(\frac{1}{4} - \frac{1}{5}\right) = \frac{h^{5}}{20} .$$

Now multiply by the constant $2\pi k$ of the previous step:

$$I_{z} = 2\pi k \cdot \frac{h^{5}}{20} = \frac{\pi k h^{5}}{10} .$$

## Result

$$I_{z} = \frac{\pi k h^{5}}{10} .$$

The result is an expression in $k$ and $h$, as the statement requires, because the statement prints
no numerical value for either symbol.

Verification: `code/part3_verify.py` evaluates $\int_{0}^{h}(h r^{3} - r^{4})\,dr$ at $h = 1$ by the
symbolic computation, by exact arithmetic on fractions, by adaptive quadrature, and by the composite
Simpson rule. The four values are $1/20$, $1/20$ = 0.05000000, 0.05000000, and 0.05000000. At
$h = 1.7$ the formula $h^{5}/20$ gives 0.7099285000, and quadrature and the Simpson rule give
0.7099285000. The script also multiplies the exact value $1/20$ by $2\pi$ and compares the product
with $\pi/10$: the two values are 0.3141592654 and 0.3141592654, so the constant $2\pi$ of the
previous step is carried correctly.

> **Part 3 answer.** $I_{z} = \dfrac{\pi k h^{5}}{10}$.
