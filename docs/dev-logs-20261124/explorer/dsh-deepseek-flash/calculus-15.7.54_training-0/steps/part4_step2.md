## Part 4, Step 2: bound the answer by the extreme values of the function

**Goal.** Check the answer against the range of the function on $E$.

**Reason.** The average of a function over a region lies between the least and the greatest value of the function on that region. This bound is a test of the arithmetic of Step 4.1 that uses no integral, so it can fail only when the division is wrong.

**Computation.** On $E$ the function is $f = r^2 z$ with $r^2 \leq 1$ and $0 \leq z \leq 1 - r^2$. Write $s = r^2$ and $z = (1 - s) u$ with $0 \leq u \leq 1$. Then $f = s (1 - s) u$, so $f \leq s (1 - s) \leq \dfrac{1}{4}$, and the bound $\dfrac{1}{4}$ is attained at $s = \dfrac{1}{2}$, $u = 1$, that is at $r^2 = \dfrac{1}{2}$ and $z = \dfrac{1}{2}$. The least value is $0$, at every point of the axis and at the rim.

$$0 \leq f_{\text{ave}} = \frac{1}{12} \leq \frac{1}{4}$$

The average is one third of the greatest value.

**Result.** The answer $\dfrac{1}{12}$ lies inside the range $\left[0, \dfrac{1}{4}\right]$, and it is exactly $\dfrac{1}{3}$ of the greatest value $\dfrac{1}{4}$ at the point $\left(\dfrac{1}{\sqrt{2}}, 0, \dfrac{1}{2}\right)$.

**Verification.** The check `[[check:part4:largest_value_on_region]]` maximises $f$ on $E$ with a bounded quasi-Newton search over the two parameters $s$ and $u$ and returns $0.2499999999993946$ against $\dfrac{1}{4}$. The check `[[check:part4:ratio_inside_bounds]]` compares the average with both extremes. The check `[[check:part4:two_wrong_answers]]` shows that the answer of a reader who drops the division is above the greatest value, and that the answer of a reader who divides by the base area $\pi$ is $0.0416667$.

**Common mistake.** A reader may take the greatest value of $f$ for $1$, because both $x^2 + z$ and $y^2 + z$ reach $1$ at a corner of a bounding box. The region couples the two variables through $z \leq 1 - r^2$, so the largest value is $\dfrac{1}{4}$ at $r^2 = \dfrac{1}{2}$ and not $1$; a reader who weights only the density $x^2 + y^2$ gets $\dfrac{17}{60} + \dfrac{\pi}{16}$ in place of $\dfrac{11}{24} + \dfrac{3\pi}{32}$.
