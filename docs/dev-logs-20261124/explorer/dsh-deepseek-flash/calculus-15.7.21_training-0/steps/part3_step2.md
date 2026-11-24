# Step 3.2 - Compute the area of the slice

Part 3: the slice at a fixed $x$.

## Reason

The slice is a polygon with straight sides, so its area has a closed form. The area of a triangle is one half of the base times the height, and we can read the base and the height from the three lines. Both legs of this triangle happen to be horizontal and vertical, so the arithmetic is short.

## Computation

The triangle of Step 3.1 has the three vertices

$$\left(a^{2}, 0\right), \qquad \left(1, 0\right), \qquad \left(a^{2}, 1 - a^{2}\right).$$

The horizontal leg runs from $\left(a^{2}, 0\right)$ to $\left(1, 0\right)$, so its length is $1 - a^{2}$. The vertical leg runs from $\left(a^{2}, 0\right)$ to $\left(a^{2}, 1 - a^{2}\right)$, so its length is also $1 - a^{2}$. Both legs meet at the right angle $\left(a^{2}, 0\right)$, so the triangle is a right isosceles triangle and

$$A\left(a\right) = \frac{1}{2} \cdot \left(1 - a^{2}\right) \cdot \left(1 - a^{2}\right) = \frac{\left(1 - a^{2}\right)^{2}}{2}.$$

The same area also follows from an iterated integral, which is the form that the volume uses later:

$$A\left(a\right) = \int_{a^{2}}^{1} \int_{0}^{1 - y} dz\, dy = \int_{a^{2}}^{1} \left(1 - y\right) dy.$$

## Result

At $a = 0$ the area is $1 / 2 = 0.5$. At $a = 0.5$ the area is $0.75^{2} / 2 = 0.28125$. At $a = 0.9$ the area is $0.19^{2} / 2 = 0.01805$.

## Check

`code/part3_verify.py` measures each area in three independent ways: a rejection sample, a quadrature of the inner integral, and the surveyor formula for a polygon. It prints `0.4999255`, `0.28100222`, and `0.018048917` from the sample, against expected values `0.5`, `0.28125`, and `0.01805`. The sample errors are below one standard error in the first case and below four standard errors in the other two cases. The quadrature and the surveyor values agree with the formula to $10^{-12}$. The script also counts the corners of the sampled region and prints `3` at each abscissa, so the region is a triangle and not a ring.
