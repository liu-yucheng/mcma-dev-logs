# Step 3.1 Integrate over the radius

## Reason

The radius integral has a polynomial integrand, so one antiderivative gives its exact value.
Use the power rule on each term separately.
The result is the volume of one thin wedge of angle $1$ radian, so it must be smaller than the volume
of the whole solid.

## Computation

The radius integral is

$$
I_r=\int_{0}^{2}\left(8r-2r^{3}\right) dr .
$$

An antiderivative of $8r$ is $4r^{2}$, and an antiderivative of $-2r^{3}$ is $-\tfrac{1}{2}r^{4}$.
So

$$
I_r=\left[4r^{2}-\frac{r^{4}}{2}\right]_{0}^{2}
=\left(4\cdot 4-\frac{16}{2}\right)-0
=16-8=8 .
$$

## Result

The radius integral has the value $8$.
This value is the area under the curve $r\left(8-2r^{2}\right)$ on the interval $0\le r\le 2$,
and it is the volume of the part of the solid between the angles $0$ and $1$ radian.

## Check

`code/part3_verify.py` computes the antiderivative at both limits and prints
`antiderivative at radius 2: computed = 8.000000000000, expected = 8.000000000000` and
`antiderivative at radius 0: computed = 0.000000000000, expected = 0.000000000000`.
It also integrates the integrand numerically with `scipy.integrate.quad` and prints
`radius integral over 0 to 2: computed = 8.000000000000, expected = 8.000000000000`.
The script checks that the antiderivative increases by the integrand on a small interval at four radii;
the largest gap of that check is $6.4\times10^{-16}$.
