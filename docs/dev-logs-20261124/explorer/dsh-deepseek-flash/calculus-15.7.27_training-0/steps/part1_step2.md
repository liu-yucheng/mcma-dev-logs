## Step 1.2 — The middle limit fixes the variable z

**Why.** Step 1.1 uses the differential $dy$. The next differential in the order is $dz$, so the middle integral runs in $z$. Its lower limit is $0$ and its upper limit is $1-x$.

**Step.** The middle limit uses $x$. For a fixed value of $x$ the variable $z$ covers the segment

$$0 \le z \le 1-x .$$

The segment has the length $1-x$. The variable $y$ is no longer free at this point: step 1.1 ties $y$ to $z$.

**Result.** For a fixed $x$ the pair $(z,y)$ fills the region $0 \le z \le 1-x$ and $0 \le y \le 2-2z$. The variable $y$ does not use $x$, but it uses $z$, and $z$ uses $x$. The dependence on $x$ therefore reaches $y$ through $z$.

**Check.** `code/part1_verify.py` compares two tests of membership for $240$ random points. The first test uses the three limit statements. The second test solves a small linear program over the six half-spaces. The two tests agree on every point, and the script prints the count.
