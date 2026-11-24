# Part 1, Step 1: Read the three limits and the order of the differentials

## The reason

The problem gives three limits and one integrand. The limits are the only description of the
solid, because the problem asks for a sketch and gives no other information. So the first task is
to read the limits without a change, and to record which limit holds which variable.

## The computation

The integral of the exercise is

$$
\int_{0}^{2}\int_{0}^{2-y}\int_{0}^{4-y^{2}} 1\,dx\,dz\,dy .
$$

The differentials at the right end are $dx\,dz\,dy$. So the order of the integration is $x$ first,
then $z$, then $y$. The rule of the iterated integral gives one limit pair for each differential:

- the inner pair belongs to $x$: $x$ runs from $0$ to $4-y^{2}$;
- the middle pair belongs to $z$: $z$ runs from $0$ to $2-y$;
- the outer pair belongs to $y$: $y$ runs from $0$ to $2$.

The inner pair may use only the variables of the outer pairs. Here the pair of $x$ holds $y$ and
does not hold $z$. The pair of $z$ holds $y$ alone. So each pair uses only a variable that is
already fixed when that pair is read. The nesting is correct, and the order needs no change.

A point $(x,y,z)$ belongs to the solid exactly when all three pairs hold:

$$
0 \le y \le 2, \qquad 0 \le z \le 2-y, \qquad 0 \le x \le 4-y^{2}.
$$

## The result

The solid is the set

$$
R = \{(x,y,z) : 0 \le y \le 2,\ 0 \le z \le 2-y,\ 0 \le x \le 4-y^{2}\}.
$$

The order $x$, then $z$, then $y$ is correct for these limits. The variable $x$ is free of $z$,
and the variable $z$ is free of $x$. Only $y$ controls both of them.

## The check

`code/part1_verify.py`, section "region". The script compares the three pairs with two other
descriptions of the same set on 40000 seeded points: the flat form of all inequalities, and the
form that solves each inequality for one variable. It reports 0 disagreements with both forms. It
also compares the pairs with the common misreading $0 \le x \le 4-z^{2}$, and it reports
disagreements there, so the comparison can fail.
