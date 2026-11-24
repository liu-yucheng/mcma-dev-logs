## Step 4.3 — The answer is the sketch, and a check confirms the sketch

**Why.** The exercise asks for a sketch of the solid whose volume the integral gives. The answer is therefore the drawing with the data that fixes it. The volume is not the answer. The volume is a check of the drawing, because the integrand is $1$.

**Step.** Compare the drawing with the integral in three independent ways.

- The divergence theorem over the five faces gives the volume of the drawn body.
- The three families of cross sections of Step 2 each integrate to the same total.
- A rejection sample of the drawn body estimates the same total inside three standard errors.

**Result.** The drawn body is the solid $R$ of Step 1.3, and every one of the three checks returns $2/3$ within its own tolerance. The final answer of the exercise is the description and the sketch below.

> The solid is $R = \{(x,y,z) : 0 \le x \le 1,\ 0 \le z \le 1-x,\ 0 \le y \le 2-2z\}$. It sits in the box $0 \le x \le 1$, $0 \le y \le 2$, $0 \le z \le 1$. Its base is the triangle $D$ with the corners $(0,0)$, $(1,0)$, and $(0,1)$ in the plane $y=0$, and its height above a base point $(x,z)$ is $2-2z$. Its surface has five faces: the base $D$, the top face $y+2z=2$, and the three walls $x=0$, $z=0$, and $x+z=1$. The sketch is Figure 3, with the base in Figure 2.

**Check.** `code/part4_verify.py` computes the volume three ways and prints the three values. It also prints the volume of the drawn body from the divergence theorem and the estimate from the rejection sample with its standard error.
