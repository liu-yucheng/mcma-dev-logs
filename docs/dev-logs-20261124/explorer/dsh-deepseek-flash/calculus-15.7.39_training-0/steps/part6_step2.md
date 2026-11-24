# Step 6.2: Divide the moment by the mass to get $\bar{z}$ and state the answer

## Reason

The last coordinate uses the same rule as Steps 4.2 and 5.2. After that division, the three coordinates and the mass answer the question.

## Work

$$\bar{z} = \frac{M_{xy}}{m} = \frac{571/210}{79/30} = \frac{571}{210}\cdot\frac{30}{79} = \frac{571}{7 \cdot 79} = \frac{571}{553}.$$

A numerical check: $571 \div 553 = 1.032550$.

The value is consistent with the geometry. The ceiling above $(\bar{x}, \bar{y})$ is $1 + 0.647378 + 0.417722 = 2.065099$, so $\bar{z} = 1.032550$ lies below the ceiling and above the floor.

Collect the three coordinates and the mass:

- $\bar{x} = \frac{358}{553} \approx 0.647378$
- $\bar{y} = \frac{33}{79} \approx 0.417722$
- $\bar{z} = \frac{571}{553} \approx 1.032550$
- $m = \frac{79}{30} \approx 2.633333$

Figure 2 shows the solid $E$, the ceiling $z = 1 + x + y$, the two vertical walls, the floor $z = 0$, the center of mass, and its projection on the floor.

## Result

The mass is $\frac{79}{30} \approx 2.633333$. The center of mass is

$$\left(\frac{358}{553},\ \frac{33}{79},\ \frac{571}{553}\right) \approx (0.647378,\ 0.417722,\ 1.032550).$$

Verification: `part6_verify.py` prints $\bar{z}$ from the fraction division, from a symbolic moment over the exact mass, and from the quadrature moment over the quadrature mass. It also compares all three coordinates with one Monte Carlo average of six million points.
