# Part 3, Step 2: Evaluate the polar integral

## Reason

The polar integral carries the Jacobian factor $\sin\varphi$, and that extra factor is what makes the integral elementary. The substitution $u = \cos\varphi$ turns $\sin\varphi\,d\varphi$ into $-du$, so the integral becomes a polynomial in $u$ over the interval $-1 \le u \le 1$. The result is a rational number that is slightly larger than one, and the excess over one is the exact excess of the body over the unit ball in the polar direction.

## Computation

Set $u = \cos\varphi$, so that $du = -\sin\varphi\,d\varphi$ and $\varphi$ from $0$ to $\pi$ means $u$ from $1$ to $-1$. Then

$$
B = \int_{0}^{\pi}\sin^{2}5\varphi\,\sin\varphi\,d\varphi
= \int_{-1}^{1}\sin^{2}(5\arccos u)\,du .
$$

Expand the square with $\sin^{2}v = \frac{1 - \cos 2v}{2}$ and use $2\arccos u$ as one angle:

$$
B = \frac{1}{2}\int_{-1}^{1}du - \frac{1}{2}\int_{-1}^{1}\cos(10\arccos u)\,du .
$$

The first integral is $1$. The second follows from the product-to-sum identity $\cos 10\varphi\,\sin\varphi = \frac{1}{2}\bigl(\sin 11\varphi - \sin 9\varphi\bigr)$, so

$$
\int_{0}^{\pi}\cos 10\varphi\,\sin\varphi\,d\varphi
= \frac{1}{2}\left(\frac{2}{11} - \frac{2}{9}\right) = -\frac{2}{99},
$$

This value follows because $\int_{0}^{\pi}\sin 11\varphi\,d\varphi = \frac{2}{11}$ and $\int_{0}^{\pi}\sin 9\varphi\,d\varphi = \frac{2}{9}$. The minus sign in front of the cosine term then gives

$$
B = 1 + \frac{1}{99} = \frac{100}{99}.
$$

The same calculation for the harmonic $n$ gives

$$
B_{n} = 1 + \frac{1}{4n^{2} - 1}.
$$

## Result

The polar integral is $B = \frac{100}{99} = 1.0101010101$. The identity returns $\frac{36}{35}$ at $n = 3$, $\frac{100}{99}$ at $n = 5$, and $\frac{196}{195}$ at $n = 7$. The value is larger than one, so the polar direction adds a small amount of volume, and that amount is $\frac{1}{99}$ of the volume of the unit ball.

## Common mistake

A reader may integrate $\sin^{2}5\varphi$ without the factor $\sin\varphi$ and obtain $\pi$, but the Jacobian factor belongs to the integrand and its presence is what reduces the integral to a rational number. A reader may also expect the polar integral to be one, because the average of a sine squared is one half, but the weight $\sin\varphi$ favours the equator, where $\sin^{2}5\varphi$ is large on most of the equator band, and the weighted average is slightly above one half of the maximum.

## Verification

The script `code/part3_verify.py` evaluates $B$ in two ways. The exact route builds the trigonometric polynomial of $\sin^{2}5\varphi\,\sin\varphi$ and integrates each term, and the reference route uses an adaptive quadrature of the same integrand. The row `polar integral: exact polynomial against quadrature` of `code/outputs/part3_summary.md` reports $1.0101010101$ against $1.0101010101$ with a difference of $2.220 \times 10^{-16}$, the row `polar integral: polynomial against the product-to-sum identity` reports $\frac{100}{99}$ against $\frac{100}{99}$, and the three rows at harmonics $3$, $5$, and $7$ report $\frac{36}{35}$, $\frac{100}{99}$, and $\frac{196}{195}$ against the same values with a difference of $0$.
