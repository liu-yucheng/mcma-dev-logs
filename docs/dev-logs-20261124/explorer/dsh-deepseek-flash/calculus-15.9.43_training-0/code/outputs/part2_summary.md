| Check | Computed value | Reference value | Difference | Status |
| --- | --- | --- | --- | --- |
| C1 section radius: ceiling formula against bisection on membership, 9 heights | 5.66213742559e-15 | 0 | 5.662e-15 | pass |
| C2 section area at three heights: formula against the 720-vertex shoelace polygon of bisected rays | 0.000358867576587 | 0 | 3.589e-04 | pass |
| C3 junction: area just below $z=10$ against area just above | 28.2743338823 | 28.2743338823 | 0.000e+00 | pass |
| C4 cylinder volume: Simpson integral of the section area against $\pi R^{2}H$ | 282.743338822 | 282.743338823 | 8.153e-10 | pass |
| C5 cap volume: Simpson integral of the section area against $\frac{2}{3}\pi R^{3}$ | 56.5486677646 | 56.5486677646 | 1.044e-12 | pass |
| C6 whole volume: sum of the two integrals against $90\pi+18\pi$ | 339.292006587 | 339.292006588 | 8.142e-10 | pass |
| C7 whole volume: Monte Carlo estimate against the exact value | 339.265602 | 339.292006588 | 2.640e-02 | pass |
| C8 whole volume: two exact solids against the numerical whole | 339.292006588 | 339.292006587 | 8.142e-10 | pass |
