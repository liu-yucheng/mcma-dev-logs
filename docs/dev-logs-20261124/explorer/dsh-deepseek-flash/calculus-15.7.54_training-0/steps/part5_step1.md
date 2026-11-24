## Part 5, Step 1: check the whole chain with two independent routes

**Goal.** Confirm the five numbers of the tutorial by routes that share no step with Parts 2 to 4.

**Reason.** A chain of exact fractions can carry one arithmetic slip from step to step and still look consistent, because every later step repeats the same slip. An independent route is a route that starts from the region only: it uses no antiderivative of the earlier parts, and it uses a sample whose error the script can estimate.

**Computation.** The first route expands the polynomial integrand in the single variable $r$ and integrates term by term with a library that stores the coefficients, so the powers and the coefficients come from two different places. The second route draws $800000$ random points in the box $[-1, 1] \times [-1, 1] \times [0, 1]$, keeps the points that lie in $E$, and averages $f$ over the kept points.

$$V(E) \approx 1.57458, \qquad \iiint_{E} f\, dV \approx 0.13102786, \qquad f_{\text{ave}} \approx 0.08321448$$

The standard error of the average is $0.00011486$, so the sample agrees with $\dfrac{1}{12}$ inside one standard error.

**Result.** Both routes return $V(E) = \dfrac{\pi}{2}$, $\iiint_{E} f\, dV = \dfrac{\pi}{24}$, and $f_{\text{ave}} = \dfrac{1}{12}$. The tutorial answer is therefore stable under a change of method.

**Verification.** The check `[[check:part5:reduced_polynomial_route]]` returns $1.5707963268$, $0.1308996939$, and $0.0833333333$. The check `[[check:part5:direct_rejection_sample]]` returns the sample average with its standard error. The check `[[check:part5:volume_and_integral_from_sample]]` returns the volume and the integral of the same sample. The check `[[check:part5:exact_chain_identity]]` confirms that the exact ratio of the two exact fractions is $\dfrac{1}{12}$ once more, by a comparison of two fractions that the script builds separately.

**Common mistake.** A reader may treat a sample that agrees inside two standard errors as a proof of the exact value. A sample only shows that the exact value is consistent with the data; the proof of $\dfrac{1}{12}$ rests on the exact fractions of Parts 2 to 4, and the sample is a guard against a large slip.
