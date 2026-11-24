# Step 4.2: Independent numerical check

## Reason

A closed form can hide an error in a bound. A numerical method that uses only the three inequalities
can find such an error, because it never uses the algebraic form of the answer.

## Computation

The check uses two methods.

1. Adaptive triple quadrature integrates the constant $1$ over the set
   $x^2+z^2\le 4$, $-1\le y\le 4-z$, with $z$ taken from $-\sqrt{4-x^2}$ to $\sqrt{4-x^2}$ and $y$ taken
   from $-1$ to $4-z$.
2. A Monte Carlo estimate draws random points in the box $[-2,2]\times[-1,6]\times[-2,2]$ of volume
   $V_{\text{box}}=4\cdot 7\cdot 4=112$. The estimate is $112$ times the fraction of the points that
   satisfy the three inequalities.

The seed is $20261122$, and the sample count is $4\,000\,000$.

## Check

The quadrature gives $62.831853071796$, and the difference from $20\pi$ is $1.4\times10^{-14}$.

The Monte Carlo estimate is $62.777736$, with the standard error

$$\sigma=V_{\text{box}}\sqrt{\frac{p(1-p)}{N}}\approx 0.027794,$$

where $p$ is the estimated fraction. The estimate lies $1.947$ standard errors from $20\pi$, below the
accepted limit of $3$.

## Result

$$V=20\pi\approx 62.831853071796.$$

All four parts give the same value.

## Verification

`code/part4_verify.py` prints the polar value, the quadrature value, and the Monte Carlo estimate with
its standard error. It asserts that each value lies within its stated difference from $20\pi$, and that
the Monte Carlo estimate lies within $3$ standard errors of the quadrature value.
