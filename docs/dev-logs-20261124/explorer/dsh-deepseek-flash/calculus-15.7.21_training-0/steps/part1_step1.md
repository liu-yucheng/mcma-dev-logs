# Step 1.1 - Turn the three equations into one inequality chain

Part 1: what the solid is.

## Reason

The statement names three surfaces: the cylinder $y = x^{2}$, the plane $z = 0$, and the plane $y + z = 1$. A surface that encloses a solid is a wall of the solid. Therefore the solid is the set of points that lie on the same side of all three walls. Two sides exist for each wall, so the statement alone does not yet fix the solid. The word "enclosed" fixes it: the solid is the bounded side, and the bounded side is the only choice that gives a finite set.

## Computation

Choose the side of each wall that keeps the set finite:

- The cylinder $y = x^{2}$ opens toward the positive $y$ direction. The bounded side is $y \geq x^{2}$.
- The plane $z = 0$ is the floor. The bounded side is $z \geq 0$.
- The plane $y + z = 1$ is the roof. The bounded side is $y + z \leq 1$.

The solid is the closed set

$$S = \left\{(x, y, z) : y \geq x^{2},\; z \geq 0,\; y + z \leq 1\right\}.$$

## Result

A point belongs to the solid when the three inequalities hold. The same statement reads as one chain, because the roof and the floor both speak about $z$ at a fixed $y$:

$$x^{2} \leq y, \qquad 0 \leq z \leq 1 - y.$$

## Check

`code/part1_verify.py` compares the three-line description with the chain on 200000 random points of the bounding box. It reports 0 disagreements.
