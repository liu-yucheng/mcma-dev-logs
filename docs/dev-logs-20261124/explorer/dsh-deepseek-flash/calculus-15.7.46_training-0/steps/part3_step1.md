# Part 3, Step 1: Integrate in z first

## Reason

The integrand $k r^{3}$ of Part 2 holds no $z$. The inner integral of a constant over an interval
is the constant multiplied by the length of the interval, so the first integration needs no
antiderivative.

## Computation

The inner limits are $z = r$ and $z = h$ at fixed $r$. Their difference is the length $h - r$ of the
vertical chord, so

$$\int_{z=r}^{h} k\,r^{3}\,dz = k\,r^{3}\,(h - r) .$$

Insert this value into the two outer integrals. The integrand no longer holds $z$, so the two
remaining integrals are

$$I_{z} = \int_{0}^{2\pi} \int_{0}^{h} k\,r^{3}\,(h - r)\,dr\,d\theta .$$

The factor $k\,r^{3}\,(h - r)$ holds no $\theta$, and the limits of $\theta$ are $0$ and $2\pi$, so
the outer integral multiplies the result by $2\pi$:

$$I_{z} = 2\pi k \int_{0}^{h} \left(h\,r^{3} - r^{4}\right) dr .$$

## Result

One integration remains, over the single variable $r$:

$$I_{z} = 2\pi k \int_{0}^{h} \left(h\,r^{3} - r^{4}\right) dr .$$

Verification: `code/part3_verify.py` evaluates the inner integral $\int_{r}^{h} k\,r^{3}\,dz$ at
$r = 0.3$, $h = 1$, and $k = 1$ by three methods. The symbolic computation gives $189/10000$, the
exact arithmetic on fractions gives $189/10000$, and adaptive quadrature gives 0.01890000. The
three values agree, and $k\,r^{3}(h - r) = 0.3^{3} \cdot 0.7 = 0.0189$ by hand.
