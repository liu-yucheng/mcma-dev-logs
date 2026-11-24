# Step 11 — Check the volume and the mean value

## Reason

Two numbers must agree with the value of the integral: the volume of $E$ and the mean value of $x$ over $E$. Both have independent formulas, so a disagreement shows an arithmetic fault or a limit fault.

The mean value of $x$ also gives a physical check. The region lies between $x = 0$ and $x = 4$, so the mean value must lie in that interval. The paraboloid is thin near $x = 0$ and wide near $x = 4$, so the mean value must be above the midpoint $2$.

## Computation

The volume follows from the disk slices of Step 10:

$$
V = \int_{0}^{4} \frac{\pi x}{4} \, dx = \frac{\pi}{4} \cdot 8 = 2\pi .
$$

The mean value of $x$ over $E$ is the integral divided by the volume:

$$
\bar{x} = \frac{1}{V}\iiint_{E} x \, dV = \frac{16\pi/3}{2\pi} = \frac{8}{3}.
$$

The shell form gives a third route. At radius $r$ the shell has circumference $2\pi r$, length $4 - 4r^{2}$, and mean $x$ equal to $\left(4 + 4r^{2}\right)/2$:

$$
\iiint_{E} x \, dV = \int_{0}^{1} 2\pi r \left(4 - 4r^{2}\right) \frac{4 + 4r^{2}}{2} \, dr
= 16\pi \int_{0}^{1} r\left(1 - r^{4}\right) dr
= 16\pi \left(\frac{1}{2} - \frac{1}{6}\right) = \frac{16\pi}{3}.
$$

## Result

$$
V = 2\pi \approx 6.283185307180, \qquad \bar{x} = \frac{8}{3} \approx 2.666666666667, \qquad
\iiint_{E} x \, dV = V\bar{x} = \frac{16\pi}{3}.
$$

The mean value $2.667$ lies in $(0, 4)$ and above the midpoint $2$. Both facts fit the shape of $E$.

## Verification

`code/part4_verify.py` reports the volume $6.283185307180$ from the disk slices, the mean value $2.666666666667$, and the shell integral $16.755160819146$. `code/part1_verify.py` counts the volume by a Monte Carlo test and reports $6.2755$ against $6.2832$, within four standard errors.
