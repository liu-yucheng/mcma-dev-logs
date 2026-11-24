## Step 6.2. Check that the six orders agree

**Why.** Six correct orders must return one value for one integrand. A disagreement would show an error
in at least one limit set. A large integrand that depends on all three variables gives a sharper test
than the constant 1.

**Compute the value of four integrands in each order.** The table below gives the value of each
integrand in one order, and the script prints 24 values in total.

| Integrand | Value in every order | Exact value |
| --- | --- | --- |
| $f = 1$ | $8.533333333333$ | $128/15$ |
| $f = x^{2} + y + z$ | $24.380952380952$ | $512/21$ |
| $f = 1 + xyz$ | $8.533333333333$ | $128/15$ |
| $f = e^{-x^{2}}(1 + z)$ | $9.128104606107$ | no closed form |

**Read the table.** The integrand $f = 1 + xyz$ returns the volume, because the term $xyz$ integrates to
0 over the symmetric region in $x$. The integrand $f = x^{2} + y + z$ returns $512/21$, and its parts are
$\iiint x^{2} = 512/105$, $\iiint y = 512/35$, and $\iiint z = 512/105$. The three parts sum to
$512/21$.

**Count the orders.** Six orders are a permutation of three variables, so the count is
$3! = 6$. The script prints the count of orders and the value of $3!$ side by side.

**Result.** All six orders agree for all four integrands. The largest difference between two orders is
$8.882 \times 10^{-15}$, which is the size of the rounding error of the quadrature. The six orders of
Part 6.1 are therefore six correct answers to the problem.

**Check.** `code/part6_verify.py` evaluates the six orders for the four integrands, prints the largest
difference between two orders, and compares each value with the exact fraction where a closed form
exists. It also computes the exact value of $f = 1$ and of $f = x^{2} + y + z$ from a rational
parametrisation of $E$, so the closed forms of the table are not taken on trust.
