# Part 6, Step 6.2: The check that the six forms agree

Part goal: Collect the six forms, then check that all six agree for five test functions with an exact value.

## Reason

A single order with a wrong limit can still look right. Six orders that disagree would show the fault at once, so the six values of one test function must agree with each other and with the exact value.

## Computation

The exact value of the integral of $x^{a} y^{b} z^{c}$ over $E$ follows by the substitution $x = 2u$, $z = w$, $y = 4s$, which maps $E$ onto the unit disk times the unit interval and multiplies the volume element by $8$. The result is a rational multiple of $\pi$.

The five test functions give: $f = 1$ gives $4\pi = 12.566370614$; $f = y$ gives $16\pi/3 = 16.755160819$; $f = z$ gives $0$; $f = x^{2}$ gives $8\pi/3 = 8.377580410$; $f = z^{2}$ gives $2\pi/3 = 2.094395102$.

## Result

Every order gives the exact value of every test function. The largest difference over the 30 pairs is below $7 \times 10^{-13}$, and the largest spread over the six orders of one function is below $8 \times 10^{-14}$. The six forms are equal.

## Verification

`code/part6_verify.py` compares each of the 30 values with the exact rational multiple of $\pi$ from `code/exact_integrals.py`, and compares the six values of each function with each other.
