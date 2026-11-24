# Step 1.2 Find the region that the solid covers in the horizontal plane

## Reason

A triple integral needs the region of the two horizontal variables.
Look straight down the vertical axis. The solid covers a point $(x,z)$ only when the upper surface is
above the lower surface at that point.
The difference of the two heights is the vertical thickness. A positive thickness means that the solid
covers the point.

## Computation

The vertical thickness at the squared radius $s=x^{2}+z^{2}$ is

$$
T(s)=\left(8-s\right)-s=8-2s .
$$

The thickness is positive when

$$
8-2s>0 \quad\Longleftrightarrow\quad s<4 .
$$

The thickness is zero on the circle $s=4$ and negative outside that circle.
So the solid covers exactly the disk

$$
D=\left\{(x,z)\;:\;x^{2}+z^{2}\le 4\right\}
$$

of radius $2$. The area of $D$ is $\pi\cdot 2^{2}=4\pi$.
The largest thickness is $T(0)=8$ at the center, and the smallest thickness is $T(4)=0$ at the rim.

## Result

The projection of the solid on the plane $y=0$ is the closed disk of radius $2$.
Every vertical line through the inside of the disk cuts the solid in one segment.
Every vertical line through the outside of the disk misses the solid.

## Check

`code/part1_verify.py` samples the thickness on $0\le r\le 1.999$ and on $2.001\le r\le 3$.
It prints `smallest thickness on 0 <= radius <= 1.999: computed = 0.007998` and
`largest thickness on 2.001 <= radius <= 3: computed = -0.008002`.
The first value is positive and the second value is negative, so the projection is the disk and nothing more.
The same script prints `area of the projection disk: computed = 12.566370614359172, expected = 12.566370614359172`
for $4\pi$.
