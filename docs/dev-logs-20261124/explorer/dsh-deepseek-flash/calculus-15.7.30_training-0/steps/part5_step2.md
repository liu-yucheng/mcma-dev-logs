### Step 5.2 — Write the six answers in one table

**Reason.** The answer to the exercise is the list of six iterated integrals, so collect them in
one place, and state which limits depend on which variable.

**Computation.** The six integrals are

$$\int_{-2}^{2}\int_{-3}^{3}\int_{-\sqrt{9-y^2}}^{\sqrt{9-y^2}}f\,dz\,dy\,dx,\qquad
\int_{-2}^{2}\int_{-3}^{3}\int_{-\sqrt{9-z^2}}^{\sqrt{9-z^2}}f\,dy\,dz\,dx,$$

$$\int_{-3}^{3}\int_{-2}^{2}\int_{-\sqrt{9-y^2}}^{\sqrt{9-y^2}}f\,dz\,dx\,dy,\qquad
\int_{-3}^{3}\int_{-\sqrt{9-y^2}}^{\sqrt{9-y^2}}\int_{-2}^{2}f\,dx\,dz\,dy,$$

$$\int_{-3}^{3}\int_{-2}^{2}\int_{-\sqrt{9-z^2}}^{\sqrt{9-z^2}}f\,dy\,dx\,dz,\qquad
\int_{-3}^{3}\int_{-\sqrt{9-z^2}}^{\sqrt{9-z^2}}\int_{-2}^{2}f\,dx\,dy\,dz,$$

with $f=f(x,y,z)$ in every one of them.

**Result.** The list above is the final answer of the exercise.

**Verification.** The script `code/part5_verify.py` checks that the six printed limit sets give one
value for $f=1+x+y^2+z^2$. The script `code/part6_verify.py` checks that each printed limit set
accepts exactly the points of $E$ in a random sample of $20000$ points.
