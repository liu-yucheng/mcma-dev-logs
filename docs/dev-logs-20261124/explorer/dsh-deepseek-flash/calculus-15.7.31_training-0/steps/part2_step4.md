## Step 2.4. Integrate the area of the section over the parameter

**Why.** The volume is the integral of the area of a section over the parameter of the family. This
statement is the reason that the six orders agree: each order sums the same sections in a different
sequence. If the three slab integrals return the same number, then the six orders must return that
number too.

**Integrate the three area functions.** The parameter of the first family is $x$, and the values run
over $[-2,2]$:

$$
\int_{-2}^{2} \frac{(4 - x^{2})^{2}}{4}\,dx = \frac{128}{15}.
$$

The parameter of the second family is $y$, and the values run over $[0,4]$:

$$
\int_{0}^{4} \sqrt{y}\,(4 - y)\,dy = \frac{128}{15}.
$$

The parameter of the third family is $z$, and the values run over $[0,2]$:

$$
\int_{0}^{2} \frac{4}{3}\,(4 - 2z)^{3/2}\,dz = \frac{128}{15}.
$$

**Result.** Each of the three slab integrals equals $128/15 = 8.5333333333$, which is the volume of
Step 1.3. Each integration bound follows from the range of the parameter that Step 1.2 derived, so no
bound comes from a drawing.

**Check.** `code/part2_verify.py` evaluates each slab integral with a quadrature and compares the value
with the exact fraction `Fraction(128, 15)`. It prints the three numerical values, the exact value, and
the three deviations. The script also prints the three sampled areas of each family together with the
product of the interval lengths that produced them, so the sampled values of panels (a), (b), and (c) of
Figure 2 are the same numbers that the page prints.
