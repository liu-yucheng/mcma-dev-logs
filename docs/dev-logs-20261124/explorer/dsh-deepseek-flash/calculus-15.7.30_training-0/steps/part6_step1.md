### Step 6.1 — Count the orders: there are six

**Reason.** The exercise asks for the number of ways to write the integral, so count the ways
before choosing them.

**Computation.** An order is a choice of one variable for the inner integral, one of the two
remaining variables for the middle integral, and the last variable for the outer integral. There
are $3$ choices for the inner variable, $2$ for the middle variable, and $1$ for the outer
variable, so the number of orders is $3\cdot 2\cdot 1=3!=6$.

**Result.** There are exactly six orders, and they are the six permutations of the three
coordinate names.

**Verification.** The script `code/part6_verify.py` counts the orders three ways and reports $6$
from the enumeration, $6$ from the factorial formula, and $6$ from three nested loops that skip a
repeated name.
