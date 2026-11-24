# Part 6. The six orders together

An order is a choice of the sequence of the three variables. The region supplies one limit set for each
sequence, so the problem asks for six answers. This part collects the six answers and then checks that
all six agree.

## Step 6.1. Collect the six orders in one table

**Why.** Each order comes from a different outer variable and a different pair of inner variables. The
table below repeats the reason of each order in one phrase, so the reader can compare them side by side.

**The six orders.** The outer variable of the first two orders is $x$, and the section is the triangle of
Step 2.1. The outer variable of the next two orders is $y$, and the section is the rectangle of
Step 2.2. The outer variable of the last two orders is $z$, and the section is the parabolic segment of
Step 2.3.

| Order | Outer limits | Middle limits | Inner limits | Section |
| --- | --- | --- | --- | --- |
| $dz\,dy\,dx$ | $-2 \leq x \leq 2$ | $x^{2} \leq y \leq 4$ | $0 \leq z \leq (4-y)/2$ | triangle |
| $dy\,dz\,dx$ | $-2 \leq x \leq 2$ | $0 \leq z \leq (4-x^{2})/2$ | $x^{2} \leq y \leq 4-2z$ | triangle |
| $dz\,dx\,dy$ | $0 \leq y \leq 4$ | $-\sqrt{y} \leq x \leq \sqrt{y}$ | $0 \leq z \leq (4-y)/2$ | rectangle |
| $dx\,dz\,dy$ | $0 \leq y \leq 4$ | $0 \leq z \leq (4-y)/2$ | $-\sqrt{y} \leq x \leq \sqrt{y}$ | rectangle |
| $dy\,dx\,dz$ | $0 \leq z \leq 2$ | $-\sqrt{4-2z} \leq x \leq \sqrt{4-2z}$ | $x^{2} \leq y \leq 4-2z$ | parabolic segment |
| $dx\,dy\,dz$ | $0 \leq z \leq 2$ | $0 \leq y \leq 4-2z$ | $-\sqrt{y} \leq x \leq \sqrt{y}$ | parabolic segment |

**Result.** The six orders are the six rows of the table. Each row names one order, and each inner pair
of limits matches the section named in the last column.

**Check.** `code/part6_verify.py` reads the same six limit sets from one definition, tests 20000 random
points against each set, and prints the count of points that a set and the three surfaces classify
differently. The count is 0 for every row, so each row describes the region of Step 1.1.
