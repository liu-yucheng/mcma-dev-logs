# Part 4, Step 1: Compute the moment of one horizontal slice

## Reason

The result of Part 3 needs a second route, because one route cannot expose a wrong pair of limits.
Cut the solid into thin horizontal slices. Each slice is a disk that lies in a plane perpendicular
to the $z$-axis, and the $z$-axis passes through the centre of that disk. The moment of the slice
about the $z$-axis is therefore its polar second moment, an area integral over the disk.

## Computation

Part 1 gives the slice at height $z$: it is the disk of radius $z$. In polar coordinates inside that
disk the distance to the axis is $\rho$ and the area element is $\rho\,d\rho\,d\phi$, so the polar
second moment of the slice is

$$J(z) = \int_{\phi = 0}^{2\pi} \int_{\rho = 0}^{z} \rho^{2} \cdot \rho\,d\rho\,d\phi
= 2\pi \int_{0}^{z} \rho^{3}\,d\rho = 2\pi \cdot \frac{z^{4}}{4} = \frac{\pi z^{4}}{2} .$$

The symbol $z$ is fixed during this computation. It enters only as the radius of the disk.

## Result

$$J(z) = \frac{\pi z^{4}}{2} .$$

The second moment of the slice grows as the fourth power of the height, because both the radius and
the distance of the area from the axis grow with the height. Figure 3 shows the slice cut into rings
and the curve $J(z)$ whose area under it is the moment of the whole cone.

![Figure 3: Left, the slice at $z = z_{0}$ cut into rings; the marked ring has radius $r$ and width $dr$, and its area is about $2\pi r\,dr$. Right, the second moment $J(z) = \pi z^{4}/2$ of the slice at height $z$; the shaded area under the curve is the integral $I_{z} = \int_{0}^{h} k\,J(z)\,dz$.](figures/part4_figure1.png)

Verification: `code/part4_verify.py` computes the polar second moment of the slice at the heights
$z = 0.25$, $z = 0.50$, and $z = 0.75$ by two methods. The polar integral gives 0.006135923,
0.098174770, and 0.497009775, and a Cartesian area integral over the same disk gives the same three
values, and the formula $\pi z^{4}/2$ gives the same three values. The largest gap between the polar
value and the formula is 0.000e+00. `code/part4_figure1.py` draws Figure 3 and prints the value
0.232106 for $J$ at $z = 0.6200$ and 1.570796 for $J$ at $z = 1.0000$.
