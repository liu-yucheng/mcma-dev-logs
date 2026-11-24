# Part 3. The two orders with $x$ outermost

An order names its differentials from the inside to the outside. In the order $dz\,dy\,dx$ the inner
integral is in $z$, the middle integral is in $y$, and the outer integral is in $x$. The outer variable
chooses the section, and the two inner variables run over that section.

## Step 3.1. Write the order $dz\,dy\,dx$

**Why.** The outer variable is $x$, so the section is the one at a fixed $x$. Step 2.1 gives its shape.
The inner integral is in $z$, so the section is cut into vertical pieces: a fixed value of $y$ selects
one vertical piece that runs from the floor to the slanted plane.

**Derive the limits from the outside inward.** The outer variable is $x$. Step 1.2 gives
$-2 \leq x \leq 2$. The middle variable is $y$. In the section at a fixed $x$ the values of $y$ run from
the parabola to the plane, so $x^{2} \leq y \leq 4$. The inner variable is $z$. At a fixed $x$ and a
fixed $y$ the values of $z$ run from the floor to the plane, so $0 \leq z \leq (4 - y)/2$. The order is

$$
\iiint_{E} f\,dV = \int_{-2}^{2}\int_{x^{2}}^{4}\int_{0}^{(4-y)/2} f(x,y,z)\,dz\,dy\,dx.
$$

**Read the inner piece.** At a fixed $x$ the inner piece is a vertical segment of length $(4 - y)/2$.
That length becomes small as $y$ approaches 4, and its largest value $(4 - x^{2})/2$ occurs at
$y = x^{2}$.

**Result.** The first order is
$\int_{-2}^{2}\int_{x^{2}}^{4}\int_{0}^{(4-y)/2} f\,dz\,dy\,dx$. Its value for $f = 1$ is
$8.5333333333$.

**Check.** `code/part3_verify.py` compares this order with the order of Step 3.2. It prints the value of
each order for $f = 1$, for $f = x^{2} + y + z$, and for $f = xyz$, and it prints the smallest length of
an inner interval over a grid of the section. That smallest length is $1.994950 \times 10^{-2}$, so no
inner interval collapses. Panel (a) of Figure 3 draws the vertical inner pieces at $x = 1$.
