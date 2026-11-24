# Step 3 — Write $E$ as an iterated region and choose the order

## Reason

A triple integral needs three one-variable integrals. You get them from the description of $E$: one variable must run between two functions, and the other two run over a plane region. Choose the variable that already has two bounds as the inner variable.

## Computation

In Step 1 you found two bounds on $x$ and no bound on $y$ or $z$ alone:

$$
4\left(y^{2} + z^{2}\right) \le x \le 4.
$$

In Step 2 you found that $y$ and $z$ move over the unit disk. Thus

$$
E = \left\{(x, y, z) : (y, z) \in D,\; 4\left(y^{2} + z^{2}\right) \le x \le 4\right\}.
$$

This description gives the order $dx$ first, then the area element $dA$ of the disk:

$$
\iiint_{E} x \, dV = \iint_{D} \left[\int_{4(y^{2}+z^{2})}^{4} x \, dx\right] dA.
$$

The order is good for two reasons. First, the inner integrand $x$ has the antiderivative $x^{2}/2$, so the inner integral is elementary. Second, the result of the inner integral depends only on $y^{2} + z^{2}$, and the disk $D$ is described by that same quantity.

## Result

$$
\iiint_{E} x \, dV = \iint_{D} \left(\int_{4(y^{2}+z^{2})}^{4} x \, dx\right) dA,
\qquad D = \left\{y^{2} + z^{2} \le 1\right\}.
$$

## Verification

`code/part1_verify.py` checks the length of the segment above each point of a fine random grid. The length is positive exactly on the unit disk, and the agreement of the two tests is $1.000000$.
