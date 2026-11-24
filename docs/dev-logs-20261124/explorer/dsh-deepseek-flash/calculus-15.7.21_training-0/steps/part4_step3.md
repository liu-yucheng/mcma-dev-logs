# Step 4.3 - Check the volume against the geometry, and state the answer

Part 4: the volume and its checks.

## Reason

A number from a formula needs a check that does not use the formula. Two geometric bounds do that work: the volume is larger than an easy inner box, and it is smaller than the shadow area times the tallest column. A result outside those bounds would be wrong even if every integral looked right.

## Computation

Lower bound. Take the box

$$-0.5 \leq x \leq 0.5, \qquad 0.25 \leq y \leq 0.5, \qquad 0 \leq z \leq 0.5.$$

Every point of this box is in the solid: $y \geq 0.25 \geq x^{2}$ holds on the $x$ range, and $y + z \leq 0.5 + 0.5 = 1$ holds on the other two ranges. The volume of the box is $1 \cdot 0.25 \cdot 0.5 = 0.125$, so $V > 0.125$.

Upper bound. The column height is at most 1 on the shadow, so $V$ is at most the shadow area, which is $4 / 3$. The shadow lies in the box of Step 1.2, whose volume is 2, so $V < 4 / 3 < 2$.

The computed value satisfies both bounds:

$$0.125 < 0.533333\ldots < 1.333333\ldots < 2.$$

## Result

$$\boxed{V = \frac{8}{15} \approx 0.5333 \text{ cubic units}}$$

## Check

`code/part4_verify.py` prints the lower bound check with margin `0.408`, the shadow area `1.33333333333333` against `4 / 3`, and the upper bound check with margin `0.8`. It also prints the volume from a trapezoid rule on 1600000 intervals as `0.533333333333333`, and the volume of a rejection sample of the bounding box as `0.5334815` with a standard error of `4.422e-04`. Five independent methods agree on $8 / 15$.
