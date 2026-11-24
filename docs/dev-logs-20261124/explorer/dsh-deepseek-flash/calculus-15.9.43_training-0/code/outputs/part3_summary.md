| Check | Computed value | Reference value | Difference | Status |
| --- | --- | --- | --- | --- |
| C1 radial integral: Simpson of $r(10+\sqrt{9-r^{2}})$ against $45+9$ | 53.9999999653 | 54 | 3.466e-08 | pass |
| C2 cylindrical volume: $2\pi$ times the radial integral against $108\pi$ | 339.292006588 | 339.292006588 | 0.000e+00 | pass |
| C3 spherical volume: product of three numerical Jacobian factors against $18\pi$ | 56.5486677646 | 56.5486677646 | 1.421e-13 | pass |
| C4 one ball of radius 13 about the origin against the true volume, the two values must differ | 4601.38603996 | 339.292006588 | 4.262e+03 | pass |
| C5 cap volume: Monte Carlo estimate against $18\pi$ | 56.578392 | 56.5486677646 | 2.972e-02 | pass |
| C6 spherical map: 3000 cap points against the membership test | 0 | 0 | 0.000e+00 | pass |
| C7 lower branch $z=10-\sqrt{9-r^{2}}$: 40 points against the membership test | 40 | 40 | 0.000e+00 | pass |
