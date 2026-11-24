# Step 3.1: integrate the density in $z$

## Reason

The inner integral holds $x$ and $y$ fixed, so only $z$ varies. The density is $z$ and the upper limit is a function of $y$, so the result of this step still carries $y$ and no longer carries $z$.

A reader may drop the factor $\dfrac{1}{2}$ and write $9 - y^{2}$ for the inner integral, but the integral of $z$ from zero to a limit $b$ is $\dfrac{b^{2}}{2}$, and the square of the limit brings that factor.

## Computation

$$\int_{0}^{\sqrt{9 - y^{2}}} z\,dz = \left[\dfrac{z^{2}}{2}\right]_{0}^{\sqrt{9 - y^{2}}} = {{p3_inner_latex}}$$

## Result

The inner integral is $\dfrac{9 - y^{2}}{2}$ at every $y$ between $0$ and $3$.

## Verification

`code/part3_verify.py` evaluates the inner integral in closed form and again with a quadrature at many values of $y$, and it compares the two results with a relative tolerance of $10^{-9}$.
