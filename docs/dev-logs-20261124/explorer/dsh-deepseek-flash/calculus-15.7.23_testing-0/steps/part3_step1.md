# Part 3. The exact value of the integral

## Reason

The integral of Part 2 has three nested integrals, and each one is a polynomial in its variable
once the inner limit is in place. Evaluate from the inner integral to the outer integral, and
check each antiderivative by a derivative.

## Computation

The inner integral is

$$\int_{0}^{y}1\,dx=y .$$

The middle integral is

$$\int_{0}^{\sqrt{1-z^{2}}}y\,dy=\frac{1-z^{2}}{2}.$$

The outer integral is

$$V=\int_{0}^{1}\frac{1-z^{2}}{2}\,dz=\left[\frac{z}{2}-\frac{z^{3}}{6}\right]_{0}^{1}=\frac{1}{2}-\frac{1}{6}=\frac{1}{3}.$$

## Common mistake

A reader may keep the factor $1/2$ from the inner integral and also divide the outer result by
$2$, but the antiderivative $z/2-z^{3}/6$ already holds the factor, so the value is $1/3$ and not
$1/6$.

## Result

The exact volume is $1/3$, that is {{p3_exact_decimal}}. The check of
`code/part3_verify.py` compares the fraction $1/3$ with adaptive quadrature, which gives
{{p3_quadrature}}, and with the substitution $z=\sin t$, which gives {{p3_substituted}}. The
script also compares the derivative of $z/2-z^{3}/6$ with the slice area at {{p3_point_count}}
points. This is the answer to part (b).

Verification: `code/part3_verify.py`.
