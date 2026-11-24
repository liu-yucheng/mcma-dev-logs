# Step 3.1 - Cut the solid at a fixed $x$ and derive the slice

Part 3: the slice at a fixed $x$.

## Reason

A slice is a way to check a volume, because the slice area is a one-variable function and its integral repeats the volume. The slice must come from the three inequalities, not from a drawing. A drawing shows one cut and hides the others, and it can suggest a wrong shape. So we derive the slice algebraically.

## Computation

Fix $x = a$ with $-1 \leq a \leq 1$. Put that value into the chain of Step 1.1 and keep the two remaining variables:

$$y \geq a^{2}, \qquad z \geq 0, \qquad y + z \leq 1.$$

The three conditions are conditions on the pair $\left(y, z\right)$ only, so the slice is a plane region in the $y z$ plane. Its three boundary lines are

- $y = a^{2}$, a vertical line,
- $z = 0$, a horizontal line,
- $y + z = 1$, the line of slope $-1$ through $\left(1, 0\right)$ and $\left(a^{2}, 1 - a^{2}\right)$.

## Result

The slice is the closed plane region

$$S_{a} = \left\{(y, z) : y \geq a^{2},\; z \geq 0,\; y + z \leq 1\right\}.$$

The region is bounded by three lines, so it is a triangle. The line $y = a^{2}$ cuts the horizontal line at $\left(a^{2}, 0\right)$ and the sloping line at $\left(a^{2}, 1 - a^{2}\right)$.

## Check

`code/part3_verify.py` tests the slice at $a = 0$, $a = 0.5$, and $a = 0.9$. At each abscissa it takes 200000 random points of a test box and compares the two descriptions, one from the three inequalities and one from the triangle of Step 3.2. It reports `0` disagreements at each abscissa.
