# Step 3.2: Record the mass in both exact and decimal form

## Reason

The later steps divide the moments by the mass. The exact fraction $\frac{79}{30}$ keeps the division exact. The decimal form lets the reader compare the answer with a plot.

## Work

Divide the numerator by the denominator: $79 \div 30 = 2.6333\ldots$. So the mass is $2.633333$ to six decimal places.

The mass has no units in this problem, because the statement gives the coordinates and the density as plain numbers.

One consistency check: the mass must be smaller than the density times the volume of the bounding box. The box of $E$ is $0 \leq x \leq 1$, $0 \leq y \leq 1$, $0 \leq z \leq 3$, so its volume is $3$. The value $2 \cdot 3 = 6$ is larger than $\frac{79}{30} \approx 2.63$, as expected.

## Result

$m = \frac{79}{30} \approx 2.633333$.

The mass is smaller than the mass of the bounding box at the same density.

Verification: `part3_verify.py` prints both forms and the bounding-box comparison.
