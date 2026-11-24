# Step 4.2: check the answer with two independent quadratures

## Reason

A numerical method that uses another parameterization shares neither the antiderivative of Part 3 nor the fraction arithmetic of Step 4.1. Two such methods test the value from two more directions, and each method reports its own error.

A reader may take a Monte Carlo value as exact, but that value carries a standard error, and the meaningful statement is the gap in standard errors, not the gap in units.

## Computation

The polar quadrature uses the radius $r$ and the angle $\theta$ of the plane $y^{2} + z^{2} = 9$ and the Jacobian $r$, with $x$ from $0$ to $\dfrac{r\cos\theta}{3}$. It gives ${{p4_polar_decimal}}$, and the same parameters give the volume ${{p4_polar_volume_decimal}}$.

The Monte Carlo method samples $4\times 10^{6}$ points of the box $0 \le x \le 1$, $0 \le y \le 3$, $0 \le z \le 3$ and averages the density of the points that fall inside the solid. It gives ${{p4_monte_carlo_decimal}}$ with a standard error of ${{p4_monte_carlo_error}}$, which is ${{p4_monte_carlo_standard_errors}}$ standard errors from the answer.

## Result

The four values ${{p3_answer_decimal}}$, ${{p4_second_order_decimal}}$, ${{p4_polar_decimal}}$ and ${{p4_monte_carlo_decimal}}$ agree within their stated errors. The answer of the problem is $\dfrac{27}{8} = 3.375$.

## Verification

`code/part4_verify.py` runs both quadratures and the parameter map that samples ${{p4_parameter_sample_count}}$ triples of the parameter box, and it finds no sampled triple outside the solid. Every value and every standard error that this step quotes comes from a print of that script.
