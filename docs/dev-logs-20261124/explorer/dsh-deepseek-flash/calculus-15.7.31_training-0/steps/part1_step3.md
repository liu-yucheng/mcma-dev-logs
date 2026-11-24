## Step 1.3. Compute the volume of $E$ in two ways

**Why.** The volume is the value of $\iiint_{E} 1\,dV$. It is one number that tests a complete set of
limits. Two different orders that return the same number give evidence that both limit sets are right.

**First order: $dz\,dy\,dx$.** The outer variable is $x$. From Step 1.2, $|x| \leq 2$. For a fixed $x$
the values of $y$ run from $x^{2}$ to 4. For a fixed $y$ the values of $z$ run from 0 to $(4 - y)/2$.
Then

$$
V = \int_{-2}^{2}\int_{x^{2}}^{4} \frac{4-y}{2}\,dy\,dx
  = \int_{-2}^{2} \left[\frac{(4-y)^{2}}{4}\right]_{y=4}^{y=x^{2}} dx
  = \int_{-2}^{2} \frac{(4 - x^{2})^{2}}{4}\,dx
  = \frac{128}{15}.
$$

**Second order: $dy\,dx\,dz$.** The outer variable is $z$. From Step 1.2, $0 \leq z \leq 2$. For a fixed
$z$ the values of $x$ run from $-\sqrt{4-2z}$ to $\sqrt{4-2z}$. The inner variable is $y$, and $y$ runs
from $x^{2}$ to $4 - 2z$, so the inner integral has the closed form $4 - 2z - x^{2}$. Then

$$
V = \int_{0}^{2}\int_{-\sqrt{4-2z}}^{\sqrt{4-2z}} \left(4 - 2z - x^{2}\right) dx\,dz
  = \int_{0}^{2} \frac{4}{3}\,(4 - 2z)^{3/2}\,dz
  = \frac{128}{15}.
$$

**Result.** The volume is $128/15 = 8.5333333333$.

**Check.** `code/part1_verify.py` evaluates both orders with the quadrature of `scipy` and compares each
value with the exact fraction `Fraction(128, 15)`. It prints the exact value, the value of the order
$dz\,dy\,dx$, the value of the order $dy\,dx\,dz$, and the two deviations. The script also prints the
count of disagreements between the three-surface test and the bound chain, and the count is 0.
