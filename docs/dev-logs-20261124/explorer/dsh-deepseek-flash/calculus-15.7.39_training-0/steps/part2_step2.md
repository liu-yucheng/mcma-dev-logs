# Step 2.2: Integrate the slice area to get the volume

## Reason

The solid is a stack of the slices of Step 2.1. Cavalieri's principle: the volume is the integral of the slice area over $x$. Each slice is perpendicular to the $x$-axis, so the integral runs over $x$.

## Work

$$V = \int_{0}^{1} s(x)\, dx = \int_{0}^{1}\left(\sqrt{x} + x^{3/2} + \frac{x}{2}\right) dx .$$

Integrate term by term:

$$\int_{0}^{1} x^{1/2} dx = \frac{2}{3}, \qquad \int_{0}^{1} x^{3/2} dx = \frac{2}{5}, \qquad \int_{0}^{1} \frac{x}{2} dx = \frac{1}{4}.$$

Add the three exact terms:

$$V = \frac{2}{3} + \frac{2}{5} + \frac{1}{4} = \frac{40}{60} + \frac{24}{60} + \frac{15}{60} = \frac{79}{60}.$$

## Result

$V = \frac{79}{60} \approx 1.316667$.

Verification: `part2_verify.py` prints the volume from exact fractions, from a symbolic double integral, from a numerical double quadrature, and from a Monte Carlo sample. All four values agree.
