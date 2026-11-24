# Step 3.2 Integrate over the angle and state the volume

## Reason

The angle integral has the constant integrand $1$, and its limits are $0$ and $2\pi$.
The two outer integrals multiply, because the radius integral does not depend on the angle.
The product gives the exact volume.

## Computation

The angle integral is

$$
I_\theta=\int_{0}^{2\pi} d\theta=2\pi .
$$

Multiply the two outer integrals.

$$
V=I_\theta \cdot I_r = 2\pi\cdot 8 = 16\pi .
$$

The numerical value is

$$
V=16\pi \approx 50.2654824574 .
$$

## Result

The volume of the solid is

$$
\boxed{V=16\pi \approx 50.27}
$$

cubic units. The statement gives no unit of length, so the statement of the answer uses cubic units of the
given coordinates.

## Check

`code/part3_verify.py` evaluates the same triple integral with `scipy.integrate.tplquad` in cylindrical
coordinates and prints `volume from the cylindrical triple integral: computed = 50.265482457437,
expected = 50.265482457437`. It also prints `volume from the product of the outer integrals:
computed = 50.265482457437`.
The script asserts an absolute difference below $10^{-9}$ between that product and $16\pi$.
The numerical triple integral has the looser bound $10^{-8}$, because a quadrature routine adds its own
rounding error.
