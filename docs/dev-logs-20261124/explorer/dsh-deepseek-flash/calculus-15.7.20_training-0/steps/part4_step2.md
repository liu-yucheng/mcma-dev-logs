# Step 4.2 Check the volume with random points and with two bounds

## Reason

A random estimate gives an independent numerical value, and it gives its own error bar.
The error bar must contain the exact value; otherwise the estimate and the formula disagree.
Two simple solids also give bounds: one solid fits inside the given solid, and the second solid contains
the given solid. The exact value must lie between the two bounds.

## Computation

The box $\left[-2,2\right]\times\left[0,8\right]\times\left[-2,2\right]$ contains the solid and has the
volume $128$.
Draw $400000$ points at random in the box and count the points with

$$
x^{2}+z^{2}\le y\le 8-x^{2}-z^{2}.
$$

A fraction $p=0.393427$ of the points falls inside. The estimate is $128\cdot p=50.358720$.
The standard error of the estimate is

$$
128\sqrt{\frac{p\left(1-p\right)}{400000}}=0.098868 .
$$

The difference from $16\pi$ is $0.093238$, which is $0.94$ standard errors.

The inner solid is a double cone: two cones with base radius $2$ and height $4$. Its volume is

$$
2\cdot\frac{1}{3}\pi\cdot 2^{2}\cdot 4=\frac{32\pi}{3}\approx 33.51 .
$$

The outer solid is the cylinder of radius $2$ and height $8$. Its volume is $32\pi\approx 100.53$.
The cone fits inside the solid because $\sqrt{y}\ge y/2$ on $0\le y\le 4$, so the paraboloid is at least as
wide as the cone at every height.

## Result

Both checks agree with $V=16\pi$:
the random estimate is inside its own error bar, and $16\pi$ lies between $\frac{32\pi}{3}$ and $32\pi$.
The volume is exactly one half of the bounding cylinder, which is plausible because the two paraboloids are
mirror images about the plane $y=4$.

## Check

`code/part4_verify.py` uses the seed $20261122$ and prints
`random check: volume = 50.358720, expected = 50.265482, difference = 0.093238`,
`random check: standard error = 0.098868, allowed difference = 4.0 * standard error = 0.395470`.
The script asserts three conditions: the standard error is below $0.3$, the absolute difference is below
four standard errors, and the inside fraction stays between $0$ and $1$.
It also prints `volume of the inscribed double cone: computed = 33.510321638291`,
`volume of the bounding cylinder: computed = 100.530964914873`, and the bound check
`33.510322 < 50.265482 < 100.530965`.
