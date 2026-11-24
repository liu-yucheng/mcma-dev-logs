# Step 2.1: Choose the order of integration

## Reason

Each bound must come from the three inequalities. The variable $y$ appears alone in the two plane
inequalities, and the cylinder restricts only $x$ and $z$. Thus, for each point $(x,z)$ of the disk, the
set of allowed $y$ is one interval, and its endpoints do not depend on $x$. An inner integral in $y$
therefore needs no split of the disk. The order $dz\,dx$ inside the disk is also free of a split,
because $z$ enters the circle through $z^2$ only.

## Computation

The inequality $x^2+z^2\le 4$ needs $4-x^2\ge 0$, so $-2\le x\le 2$. For a fixed $x$ of that interval,
the same inequality gives

$$-\sqrt{4-x^2}\le z\le\sqrt{4-x^2}.$$

For a fixed pair $(x,z)$ of the disk, Step 1.2 gives $-1\le y\le 4-z$. The three pairs of bounds give
one iterated integral:

$$V=\int_{-2}^{2}\int_{-\sqrt{4-x^2}}^{\sqrt{4-x^2}}\int_{-1}^{4-z}dy\,dz\,dx.$$

The order is $dy\,dz\,dx$: $y$ first, then $z$, then $x$.

## Check

The inner limits contain $z$, so the $y$ integral must be inside the $z$ integral. The limits of $z$
contain $x$, so the $z$ integral must be inside the $x$ integral. The printed order agrees with the
printed limits at each level.

## Result

$$V=\int_{-2}^{2}\int_{-\sqrt{4-x^2}}^{\sqrt{4-x^2}}\int_{-1}^{4-z}dy\,dz\,dx.$$

## Verification

`code/part2_verify.py` checks the inner limits at four heights. The integral of the constant $1$ from
$-1$ to $4-z$ gives $7$, $5.5$, $3.5$, and $3$ at $z=-2$, $-0.5$, $1.5$, and $2$, and the formula
$5-z$ gives the same four values. The accepted difference is $10^{-9}$.
