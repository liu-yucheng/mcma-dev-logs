# Step 1.2 - Show that the solid is bounded, and name its smallest box

Part 1: what the solid is.

## Reason

A triple integral needs finite limits. Before any integral, we must know that the three walls close the solid. The test is a squeeze of the variables: each wall gives one one-sided bound, and the walls taken together must also give the opposite bound.

## Computation

Start from the floor and the roof. The two inequalities $z \geq 0$ and $y + z \leq 1$ give

$$y \leq 1 - z \leq 1,$$

so $y$ never exceeds 1. Put this bound into the cylinder inequality:

$$x^{2} \leq y \leq 1 \quad\Longrightarrow\quad x^{2} \leq 1 \quad\Longrightarrow\quad -1 \leq x \leq 1.$$

The remaining bounds come back from the same two inequalities: $y \geq x^{2} \geq 0$ and $0 \leq z \leq 1 - y \leq 1$.

## Result

Every point of the solid lies in the box

$$-1 \leq x \leq 1, \qquad 0 \leq y \leq 1, \qquad 0 \leq z \leq 1,$$

whose volume is $2 \cdot 1 \cdot 1 = 2$. The solid is bounded, so its volume is a finite number between 0 and 2.

## Check

`code/part1_verify.py` prints the box volume `2` and the membership of nine extreme points. Five of the points lie on the boundary of the solid, and four lie just outside it. `code/part2_verify.py` scans the three coordinates and prints the smallest and the largest value that a member attains: $x$ runs from `-1` to `1`, and the largest value of $y$ is `0.99999`, which is the largest grid value below 1.
