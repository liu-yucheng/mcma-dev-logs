## Part 4, Step 1: divide the integral by the volume

**Goal.** Apply the definition of the average value.

**Reason.** The statement defines the average value of $f$ over $E$ as the triple integral of $f$ divided by the volume of $E$. Part 2 gives the volume and Part 3 gives the integral, so the average is a ratio of two checked numbers.

**Computation.**

$$f_{\text{ave}} = \frac{1}{V(E)} \iiint_{E} f\, dV = \frac{\pi / 24}{\pi / 2} = \frac{\pi}{24} \cdot \frac{2}{\pi} = \frac{2}{24} = \frac{1}{12}$$

The factor $\pi$ cancels, so the answer does not contain $\pi$.

**Result.** $f_{\text{ave}} = \dfrac{1}{12} = 0.0833333$ to seven decimal places.

**Verification.** The check `[[check:part4:exact_ratio]]` divides the exact fraction of the integral by the exact fraction of the volume and returns $\dfrac{1}{12}$. The check `[[check:part4:ratio_by_numeric_integrals]]` divides two adaptive quadratures and returns $0.0833333333$. The check `[[check:part4:decimal_form]]` rounds the exact fraction to seven decimal places and returns the string $0.0833333$.

**Common mistake.** A reader may stop at the triple integral, because the phrase "average value" reads like a property of the function alone. The definition divides by the volume of the region; without the division the result is $0.1308997$, which is the integral and not the average.
