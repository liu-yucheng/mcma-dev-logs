## Part 5, Step 2: collect the results and the checks

**Goal.** Present every result of the tutorial in one table and bind each result to the script that checks it.

**Reason.** A reader who wants to check one number needs the exact form, the decimal form, and the name of the check in one place. The table below carries all three, and the values in it repeat the values of Parts 1 to 4 without a new computation.

**Computation.** The table lists the projection area, the volume, the triple integral, the average value, and the largest value of the integrand.

| Quantity | Exact value | Decimal value | Checked by |
| --- | --- | --- | --- |
| Area of the projection $D$ | $\pi$ | $3.1415926536$ | `[[check:part1:projection_area]]` |
| Volume $V(E)$ | $\dfrac{\pi}{2}$ | $1.5707963268$ | `[[check:part2:volume_height_integral]]` |
| Integral of $x^2 z + y^2 z$ over $E$ | $\dfrac{\pi}{24}$ | $0.1308996939$ | `[[check:part3:exact_horizontal_route]]` |
| Average value $f_{\text{ave}}$ | $\dfrac{1}{12}$ | $0.0833333333$ | `[[check:part4:exact_ratio]]` |
| Largest value of $f$ on $E$ | $\dfrac{1}{4}$ | $0.2500000000$ | `[[check:part4:largest_value_on_region]]` |

The next table lists the three wrong answers that the tutorial warns against, with the factor by which each one misses the correct value.

| Wrong route | Value that it returns | Ratio to the correct value of the same quantity |
| --- | --- | --- |
| Drop the Jacobian factor $r$ | $\dfrac{8\pi}{105} = 0.2394$ | $\dfrac{64}{35} = 1.8286$ |
| Drop the factor $z$ of the integrand | $\dfrac{\pi}{6} = 0.5236$ | $4.0000$ |
| Skip the division by the volume | $0.1309$ | $\dfrac{\pi}{2} = 1.5708$ |

**Result.** The tutorial answer is $f_{\text{ave}} = \dfrac{1}{12} = 0.0833333$. The volume is $\dfrac{\pi}{2}$, the integral is $\dfrac{\pi}{24}$, and the largest value of the integrand on the region is $\dfrac{1}{4}$.

**Verification.** Every row of the first table names the check that prints its value. The check `[[check:part3:wrong_integrands]]` prints the first two rows of the second table, and the check `[[check:part4:two_wrong_answers]]` prints the third row.

**Common mistake.** A reader may copy the decimal value of the average as $0.0833$ and then quote it with four correct digits. The exact value is $\dfrac{1}{12}$, whose decimal form repeats the digit $3$ without end; the tutorial quotes seven decimal places, $0.0833333$, and the exact fraction is the safer form to carry forward.
