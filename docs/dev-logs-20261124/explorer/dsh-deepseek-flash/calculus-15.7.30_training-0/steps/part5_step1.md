### Step 5.1 — One function that uses all three coordinates

**Reason.** A general $f$ has no numeric value, so the six orders cannot be compared by a number.
Choose one function that depends on all three coordinates, and compare the six orders on that
function. The closed form of its integral follows from Parts 1, 3, and 4.

**Computation.** Take $f(x,y,z)=1+x+y^2+z^2$. Then

$$\iiint_E f\,dV=V+\iiint_E x\,dV+\iiint_E y^2\,dV+\iiint_E z^2\,dV
=36\pi+0+81\pi+81\pi=198\pi\approx 622.0353.$$

The term $\iiint_E x\,dV$ is $0$ because the solid is symmetric about the plane $x=0$ and the
integrand is odd in $x$.

**Result.** The six orders must all give $198\pi$ for this function.

**Verification.** The script `code/part5_verify.py` evaluates the six orders with six separate
nested quadratures and reports $622.035345410779$ six times against $198\pi=622.035345410779$. The
largest pairwise difference of the six values is $3.4\times10^{-13}$.
