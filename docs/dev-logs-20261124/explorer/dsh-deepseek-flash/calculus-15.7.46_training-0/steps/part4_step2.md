# Part 4, Step 2: Stack the slices and compare with Part 3

## Reason

A slice of thickness $dz$ at height $z$ has mass $k$ multiplied by its area, and the area of the
disk of radius $z$ is $\pi z^{2}$. The definition of Part 1 puts the density $k$ outside the area
integral, so the slice contributes $k\,J(z)\,dz$, where $J(z)$ of Step 1 is the area integral of the
squared distance over that disk. The moment of the solid is the sum of the contributions of all
slices, which is an integral over $z$.

## Computation

$$I_{z} = \int_{0}^{h} k\,J(z)\,dz = k \int_{0}^{h} \frac{\pi z^{4}}{2}\,dz
= \frac{k\pi}{2} \cdot \frac{h^{5}}{5} = \frac{\pi k h^{5}}{10} .$$

The limits of this integral are $z = 0$ at the apex and $z = h$ at the base, and these limits come
from the same two inequalities that gave the limits of Part 2.

## Result

$$I_{z} = \frac{\pi k h^{5}}{10} .$$

This value is the value of Part 3, and the two routes use different limits: Part 3 integrates $z$
from $r$ to $h$ inside the body, and this step integrates $z$ from $0$ to $h$ over the whole height
with the radius $z$ inside the slice. The agreement supports both the limits of Part 2 and the
constant of Part 3.

Verification: `code/part4_verify.py` computes the same number by four methods. The symbolic triple
integral gives $\pi h^{5} k/10$. Triple adaptive quadrature gives 0.314159265359. The stack of the
slice moments gives 0.314159265359. Monte Carlo sampling of the definition of Part 1 gives
0.313724 plus or minus 0.000408, which is 1.067 standard errors from 0.314159. At $k = 1$ and
$h = 1$ the four methods agree.

> **Part 4 answer.** $I_{z} = \displaystyle\int_{0}^{h} k\,\frac{\pi z^{4}}{2}\,dz
> = \dfrac{\pi k h^{5}}{10}$, the same value that Part 3 gives.
