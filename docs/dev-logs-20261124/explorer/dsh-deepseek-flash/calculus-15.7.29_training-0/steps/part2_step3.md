# Part 2, Step 2.3: The section at each boundary value of $y$

Part goal: Describe the projection that the two orders with an outer integral in $x$ or in $z$ need, and describe the section at a fixed height.

## Reason

A formula for the semi-axes returns $0$ at $y = 4$. A reader must read the printed corner list before naming any shape, because a shape with equal corners is not an ellipse.

## Computation

The script prints the four extreme points of the section at each height.

At $y = 0$ the corners are $(2, 0, 0)$, $(-2, 0, 0)$, $(0, 0, 1)$, and $(0, 0, -1)$: four distinct positions, so the section is a filled ellipse.

At $y = 2$ the corners are $(\sqrt{2}, 2, 0)$, $(-\sqrt{2}, 2, 0)$, $(0, 2, \sqrt{2}/2)$, and $(0, 2, -\sqrt{2}/2)$: four distinct positions, so the section is a filled ellipse.

At $y = 4$ the four corners coincide at $(0, 4, 0)$: one position, so the section is a single point.

## Result

The section is a filled ellipse for $0 \leq y < 4$, and a single point at $y = 4$. The collapse happens first at the top of the solid, and nowhere else.

## Verification

`code/part2_verify.py` prints the corner list of each section and counts the distinct positions. It also counts the points of a grid of $2001$ by $2001$ positions at $y = 4$ that belong to the section, and the count is exactly $1$.
