# Step 3.3 - Find the largest slice and the two vanishing ends

Part 3: the slice at a fixed $x$.

## Reason

The largest slice fixes the scale of the solid, and it is a cheap test of the area formula: a wrong slice shape gives a wrong maximum. The two ends of the $x$ range must also give a zero area, because the solid closes there. Both facts follow from the derivative of $A$.

## Computation

Differentiate $A\left(a\right) = \frac{1}{2}\left(1 - a^{2}\right)^{2}$:

$$A'\left(a\right) = \frac{1}{2} \cdot 2\left(1 - a^{2}\right) \cdot \left(-2a\right) = -2a\left(1 - a^{2}\right).$$

On the open interval $-1 < a < 1$ the factor $1 - a^{2}$ is positive, so the derivative vanishes only at $a = 0$. The derivative is positive for $a < 0$ and negative for $a > 0$, so $a = 0$ is the only maximum:

$$A\left(0\right) = \frac{1}{2}, \qquad A\left(\pm 1\right) = 0.$$

## Result

The largest slice has area $0.5$ and lies in the plane $x = 0$. The slice area falls to zero at $x = -1$ and at $x = 1$, where the parabola touches the line $y = 1$.

The slice is a filled triangle. It is not a ring, and it is not a disc. The area $0.5$ is therefore not of the form $\pi r^{2}$ with any radius. A ring would need an inner boundary and a hole, and the inequalities $y \geq a^{2}$, $z \geq 0$ give no hole: the point $\left(a^{2}, 0\right)$ always belongs to the slice.

## Check

`code/part3_verify.py` scans the abscissas on a fine grid and prints the largest area `0.5` at abscissa `0`. It prints the area `0` at $x = -1$ and at $x = 1$. It also prints the largest area divided by $\pi$, which is `0.159154943092`, and that number is not a radius squared of any circle that fits the slice.
