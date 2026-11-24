### Step 1.2 — Measure the volume, which is $36\pi$

**Reason.** The integrand $f$ is general, so no order has a numeric value that we can compare. The
volume is the one number of $E$ that we can compare, and it checks the bounds that later steps
print. The constant $36\pi$ also appears in every order when $f=1$.

**Computation.** The section at a fixed value of $x$ is the disk $y^2+z^2\leq 9$, and its area is
$\pi\cdot 3^2=9\pi$. The area does not depend on $x$, so

$$V=\int_{-2}^{2}9\pi\,dx=9\pi\cdot 4=36\pi\approx 113.0973.$$

**Result.** The volume of $E$ is $36\pi$. The bounding box $[-2,2]\times[-3,3]\times[-3,3]$ has
volume $144$, and $36\pi<144$, as a solid inside its box must satisfy.

**Verification.** The script `code/part1_verify.py` reports $113.097335529233$ from the slice
quadrature against $36\pi$, with a difference of $1.99\times10^{-13}$, and $1.42\times10^{-14}$
from a triple quadrature over the whole solid.
