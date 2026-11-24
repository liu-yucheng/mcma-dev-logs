## Step 1.3 — The outer limit fixes the variable x, and the limits give six inequalities

**Why.** The last differential is $dx$. The outer integral runs in $x$ from $0$ to $1$, and this limit uses no other variable. The three limits now describe the solid completely.

**Step.** Write the three statements of the limits as one set:

$$R = \{(x,y,z) : 0 \le x \le 1,\ 0 \le z \le 1-x,\ 0 \le y \le 2-2z\} .$$

Each statement with a limit that uses a variable becomes one inequality with two variables. The set $R$ is therefore the common part of six half-spaces:

$$x \ge 0,\quad x \le 1,\quad z \ge 0,\quad x+z \le 1,\quad y \ge 0,\quad y+2z \le 2 .$$

**Result.** The solid $R$ is the set of points in the first octant that satisfy $x \le 1$, $x+z \le 1$, and $y+2z \le 2$. It fits in the box $0 \le x \le 1$, $0 \le y \le 2$, $0 \le z \le 1$. The section at $y=0$ is the triangle with the corners $(0,0)$, $(1,0)$, and $(0,1)$ in the $xz$-plane, and its area is $1/2$.

**Check.** `code/part1_verify.py` builds the box from the corner points of $R$ and compares it with the box that the limits give. It also computes the area of the section at $y=0$ in two ways: by clipping the plane with the six half-spaces, and by the exact formula for the triangle.
