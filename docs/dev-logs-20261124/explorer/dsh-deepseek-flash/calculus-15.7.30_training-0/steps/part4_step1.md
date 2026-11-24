### Step 4.1 — The section at a fixed $z$ is the same rectangle

**Reason.** The cylinder $y^2+z^2=9$ and the two planes treat $y$ and $z$ in the same way, so the
section at a fixed $z$ follows from the section at a fixed $y$ with the two letters exchanged.
Derive it again from the inequalities, because the figure must not decide the shape.

**Computation.** Fix $z=c$. The condition on the point is $-2\leq x\leq 2$ and $y^2\leq 9-c^2$.
The two conditions involve different variables, so the section is

$$\{(x,y,c): -2\leq x\leq 2,\ -\sqrt{9-c^2}\leq y\leq\sqrt{9-c^2}\}.$$

**Result.** The section at $z=c$ is the rectangle $[-2,2]\times[-\sqrt{9-c^2},\sqrt{9-c^2}]$ in the
plane $z=c$, and its area is $8\sqrt{9-c^2}$. That area equals the area of the section at $y=c$. At
$|c|=3$ the rectangle collapses to the segment $-2\leq x\leq 2$ on the line $y=0$.

**Verification.** The script `code/part4_verify.py` measures the section area on a grid at
$c=-3,-2,0,1.5,3$ and compares each measurement with $8\sqrt{9-c^2}$. It also compares the measured
area at $z=c$ with the closed form of the area at $y=c$ for three values of $c$.
