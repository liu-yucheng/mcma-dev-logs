# Step 4.2 — Confirm with random points and state the answer

**Part:** 4 — Check the answer
**Verification:** `code/part4_verify.py`

## Reason

The two exact orders share the same algebra, so a third check uses no algebra from parts 2 and 3. A
Monte Carlo estimate uses only the definition of the solid and the definition of a volume integral.
The estimate is random, so it needs a standard error and a fixed seed.

## Computation

Take the box $B = [0,4] \times [-1,1] \times [-1,1]$, with volume $16$. Draw $N = 4{,}000{,}000$
uniform points with seed `20261122`. A point belongs to $E$ when $x \ge 4(y^2+z^2)$, because
$x \le 4$ holds everywhere in $B$. The estimate is

$$I \approx \operatorname{vol}(B) \cdot \frac{1}{N} \sum_{i=1}^{N} x_i \cdot \mathbf{1}_{E}(x_i,y_i,z_i) .$$

The run gives

| quantity | value |
| --- | --- |
| points inside $E$ | 1,570,019 |
| estimate | 16.742422 |
| exact value | 16.755161 |
| standard error | 0.011437 |
| relative difference | 0.00076 |

The relative difference $7.6 \times 10^{-4}$ is well inside the tolerance $5 \times 10^{-3}$, and the
difference is smaller than one standard error. The random check agrees with the exact answer.

## Result

$$I = \frac{16\pi}{3} \approx 16.7552 .$$

Three independent computations agree: the polar order of part 3, the order with $x$ outermost of
step 4.1, and the Monte Carlo estimate of this step.

## Check

`code/part4_verify.py`, step 4.2:

- relative difference of the estimate: computed `0.00076`, tolerance `5.0e-3`, verdict pass;
- answer rounded to four decimals: computed `16.7552`, expected `16.7552`;
- exact value printed by the script: `16.755160819145562`.
